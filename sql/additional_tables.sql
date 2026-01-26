-- ==========================================
-- 추가 테이블: 연간 재무 데이터 (Annual_Reports)
-- ==========================================
-- BM 포인트: 연간 재무제표 데이터 저장용 (10-K 기반)

create table if not exists annual_reports (
    id uuid primary key default uuid_generate_v4(),
    company_id uuid references companies(id) on delete cascade,
    
    fiscal_year int not null,             -- 회계 연도
    period_ended date,                    -- 해당 연도 종료일
    
    -- 주요 재무 지표 (단위: USD)
    revenue numeric,                      -- 매출액
    cost_of_revenue numeric,              -- 매출원가
    gross_profit numeric,                 -- 매출 총이익
    operating_income numeric,             -- 영업 이익
    net_income numeric,                   -- 당기 순이익
    eps numeric,                          -- 주당 순이익 (Earnings Per Share)
    
    -- 재무 상태표
    total_assets numeric,                 -- 총자산
    total_liabilities numeric,            -- 총부채
    stockholders_equity numeric,          -- 자기자본
    
    -- 현금흐름표
    operating_cash_flow numeric,          -- 영업 활동 현금 흐름
    investing_cash_flow numeric,          -- 투자 활동 현금 흐름
    financing_cash_flow numeric,          -- 재무 활동 현금 흐름
    
    -- 주요 비율
    profit_margin numeric,                -- 순이익률
    roe numeric,                          -- 자기자본이익률
    roa numeric,                          -- 총자산이익률
    debt_to_equity numeric,               -- 부채비율
    current_ratio numeric,                -- 유동비율
    
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now(),
    
    -- 동일 기업의 동일 연도 데이터 중복 방지
    unique(company_id, fiscal_year)
);

comment on table annual_reports is '10-K 기반 연간 재무제표 데이터를 저장하는 테이블';

-- 인덱스 생성
create index if not exists idx_annual_reports_company on annual_reports(company_id);
create index if not exists idx_annual_reports_year on annual_reports(fiscal_year);
create index if not exists idx_annual_reports_company_year on annual_reports(company_id, fiscal_year);

-- ==========================================
-- 추가 테이블: 주가 데이터 (Stock_Prices)
-- ==========================================
-- BM 포인트: 시계열 주가 데이터 및 밸류에이션 분석용

create table if not exists stock_prices (
    id uuid primary key default uuid_generate_v4(),
    company_id uuid references companies(id) on delete cascade,
    
    price_date date not null,             -- 거래일
    open_price numeric,                   -- 시가
    high_price numeric,                   -- 고가
    low_price numeric,                    -- 저가
    close_price numeric,                  -- 종가
    adjusted_close numeric,               -- 수정 종가
    volume bigint,                        -- 거래량
    
    -- 밸류에이션 지표
    market_cap numeric,                   -- 시가총액
    pe_ratio numeric,                     -- PER
    pb_ratio numeric,                     -- PBR
    ps_ratio numeric,                     -- PSR
    
    created_at timestamp with time zone default now(),
    
    -- 동일 기업의 동일 날짜 데이터 중복 방지
    unique(company_id, price_date)
);

comment on table stock_prices is '일별 주가 및 밸류에이션 지표를 저장하는 테이블';

-- 인덱스 생성
create index if not exists idx_stock_prices_company on stock_prices(company_id);
create index if not exists idx_stock_prices_date on stock_prices(price_date);

-- ==========================================
-- companies 테이블에 추가 컬럼
-- ==========================================
-- 기존 테이블에 CIK 등 추가 정보

alter table companies add column if not exists cik text;
alter table companies add column if not exists market_cap numeric;
alter table companies add column if not exists employees int;
alter table companies add column if not exists founded_year int;
alter table companies add column if not exists headquarters text;
alter table companies add column if not exists website text;
alter table companies add column if not exists exchange text;  -- NYSE, NASDAQ 등

-- CIK 인덱스 추가
create index if not exists idx_companies_cik on companies(cik);
