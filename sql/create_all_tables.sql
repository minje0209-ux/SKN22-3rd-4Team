-- ==========================================
-- Supabase 전체 테이블 생성 스크립트
-- ==========================================
-- 이 파일을 Supabase SQL Editor에서 실행하세요

-- ==========================================
-- 1. 확장 기능 활성화 (Extensions)
-- ==========================================
create extension if not exists "uuid-ossp";

-- ==========================================
-- 2. 기업 기본 정보 테이블 (Companies)
-- ==========================================
create table if not exists companies (
    id uuid primary key default uuid_generate_v4(),
    ticker text unique not null,
    company_name text not null,
    cik text,
    industry text,
    sector text,
    description text,
    logo_url text,
    market_cap numeric,
    employees int,
    exchange text,
    website text,
    created_at timestamp with time zone default now()
);

comment on table companies is '미국 상장 기업의 기본 메타데이터를 저장하는 테이블';

-- ==========================================
-- 3. 연간 재무 데이터 테이블 (Annual_Reports)
-- ==========================================
create table if not exists annual_reports (
    id uuid primary key default uuid_generate_v4(),
    company_id uuid references companies(id) on delete cascade,
    
    fiscal_year int not null,
    period_ended date,
    
    -- 손익계산서
    revenue numeric,
    cost_of_revenue numeric,
    gross_profit numeric,
    operating_income numeric,
    net_income numeric,
    eps numeric,
    
    -- 재무상태표
    total_assets numeric,
    total_liabilities numeric,
    stockholders_equity numeric,
    
    -- 현금흐름표
    operating_cash_flow numeric,
    investing_cash_flow numeric,
    financing_cash_flow numeric,
    
    -- 재무비율
    profit_margin numeric,
    roe numeric,
    roa numeric,
    debt_to_equity numeric,
    current_ratio numeric,
    
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now(),
    
    unique(company_id, fiscal_year)
);

comment on table annual_reports is '10-K 기반 연간 재무제표 데이터를 저장하는 테이블';

-- ==========================================
-- 4. 분기별 재무 데이터 테이블 (Quarterly_Reports)
-- ==========================================
create table if not exists quarterly_reports (
    id uuid primary key default uuid_generate_v4(),
    company_id uuid references companies(id) on delete cascade,
    
    fiscal_year int not null,
    fiscal_quarter int not null,
    period_ended date not null,
    
    revenue numeric,
    gross_profit numeric,
    operating_income numeric,
    net_income numeric,
    eps numeric,
    operating_cash_flow numeric,
    
    created_at timestamp with time zone default now(),
    
    unique(company_id, fiscal_year, fiscal_quarter)
);

comment on table quarterly_reports is '정확한 수치 계산을 위해 구조화된 재무 제표 데이터를 저장하는 테이블';

-- ==========================================
-- 5. 벡터 데이터 테이블 (Document_Sections)
-- ==========================================
-- 참고: vector 확장이 필요합니다. Supabase에서는 기본 제공됩니다.
create table if not exists document_sections (
    id uuid primary key default uuid_generate_v4(),
    company_id uuid references companies(id) on delete cascade,
    
    content text not null,
    section_name text,
    report_type text,
    report_date date,
    
    -- OpenAI text-embedding-3-small 모델 기준 (1536차원)
    -- embedding vector(1536),
    
    metadata jsonb,
    created_at timestamp with time zone default now()
);

comment on table document_sections is '공시 문서(PDF/HTML)를 조각내어 벡터 임베딩과 함께 저장하는 테이블';

-- ==========================================
-- 6. 인덱스 생성
-- ==========================================
create index if not exists idx_annual_reports_company on annual_reports(company_id);
create index if not exists idx_annual_reports_year on annual_reports(fiscal_year);
create index if not exists idx_quarterly_reports_company on quarterly_reports(company_id);
create index if not exists idx_quarterly_reports_year on quarterly_reports(fiscal_year);
create index if not exists idx_document_sections_company on document_sections(company_id);
create index if not exists idx_companies_cik on companies(cik);

-- ==========================================
-- 완료 메시지
-- ==========================================
-- 테이블 생성이 완료되었습니다!
