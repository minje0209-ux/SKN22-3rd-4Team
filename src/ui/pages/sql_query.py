"""
SQL 쿼리 페이지 - Supabase DB 연동
자연어 질문을 SQL로 변환하고 Supabase에서 실행
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    from src.data.supabase_client import SupabaseClient
    SUPABASE_AVAILABLE = True
except:
    SUPABASE_AVAILABLE = False


def format_currency(value):
    """통화 포맷팅"""
    if pd.isna(value) or value is None:
        return "-"
    if abs(value) >= 1e9:
        return f"${value/1e9:.2f}B"
    elif abs(value) >= 1e6:
        return f"${value/1e6:.2f}M"
    return f"${value:,.0f}"


def execute_predefined_query(query_type: str, params: dict = None):
    """미리 정의된 쿼리 실행"""
    if not SUPABASE_AVAILABLE:
        return pd.DataFrame(), "Supabase 연결 필요"
    
    try:
        client = SupabaseClient.get_client()
        
        if query_type == "top_revenue":
            year = params.get("year", 2024)
            limit = params.get("limit", 10)
            result = client.table("annual_reports").select(
                "revenue, net_income, companies(ticker, company_name)"
            ).eq("fiscal_year", year).not_.is_("revenue", "null").order(
                "revenue", desc=True
            ).limit(limit).execute()
            
        elif query_type == "company_detail":
            ticker = params.get("ticker", "AAPL")
            company = SupabaseClient.get_company_by_ticker(ticker)
            if not company:
                return pd.DataFrame(), f"{ticker} 기업을 찾을 수 없습니다."
            
            result = client.table("annual_reports").select("*").eq(
                "company_id", company["id"]
            ).order("fiscal_year", desc=True).execute()
            
        elif query_type == "profit_margin_ranking":
            year = params.get("year", 2024)
            result = client.table("annual_reports").select(
                "profit_margin, roe, companies(ticker, company_name)"
            ).eq("fiscal_year", year).not_.is_("profit_margin", "null").order(
                "profit_margin", desc=True
            ).limit(20).execute()
            
        elif query_type == "all_companies":
            result = client.table("companies").select("ticker, company_name, cik").order("ticker").execute()
            
        elif query_type == "year_comparison":
            ticker = params.get("ticker", "AAPL")
            company = SupabaseClient.get_company_by_ticker(ticker)
            if not company:
                return pd.DataFrame(), f"{ticker} 기업을 찾을 수 없습니다."
            
            result = client.table("annual_reports").select(
                "fiscal_year, revenue, net_income, total_assets, eps"
            ).eq("company_id", company["id"]).order("fiscal_year", desc=True).execute()
        
        else:
            return pd.DataFrame(), "알 수 없는 쿼리 타입"
        
        if not result.data:
            return pd.DataFrame(), "결과 없음"
        
        df = pd.DataFrame(result.data)
        
        # companies 정보 분리
        if 'companies' in df.columns:
            df['ticker'] = df['companies'].apply(lambda x: x.get('ticker') if x else None)
            df['company_name'] = df['companies'].apply(lambda x: x.get('company_name') if x else None)
            df = df.drop(columns=['companies'])
        
        return df, None
        
    except Exception as e:
        return pd.DataFrame(), str(e)


def render():
    """SQL 쿼리 페이지 렌더링"""
    
    st.markdown('<h1 class="main-header">💬 SQL 쿼리</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("자연어로 질문하면 Supabase DB에서 데이터를 조회합니다")
    
    # 연결 상태
    if SUPABASE_AVAILABLE:
        st.success("✅ Supabase 연결됨")
    else:
        st.error("❌ Supabase 연결 필요")
        return
    
    st.markdown("---")
    
    # 쿼리 입력
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_area(
            "💬 재무 데이터에 대해 질문하세요",
            placeholder="예: Apple의 2024년 매출은? / 매출 상위 10개 기업 / 순이익률이 가장 높은 기업",
            height=100
        )
    
    with col2:
        st.markdown("**빠른 선택:**")
        
        quick_query = st.selectbox(
            "쿼리 선택",
            [
                "",
                "📊 매출 상위 기업",
                "📈 특정 기업 상세",
                "💰 순이익률 랭킹",
                "📋 전체 기업 목록",
                "📅 연도별 비교"
            ],
            label_visibility="collapsed"
        )
    
    # 추가 옵션
    if quick_query in ["📊 매출 상위 기업", "💰 순이익률 랭킹"]:
        col_a, col_b = st.columns(2)
        with col_a:
            year = st.selectbox("연도", [2024, 2023, 2022, 2021, 2020])
        with col_b:
            limit = st.slider("상위 N개", 5, 30, 10)
    elif quick_query in ["📈 특정 기업 상세", "📅 연도별 비교"]:
        ticker = st.text_input("티커 입력", value="AAPL").upper()
    
    # 쿼리 실행
    if st.button("🚀 쿼리 실행", type="primary", use_container_width=True):
        with st.spinner("데이터 조회 중..."):
            
            if quick_query == "📊 매출 상위 기업":
                df, error = execute_predefined_query("top_revenue", {"year": year, "limit": limit})
                query_desc = f"{year}년 매출 상위 {limit}개 기업"
                
            elif quick_query == "📈 특정 기업 상세":
                df, error = execute_predefined_query("company_detail", {"ticker": ticker})
                query_desc = f"{ticker} 기업 재무 데이터"
                
            elif quick_query == "💰 순이익률 랭킹":
                df, error = execute_predefined_query("profit_margin_ranking", {"year": year})
                query_desc = f"{year}년 순이익률 상위 기업"
                
            elif quick_query == "📋 전체 기업 목록":
                df, error = execute_predefined_query("all_companies", {})
                query_desc = "등록된 전체 기업 목록"
                
            elif quick_query == "📅 연도별 비교":
                df, error = execute_predefined_query("year_comparison", {"ticker": ticker})
                query_desc = f"{ticker} 연도별 재무 추이"
            
            else:
                # 자연어 쿼리 처리 (간단한 패턴 매칭)
                query_lower = query.lower()
                
                if "상위" in query_lower or "top" in query_lower or "매출" in query_lower:
                    df, error = execute_predefined_query("top_revenue", {"year": 2024, "limit": 10})
                    query_desc = "매출 상위 기업"
                elif any(ticker in query.upper() for ticker in ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]):
                    # 티커 추출
                    for t in ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA"]:
                        if t in query.upper():
                            df, error = execute_predefined_query("company_detail", {"ticker": t})
                            query_desc = f"{t} 기업 정보"
                            break
                else:
                    df, error = execute_predefined_query("all_companies", {})
                    query_desc = "기업 목록"
            
            # 결과 표시
            if error:
                st.error(f"❌ 오류: {error}")
            elif df.empty:
                st.warning("결과가 없습니다.")
            else:
                st.markdown(f"### 📊 결과: {query_desc}")
                st.markdown(f"*{len(df)}개 레코드 조회됨*")
                
                # 숫자 컬럼 포맷팅
                display_df = df.copy()
                for col in ['revenue', 'net_income', 'total_assets', 'total_liabilities', 'operating_income']:
                    if col in display_df.columns:
                        display_df[col] = display_df[col].apply(format_currency)
                
                for col in ['profit_margin', 'roe', 'roa']:
                    if col in display_df.columns:
                        display_df[col] = display_df[col].apply(
                            lambda x: f"{x*100:.1f}%" if pd.notna(x) else "-"
                        )
                
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                # 차트 (숫자 데이터가 있는 경우)
                if 'revenue' in df.columns and 'ticker' in df.columns:
                    st.markdown("### 📈 매출 비교")
                    chart_df = df[['ticker', 'revenue']].dropna()
                    if not chart_df.empty:
                        chart_df['revenue'] = pd.to_numeric(chart_df['revenue'], errors='coerce') / 1e9
                        chart_df = chart_df.set_index('ticker').head(10)
                        st.bar_chart(chart_df)
                
                elif 'fiscal_year' in df.columns and 'revenue' in df.columns:
                    st.markdown("### 📈 연도별 추이")
                    chart_df = df[['fiscal_year', 'revenue']].dropna()
                    if not chart_df.empty:
                        chart_df['revenue'] = pd.to_numeric(chart_df['revenue'], errors='coerce') / 1e9
                        chart_df = chart_df.set_index('fiscal_year').sort_index()
                        st.line_chart(chart_df)
    
    st.markdown("---")
    
    # 샘플 쿼리
    with st.expander("💡 샘플 질문"):
        st.markdown("""
        **기본 조회:**
        - "전체 기업 목록 보여줘"
        - "Apple의 재무 정보"
        - "매출 상위 10개 기업"
        
        **비교 분석:**
        - "AAPL, MSFT, GOOGL 매출 비교"
        - "2023년 vs 2024년 매출 변화"
        
        **비율 분석:**
        - "순이익률 상위 기업"
        - "ROE가 가장 높은 회사"
        """)
    
    # 데이터베이스 스키마
    with st.expander("📚 데이터베이스 스키마"):
        st.markdown("""
        **companies 테이블:**
        - ticker (티커), company_name (기업명), cik (CIK 번호)
        
        **annual_reports 테이블:**
        - fiscal_year (회계연도)
        - revenue (매출), net_income (순이익)
        - total_assets (총자산), total_liabilities (총부채)
        - stockholders_equity (자기자본)
        - operating_income (영업이익), operating_cash_flow (영업현금흐름)
        - eps (주당순이익)
        - profit_margin (순이익률), roe, roa, debt_to_equity (부채비율)
        """)
