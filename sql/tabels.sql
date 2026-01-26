-- ==========================================
-- 1. 확장 기능 활성화 (Extensions)
-- ==========================================
-- UUID 생성을 위한 확장
create extension if not exists "uuid-ossp";

-- ==========================================
-- 2. 기업 기본 정보 테이블 (Companies)
-- ==========================================
-- BM 포인트: 티커 기반으로 여러 테이블을 조인(Join)하는 기준점이 됨
create table companies (
    id uuid primary key default uuid_generate_v4(),
    ticker text unique not null,          -- 주식 티커 (예: AAPL, NVDA)
    company_name text not null,           -- 기업 정식 명칭
    industry text,                        -- 산업 분류 (예: Technology, Semiconductors)
    sector text,                          -- 섹터 분류
    description text,                     -- 기업 개요 (간단한 설명)
    logo_url text,                        -- Streamlit UI에 표시할 로고 주소
    created_at timestamp with time zone default now()
);

comment on table companies is '미국 상장 기업의 기본 메타데이터를 저장하는 테이블';

-- ==========================================
-- 3. 벡터 데이터 테이블 (Document_Sections)
-- ==========================================
-- BM 포인트: RAG의 핵심. 문서의 특정 '맥락'을 찾아내는 용도
create table document_sections (
    id uuid primary key default uuid_generate_v4(),
    company_id uuid references companies(id) on delete cascade,
    
    content text not null,                -- 분할된 실제 텍스트 내용 (Chunk)
    section_name text,                    -- 공시 문서 내 섹션명 (예: Risk Factors, MD&A)
    report_type text,                     -- 문서 종류 (10-K, 10-Q)
    report_date date,                     -- 공시 발행일
    
    -- OpenAI text-embedding-3-small 모델 기준 (1536차원)
    embedding vector(1536),               
    
    metadata jsonb,                       -- 페이지 번호, 소스 URL 등 추가 정보 저장
    created_at timestamp with time zone default now()
);

comment on table document_sections is '공시 문서(PDF/HTML)를 조각내어 벡터 임베딩과 함께 저장하는 테이블';

-- ==========================================
-- 4. 재무 수치 테이블 (Quarterly_Reports)
-- ==========================================
-- BM 포인트: Text-to-SQL용. "매출이 얼마나 늘었어?" 같은 질문에 정확한 답변 제공
create table quarterly_reports (
    id uuid primary key default uuid_generate_v4(),
    company_id uuid references companies(id) on delete cascade,
    
    fiscal_year int not null,             -- 회계 연도
    fiscal_quarter int not null,          -- 회계 분기 (1, 2, 3, 4)
    period_ended date not null,           -- 해당 분기 종료일
    
    -- 주요 재무 지표 (단위: USD)
    revenue numeric,                      -- 매출액
    gross_profit numeric,                 -- 매출 총이익
    operating_income numeric,             -- 영업 이익
    net_income numeric,                   -- 당기 순이익
    eps numeric,                          -- 주당 순이익 (Earnings Per Share)
    operating_cash_flow numeric,          -- 영업 활동 현금 흐름
    
    created_at timestamp with time zone default now(),
    
    -- 동일 기업의 동일 분기 데이터 중복 방지
    unique(company_id, fiscal_year, fiscal_quarter)
);

comment on table quarterly_reports is '정확한 수치 계산을 위해 구조화된 재무 제표 데이터를 저장하는 테이블';

-- ==========================================
-- 5. 벡터 유사도 검색용 함수 (RPC)
-- ==========================================
-- BM 포인트: Streamlit에서 최단 거리의 문서를 빠르게 찾기 위한 서버 측 함수
create or replace function match_documents (
  query_embedding vector(1536),
  match_threshold float,
  match_count int,
  filter_company_id uuid default null
)
returns table (
  id uuid,
  content text,
  section_name text,
  report_date date,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    ds.id,
    ds.content,
    ds.section_name,
    ds.report_date,
    1 - (ds.embedding <=> query_embedding) as similarity -- 코사인 유사도 계산
  from document_sections ds
  where (filter_company_id is null or ds.company_id = filter_company_id)
    and 1 - (ds.embedding <=> query_embedding) > match_threshold
  order by similarity desc
  limit match_count;
end;
$$;