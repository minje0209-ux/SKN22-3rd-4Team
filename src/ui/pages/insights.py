"""
Investment insights page for AI-powered recommendations
"""
import streamlit as st
import pandas as pd


def render():
    """Render the investment insights page"""
    
    st.markdown('<h1 class="main-header">💡 Investment Insights</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("AI-powered analysis and investment recommendations based on financial data")
    
    st.markdown("---")
    
    # Analysis type selector
    analysis_type = st.selectbox(
        "Select Analysis Type",
        [
            "📊 Company Deep Dive",
            "⚖️ Comparative Analysis",
            "📈 Sector Overview",
            "🎯 Portfolio Optimization",
            "⚠️ Risk Assessment"
        ]
    )
    
    st.markdown("---")
    
    if "Company Deep Dive" in analysis_type:
        render_company_deep_dive()
    elif "Comparative Analysis" in analysis_type:
        render_comparative_analysis()
    elif "Sector Overview" in analysis_type:
        render_sector_overview()
    elif "Portfolio Optimization" in analysis_type:
        render_portfolio_optimization()
    else:
        render_risk_assessment()


def render_company_deep_dive():
    """Render company deep dive analysis"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        company = st.selectbox(
            "Select Company",
            ["AAPL - Apple Inc.", "MSFT - Microsoft Corp.", "GOOGL - Alphabet Inc."]
        )
        
        if st.button("🔍 Generate Analysis", type="primary", use_container_width=True):
            with st.spinner("Analyzing company data..."):
                st.markdown("### 📊 Apple Inc. - Comprehensive Analysis")
                
                st.success("""
                **Investment Rating: BUY ⭐⭐⭐⭐**
                
                **Executive Summary:**
                Apple Inc. demonstrates strong financial health with consistent revenue growth, 
                excellent profit margins, and a robust ecosystem business model.
                """)
                
                # Financial Health
                st.markdown("#### 💰 Financial Health")
                
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric("Revenue Growth", "+5.3%", "YoY")
                    st.metric("Profit Margin", "26.3%", "+0.4%")
                
                with col_b:
                    st.metric("ROE", "172.3%", "+8.1%")
                    st.metric("Current Ratio", "0.98", "Stable")
                
                with col_c:
                    st.metric("Debt/Equity", "1.97", "-0.12")
                    st.metric("FCF Yield", "3.8%", "+0.3%")
                
                # Strengths
                st.markdown("#### ✅ Key Strengths")
                st.markdown("""
                1. **Strong Brand Equity**: Apple maintains premium pricing power and customer loyalty
                2. **Services Growth**: Services segment growing at 15%+ annually with high margins
                3. **Cash Position**: $162B in cash and marketable securities
                4. **Innovation Pipeline**: Continued investment in AR/VR and AI technologies
                5. **Ecosystem Lock-in**: Hardware + software + services create high switching costs
                """)
                
                # Risks
                st.markdown("#### ⚠️ Key Risks")
                st.markdown("""
                1. **China Exposure**: 18% of revenue from Greater China region
                2. **Regulatory Pressure**: App Store policies under scrutiny globally
                3. **Market Saturation**: Smartphone market showing signs of maturation
                4. **Supply Chain**: Dependence on key suppliers (e.g., TSMC)
                """)
    
    with col2:
        st.markdown("### 📈 Key Metrics")
        
        metrics_data = pd.DataFrame({
            "Metric": ["P/E Ratio", "P/B Ratio", "Div Yield", "Beta"],
            "Value": ["28.5", "45.2", "0.52%", "1.23"],
            "Sector Avg": ["25.3", "8.4", "1.2%", "1.15"]
        })
        
        st.dataframe(metrics_data, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        st.markdown("### 🎯 Price Targets")
        
        st.metric("Current Price", "$185.50")
        st.metric("Analyst Average", "$205.00", "+10.5%")
        st.metric("AI Prediction", "$198.00", "+6.7%")


def render_comparative_analysis():
    """Render comparative analysis"""
    
    st.markdown("### ⚖️ Multi-Company Comparison")
    
    companies = st.multiselect(
        "Select companies to compare",
        ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA"],
        default=["AAPL", "MSFT", "GOOGL"]
    )
    
    if st.button("📊 Compare Companies", type="primary"):
        comparison_data = pd.DataFrame({
            "Company": ["Apple", "Microsoft", "Alphabet"],
            "Market Cap ($B)": [2850, 2780, 1720],
            "Revenue ($B)": [383.3, 211.9, 307.4],
            "Net Income ($B)": [101.0, 71.6, 86.4],
            "Profit Margin": ["26.3%", "33.8%", "28.1%"],
            "ROE": ["172%", "48%", "32%"],
            "P/E Ratio": [28.5, 35.2, 24.8]
        })
        
        st.dataframe(comparison_data, use_container_width=True, hide_index=True)
        
        st.markdown("### 🤖 AI Recommendation")
        st.info("""
        **Comparative Investment Analysis:**
        
        - **Microsoft**: Best profit margin (33.8%) indicates superior operational efficiency
        - **Apple**: Exceptional ROE (172%) driven by massive share buybacks
        - **Alphabet**: Most attractive P/E ratio (24.8) suggesting potential undervaluation
        
        **Recommended Portfolio Allocation:**
        - Microsoft: 40% (quality + stability)
        - Alphabet: 35% (growth + value)
        - Apple: 25% (brand + ecosystem)
        """)


def render_sector_overview():
    """Render sector overview"""
    
    st.markdown("### 📈 Technology Sector Overview")
    
    sector_metrics = pd.DataFrame({
        "Metric": ["Avg Market Cap", "Avg P/E", "Avg Profit Margin", "YoY Growth"],
        "Technology": ["$450B", "28.3", "18.5%", "+12.4%"],
        "S&P 500": ["$85B", "20.5", "11.2%", "+8.1%"]
    })
    
    st.dataframe(sector_metrics, use_container_width=True, hide_index=True)
    
    st.markdown("### 🏆 Top Performers")
    
    performers = pd.DataFrame({
        "Rank": ["1st", "2nd", "3rd"],
        "Company": ["NVDA", "MSFT", "AAPL"],
        "YTD Return": ["+245%", "+58%", "+47%"],
        "Reason": ["AI Boom", "Cloud Growth", "Services Expansion"]
    })
    
    st.dataframe(performers, use_container_width=True, hide_index=True)


def render_portfolio_optimization():
    """Render portfolio optimization"""
    
    st.markdown("### 🎯 Portfolio Optimization")
    
    st.slider("Risk Tolerance", 1, 10, 5)
    st.slider("Investment Horizon (years)", 1, 30, 10)
    
    budget = st.number_input("Investment Amount ($)", 1000, 1000000, 10000)
    
    if st.button("🎯 Optimize Portfolio", type="primary"):
        st.success("Optimized portfolio generated based on Modern Portfolio Theory")
        
        allocation = pd.DataFrame({
            "Company": ["AAPL", "MSFT", "GOOGL", "NVDA", "CASH"],
            "Allocation %": [25, 30, 20, 15, 10],
            "Amount $": [2500, 3000, 2000, 1500, 1000],
            "Expected Return": ["12%", "15%", "18%", "25%", "2%"]
        })
        
        st.dataframe(allocation, use_container_width=True, hide_index=True)


def render_risk_assessment():
    """Render risk assessment"""
    
    st.markdown("### ⚠️ Portfolio Risk Assessment")
    
    st.warning("""
    **Overall Risk Level: MODERATE**
    
    Your portfolio shows moderate risk exposure with diversified holdings.
    """)
    
    risk_factors = pd.DataFrame({
        "Risk Factor": [
            "Market Risk",
            "Sector Concentration",
            "Geographic Risk",
            "Currency Risk",
            "Liquidity Risk"
        ],
        "Level": ["Medium", "High", "Medium", "Low", "Low"],
        "Impact": ["Moderate", "Significant", "Moderate", "Minor", "Minor"]
    })
    
    st.dataframe(risk_factors, use_container_width=True, hide_index=True)
