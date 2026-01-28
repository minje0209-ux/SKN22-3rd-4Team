import streamlit as st

st.set_page_config(
    page_title="StockPulse - 모든 시장 이벤트 분석",
    page_icon="📈",
    layout="wide"
)

# 커스텀 스타일
st.markdown("""
<style>
body {
    background-color: #050a0f;
}
.nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: rgba(5, 10, 15, 0.95);
}
.logo {
    color: #00d4ff;
    font-size: 24px;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 10px;
}
.nav-menu a {
    color: #94a3b8;
    text-decoration: none;
    margin-right: 30px;
    font-size: 15px;
}
.nav-menu a:hover {
    color: #38bdf8;
}
.hero-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    height: 80vh;
    max-width: 1000px;
    margin: 0 auto;
}
.ai-badge {
    display: inline-block;
    padding: 5px 15px;
    border-radius: 20px;
    border: 1px solid #005a70;
    color: #00d4ff;
    font-size: 14px;
    margin-bottom: 20px;
    background-color: rgba(0, 212, 255, 0.05);
}
.main-title {
    font-size: 64px;
    font-weight: 800;
    color: white;
    line-height: 1.2;
    margin-bottom: 20px;
}
.highlight {
    color: #38bdf8;
}
.sub-title {
    color: #94a3b8;
    font-size: 20px;
    max-width: 800px;
    margin: 0 auto 50px auto;
    line-height: 1.6;
}
.center-text {
    text-align: center;
}            
.search-box {
    background-color: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 50px;
    padding: 10px 20px;
    max-width: 800px;
    margin: 0 auto;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}
div.stButton > button {
    background-color: #00e5ff;
    color: black;
    border-radius: 30px;
    padding: 15px 40px;
    font-weight: bold;
    border: none;
    box-shadow: 0 0 15px rgba(0, 229, 255, 0.4);
    transition: all 0.3s ease;
}
div.stButton > button:hover {
    background-color: #00b8cc;
    transform: scale(1.05);
}
.tag-container {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 30px;
}
.tag {
    background-color: #1e293b;
    color: #cbd5e1;
    padding: 8px 18px;
    border-radius: 20px;
    font-size: 14px;
    cursor: pointer;
    border: 1px solid transparent;
}
.tag:hover {
    border-color: #38bdf8;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("""
<div class='nav-container'>
    <div class='logo'>📉 StockPulse</div>
    <div class='nav-menu'>
        <a href='/dashboard' target='_self'>대시보드</a>
        <a href='/rawmaterials' target='_self'>원자재 분석</a>
        <a href='/company' target='_self'>기업 탐색</a>
        <a href='/ai' target='_self'>AI 분석</a>
    </div>
    <div style='color: white;'>🔍 🔔 로그인</div>
</div>
""", unsafe_allow_html=True)

# 히어로 섹션
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.markdown("<div class='hero-container'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'div class='ai-badge'>✨ AI 기반 주식 분석 플랫폼</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'class='main-title'>모든 시장 이벤트에서<br><span class='highlight'>수혜주를 찾아보세요</span></h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'class='sub-title'>뉴스, 정책 변화, 지정학적 이슈, 산업 트렌드 등 모든 이벤트가 미국 상장 기업에 미치는 영향을 AI가 분석합니다.</span></h3>", unsafe_allow_html=True)
    
    

# 검색창
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    search_input = st.text_input("", placeholder="예: 트럼프 관세 정책으로 수혜 보는 기업은?", label_visibility="collapsed")
    btn_col1, btn_col2, btn_col3 = st.columns([1.5, 1, 1.5])
    with btn_col2:
        if st.button("분석하기 →"):
            st.success(f"'{search_input}'에 대한 AI 분석을 시작합니다!")

# 인기 검색어
st.markdown("""
<div class='tag-container'>
    <span style='color: #64748b; align-self: center;'>인기 검색:</span>
    <div class='tag'>금리 인하</div>
    <div class='tag'>AI 반도체</div>
    <div class='tag'>트럼프 관세</div>
    <div class='tag'>전기차</div>
    <div class='tag'>중동 분쟁</div>
    <div class='tag'>FDA 승인</div>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)