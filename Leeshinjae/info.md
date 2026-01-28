미국 주식 분석 서비스를 구축하기 위해 가장 신뢰도 높고 개발자 친화적인 API 서비스들의 공식 주소와 특징을 정리해 드립니다. 2026년 현재 가장 널리 쓰이는 솔루션들입니다.

---

## 1. 실시간 및 과거 시세 (Market Data)

미국 시장의 실시간 가격, 캔들 데이터, 거래량을 제공하는 대표적인 API입니다.

* **Finnhub Stock API**
* **주소:** [https://finnhub.io/](https://finnhub.io/)
* **특징:** 실시간 주가뿐만 아니라 대체 데이터(Alternative data)에 강점이 있습니다. 무료 플랜에서도 꽤 많은 양의 데이터를 제공하며 문서화가 매우 잘 되어 있습니다.


* **Polygon.io**
* **주소:** [https://polygon.io/](https://polygon.io/)
* **특징:** 초저지연(Low-latency) 실시간 데이터를 원하는 경우 가장 추천합니다. 웹소켓(WebSocket) 지원이 강력하여 실시간 대시보드 구현에 최적입니다.


* **IEX Cloud**
* **주소:** [https://iexcloud.io/](https://www.google.com/search?q=https://iexcloud.io/)
* **특징:** 사용한 만큼 지불하는 종량제(Pay-as-you-go) 모델이 잘 되어 있어 소규모 서비스 시작에 유리합니다.



---

## 2. 재무 데이터 및 공시 (Fundamentals)

기업의 손익계산서, 대차대조표, SEC 공시 자료(10-K, 10-Q)를 제공합니다.

* **Alpha Vantage**
* **주소:** [https://www.alphavantage.co/](https://www.alphavantage.co/)
* **특징:** 재무제표 데이터와 기술적 지표(RSI, MACD 등)를 JSON 형태로 아주 쉽게 받아올 수 있습니다. 초보 개발자가 사용하기 가장 쉽습니다.


* **SEC EDGAR (공식)**
* **주소:** [https://www.sec.gov/edgar/sec-api-documentation](https://www.sec.gov/edgar/sec-api-documentation)
* **특징:** 미국 증권거래위원회에서 직접 제공하는 API로 **무료**입니다. 다만, Raw 데이터를 직접 파싱해야 하므로 난이도가 조금 높습니다.


* **Financial Modeling Prep (FMP)**
* **주소:** [https://site.financialmodelingprep.com/](https://site.financialmodelingprep.com/)
* **특징:** 30년 이상의 과거 재무 데이터와 실적 발표 일정(Earnings Calendar)을 매우 깔끔하게 제공합니다.



---

## 3. 뉴스 및 투자 심리 분석 (News & Sentiment)

시장의 분위기를 파악하고 관련 뉴스를 수집할 때 사용합니다.

* **News API**
* **주소:** [https://newsapi.org/](https://newsapi.org/)
* **특징:** 전 세계 뉴스 매체의 기사를 키워드(예: "Tesla", "Apple") 기반으로 수집할 수 있는 가장 대중적인 API입니다.


* **Stocktwits API**
* **주소:** [https://stocktwits.com/developers](https://www.google.com/search?q=https://stocktwits.com/developers)
* **특징:** '미국판 종토방'인 스톡트윗의 실시간 피드를 가져올 수 있습니다. 특정 종목에 대한 개인 투자자들의 실시간 심리(Bullish/Bearish) 파악에 필수입니다.


* **Alpha Vantage (Sentiment Endpoint)**
* **주소:** [Alpha Vantage News Sentiment](https://www.google.com/search?q=https://www.alphavantage.co/documentation/%23news-sentiment)
* **특징:** 뉴스 기사를 가져올 때 AI가 분석한 **긍정/부정 점수(Sentiment Score)**를 함께 제공하므로 별도의 자연어 처리 모델을 만들지 않아도 됩니다.
3. 무료/저비용 데이터셋 및 소스 확보
- 전 종목(10,000개+) 데이터를 구축할 때 비용을 절감할 수 있는 소스들입니다.
![image.png](attachment:image.png)


