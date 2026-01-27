-- ==========================================
-- 기업 관계 데이터 테이블 (Company Relationships)
-- ==========================================
-- 10-K 공시에서 추출한 기업 간 관계 정보

create table if not exists company_relationships (
    id uuid primary key default uuid_generate_v4(),
    source_company text not null,         -- 원본 기업명 (10-K 작성 기업)
    source_ticker text,                   -- 원본 기업 티커
    target_company text not null,         -- 대상 기업명 (관계 대상)
    target_ticker text,                   -- 대상 기업 티커 (알려진 경우)
    relationship_type text not null,      -- 관계 유형 (supplier, customer, competitor, subsidiary, partner, mentioned)
    confidence numeric default 0.5,       -- 신뢰도 (0-1)
    extracted_from text,                  -- 추출된 섹션 (business, risk_factors, mda)
    filing_date date,                     -- 10-K 제출일
    created_at timestamp with time zone default now()
);

comment on table company_relationships is '10-K 공시에서 추출한 기업 간 관계 정보 (GraphRAG용)';

-- 인덱스 생성
create index if not exists idx_relationships_source on company_relationships(source_company);
create index if not exists idx_relationships_target on company_relationships(target_company);
create index if not exists idx_relationships_type on company_relationships(relationship_type);
create index if not exists idx_relationships_source_ticker on company_relationships(source_ticker);
create index if not exists idx_relationships_target_ticker on company_relationships(target_ticker);

-- ==========================================
-- 10-K 문서 섹션 테이블 (Document Sections)
-- ==========================================
-- RAG용 문서 청크 저장 (이미 있으면 업데이트)

-- 기존 document_sections 테이블에 컬럼 추가 (없으면)
alter table document_sections add column if not exists ticker text;
alter table document_sections add column if not exists filing_date date;

-- 인덱스
create index if not exists idx_document_sections_ticker on document_sections(ticker);
