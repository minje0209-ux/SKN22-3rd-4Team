# 📊 미국 재무제표 분석 및 투자 인사이트 봇

> AI 기반 미국 상장사 재무제표 분석 도구

## 🎯 프로젝트 목표

SEC EDGAR 공시 데이터와 AI를 활용하여 미국 상장 기업의 재무제표를 분석하고, 
자연어 질의를 통해 투자 인사이트를 제공하는 종합 분석 플랫폼 구축

### 핵심 기능
1. **📥 데이터 수집**: SEC EDGAR에서 10-K, 10-Q 재무제표 자동 수집
2. **💬 Text-to-SQL**: 자연어 질문을 SQL로 변환하여 재무 데이터 조회
3. **🌐 GraphRAG**: 기업 간 관계 분석 및 시각화
4. **💡 투자 인사이트**: AI 기반 재무 분석 및 투자 추천
5. **📈 실시간 주가**: Seeking Alpha API 연동 실시간 시세 조회

---

## ✅ 진행 상황

### Phase 1: 기본 인프라 구축 ✅ 완료
- [x] 프로젝트 구조 설계
- [x] Streamlit 기반 웹 UI 구축
- [x] 다크/라이트 모드 지원
- [x] 사이드바 네비게이션

### Phase 2: 데이터 수집 ✅ 완료
- [x] SEC EDGAR API 연동
- [x] 미국 100대 기업 재무제표 수집 스크립트
- [x] **103개 기업** 데이터 수집 완료
- [x] **513개** 연간 재무 레코드 확보

### Phase 3: 데이터베이스 연동 ✅ 완료
- [x] Supabase PostgreSQL 연결
- [x] 테이블 스키마 설계 (companies, annual_reports, quarterly_reports)
- [x] 데이터 업로드 스크립트 구현
- [x] 실시간 데이터 조회 기능

### Phase 4: 실시간 주가 ✅ 완료
- [x] RapidAPI (Seeking Alpha) 연동
- [x] 실시간 주가 조회 클라이언트
- [x] 시세, 변동률, 시가총액 조회

### Phase 5: AI 분석 기능 🔄 진행 중
- [x] OpenAI API 연결 설정
- [ ] Text-to-SQL 쿼리 생성
- [ ] GraphRAG 기업 관계 분석
- [ ] 투자 인사이트 생성

### Phase 6: 고급 기능 ⏳ 예정
- [ ] 벡터 검색 (문서 유사도)
- [ ] 뉴스 감성 분석
- [ ] 포트폴리오 추천
- [ ] 리스크 평가

---

## 🗂 프로젝트 구조

```
SKN22-3rd-4Team/
├── app.py                    # Streamlit 메인 앱
├── config/
│   └── settings.py           # 환경 설정
├── src/
│   ├── data/
│   │   ├── supabase_client.py    # Supabase DB 클라이언트
│   │   └── seeking_alpha_client.py  # 실시간 주가 API
│   ├── ui/
│   │   ├── components/       # UI 컴포넌트
│   │   └── pages/            # 각 페이지 (home, sql_query, etc.)
│   └── utils/
├── scripts/
│   ├── collect_top100_financials.py  # SEC 데이터 수집
│   └── upload_to_supabase.py         # DB 업로드
├── sql/
│   └── create_all_tables.sql # 테이블 생성 스크립트
├── data/
│   └── processed/            # 수집된 재무 데이터
└── .env                      # 환경 변수
```

---

## 📊 수집된 데이터

### 기업 목록 (103개)
빅테크, 금융, 헬스케어, 소비재, 산업재, 에너지, 통신, 부동산, 유틸리티 등

### 재무 지표
| 지표 | 설명 |
|------|------|
| Revenue | 매출액 |
| Net Income | 순이익 |
| Total Assets | 총자산 |
| Total Liabilities | 총부채 |
| Stockholders Equity | 자기자본 |
| Operating Income | 영업이익 |
| EPS | 주당순이익 |
| Profit Margin | 순이익률 |
| ROE | 자기자본이익률 |
| ROA | 총자산이익률 |

---

## 🔧 설치 및 실행

### 1. 환경 설정
```bash
conda create -n dl_nlp_env python=3.12
conda activate dl_nlp_env
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일 생성:
```
OPENAI_API_KEY=sk-...
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJ...
RAPIDAPI_KEY=your-rapidapi-key
```

### 3. 데이터베이스 설정
Supabase SQL Editor에서 다음 SQL 파일들을 순서대로 실행:
1. `sql/create_all_tables.sql`: 기본 테이블 생성 (companies, annual_reports 등)
2. `sql/company_relationships.sql`: 기업 관계 테이블 생성

### 4. 데이터 생성 및 업로드 (순서대로 실행)

#### Step 1: 재무 데이터 수집
SEC EDGAR에서 103개 기업의 재무제표 데이터를 수집합니다.
```bash
python scripts/collect_top100_financials.py
```
- 결과물: `data/processed/top_100_financials_YYYYMMDD.csv`

#### Step 2: 재무 데이터 업로드
수집된 재무 데이터를 Supabase에 업로드합니다.
```bash
python scripts/upload_to_supabase.py
```

#### Step 3: 기업 관계 데이터 수집 (GraphRAG)
10-K 문서를 다운로드하고 공급사/고객사/경쟁사 정보를 추출합니다.
```bash
python scripts/collect_10k_relationships.py
```
- 결과물: `data/10k_documents/relationships.csv`

#### Step 4: 관계 데이터 업로드
추출된 관계 데이터를 Supabase에 업로드합니다.
```bash
python scripts/upload_relationships_to_supabase.py
```

### 5. 앱 실행
```bash
streamlit run app.py
```

---

## 🌐 API 연동

| 서비스 | 용도 | 상태 |
|--------|------|------|
| SEC EDGAR | 재무제표 수집 | ✅ 연동 완료 |
| Supabase | 데이터베이스 | ✅ 연동 완료 |
| RapidAPI (Seeking Alpha) | 실시간 주가 | ✅ 연동 완료 |
| OpenAI | AI 분석 | ✅ 설정 완료 |

---

## 📸 스크린샷

*Streamlit 앱 실행 후 http://localhost:8501 접속*

---

## 👥 팀원

SKN22-3rd-4Team

---

## 📝 라이선스

MIT License
