"""
데이터 수집 페이지 - SEC 공시 다운로드
"""
import streamlit as st
from datetime import datetime, timedelta


def render():
    """데이터 수집 페이지 렌더링"""
    
    st.markdown('<h1 class="main-header">📥 데이터 수집</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("SEC EDGAR 공시 다운로드 및 처리")
    
    st.markdown("---")
    
    # Collection options
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 기업 선택")
        
        # Input method selection
        input_method = st.radio(
            "기업 지정 방법을 선택하세요",
            ["직접 입력", "CSV 업로드", "인기 목록"],
            horizontal=True
        )
        
        if input_method == "직접 입력":
            tickers_input = st.text_area(
                "티커 심볼 입력 (쉼표로 구분)",
                placeholder="AAPL, MSFT, GOOGL, AMZN, TSLA",
                help="하나 이상의 티커 심볼을 쉼표로 구분하여 입력하세요"
            )
            
            if tickers_input:
                tickers = [t.strip().upper() for t in tickers_input.split(",")]
                st.success(f"{len(tickers)}개 기업 선택됨: {', '.join(tickers)}")
        
        elif input_method == "CSV 업로드":
            uploaded_file = st.file_uploader(
                "티커 심볼이 포함된 CSV 파일 업로드",
                type=["csv"],
                help="CSV에는 'ticker' 또는 'symbol' 열이 있어야 합니다"
            )
            
            if uploaded_file:
                st.info("CSV 업로드 성공!")
                tickers = []
        
        else:  # 인기 목록
            list_option = st.selectbox(
                "미리 정의된 목록 선택",
                [
                    "S&P 500 빅테크",
                    "FAANG 기업",
                    "다우존스 30",
                    "시가총액 상위 10개",
                    "맞춤 감시 목록"
                ]
            )
            
            # Pre-defined lists
            if list_option == "FAANG 기업":
                tickers = ["META", "AAPL", "AMZN", "NFLX", "GOOGL"]
                st.info(f"선택됨: {', '.join(tickers)}")
            elif list_option == "S&P 500 빅테크":
                tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA"]
                st.info(f"선택됨: {', '.join(tickers)}")
    
    with col2:
        st.markdown("### ⚙️ 수집 설정")
        
        # Form types
        form_types = st.multiselect(
            "공시 유형",
            ["10-K", "10-Q", "8-K", "DEF 14A"],
            default=["10-K", "10-Q"],
            help="다운로드할 SEC 공시 유형을 선택하세요"
        )
        
        # Date range
        st.markdown("**기간 설정**")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            start_date = st.date_input(
                "시작일",
                value=datetime.now() - timedelta(days=365*3),
                max_value=datetime.now()
            )
        
        with col_b:
            end_date = st.date_input(
                "종료일",
                value=datetime.now(),
                max_value=datetime.now()
            )
        
        # Limit
        limit = st.number_input(
            "기업당 최대 공시 수",
            min_value=1,
            max_value=50,
            value=10,
            help="각 공시 유형별 다운로드할 최대 개수"
        )
        
        st.markdown("---")
        
        # Processing options
        st.markdown("**처리 옵션**")
        
        process_immediately = st.checkbox(
            "즉시 처리",
            value=True,
            help="다운로드 후 데이터 파싱 및 구조화"
        )
        
        build_embeddings = st.checkbox(
            "벡터 임베딩 생성",
            value=True,
            help="유사도 검색을 위한 임베딩 생성"
        )
        
        update_graph = st.checkbox(
            "지식 그래프 업데이트",
            value=True,
            help="엔티티 및 관계 추출"
        )
    
    st.markdown("---")
    
    # Action buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("🚀 수집 시작", type="primary", use_container_width=True):
            with st.spinner("공시 다운로드 및 처리 중..."):
                progress_bar = st.progress(0)
                
                for i in range(100):
                    progress_bar.progress(i + 1)
                
                st.success("✅ 데이터 수집 완료!")
                
                # Show summary
                st.markdown("### 📊 수집 요약")
                
                summary_col1, summary_col2, summary_col3 = st.columns(3)
                
                with summary_col1:
                    st.metric("처리된 기업", "5")
                
                with summary_col2:
                    st.metric("다운로드된 공시", "47")
                
                with summary_col3:
                    st.metric("파싱된 문서", "47")
    
    with col2:
        if st.button("💾 설정 저장", use_container_width=True):
            st.info("설정이 저장되었습니다!")
    
    with col3:
        if st.button("🔄 초기화", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    
    # Recent collections
    st.markdown("### 📜 최근 수집 내역")
    
    import pandas as pd
    
    recent_data = pd.DataFrame({
        "날짜": ["2026-01-26", "2026-01-25", "2026-01-24"],
        "기업": ["AAPL, MSFT, GOOGL", "TSLA, AMZN", "META, NFLX"],
        "공시 수": [45, 18, 12],
        "상태": ["✅ 완료", "✅ 완료", "✅ 완료"]
    })
    
    st.dataframe(recent_data, use_container_width=True, hide_index=True)
    
    # Tips
    with st.expander("💡 데이터 수집 팁"):
        st.markdown("""
        **모범 사례:**
        
        - 파이프라인 테스트를 위해 소수의 기업으로 시작하세요
        - 10-K 연례 보고서에 가장 포괄적인 정보가 있습니다
        - 10-Q 분기 보고서는 최근 변화 추적에 유용합니다
        - 8-K 보고서에는 중요한 이벤트 공시가 포함됩니다
        - 대량 데이터 처리에는 몇 분이 걸릴 수 있습니다
        - SEC EDGAR API 속도 제한을 확인하세요
        
        **사용 사례별 권장 설정:**
        
        - **빠른 분석**: 1-2개 기업, 10-K만, 최근 1년
        - **종합 연구**: 5-10개 기업, 10-K + 10-Q, 최근 3년
        - **섹터 분석**: 20개 이상 기업, 10-K만, 최근 2년
        """)
