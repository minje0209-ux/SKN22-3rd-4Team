"""
SEC EDGAR 10-K 문서 다운로드 및 관계 정보 추출

수집된 105개 기업의 10-K 전체 문서를 다운로드하고,
기업 간 관계 정보(공급업체, 고객, 경쟁사, 자회사)를 추출합니다.
"""
import os
import re
import json
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# SEC API 설정
SEC_BASE_URL = "https://www.sec.gov"
SEC_EDGAR_URL = "https://data.sec.gov"

# 105개 기업 티커 목록
TOP_COMPANIES = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B", "TSM", "AVGO",
    "JPM", "V", "MA", "BAC", "WFC", "GS", "MS", "AXP", "SPGI", "BLK",
    "UNH", "JNJ", "LLY", "PFE", "ABBV", "MRK", "TMO", "ABT", "DHR", "BMY",
    "WMT", "PG", "KO", "PEP", "COST", "MCD", "NKE", "DIS", "SBUX", "TGT",
    "CAT", "GE", "HON", "UNP", "RTX", "BA", "LMT", "DE", "UPS", "MMM",
    "XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO", "OXY", "KMI",
    "VZ", "T", "TMUS", "CMCSA", "CHTR",
    "PLD", "AMT", "EQIX", "CCI", "SPG",
    "NEE", "DUK", "SO", "D", "AEP",
    "ORCL", "CRM", "ADBE", "AMD", "INTC", "QCOM", "TXN", "AMAT", "MU", "LRCX",
    "ASML", "NOW", "INTU", "PYPL", "ISRG", "BKNG", "MDLZ", "ADP", "CI", "REGN",
    "CVS", "GILD", "VRTX", "AMGN", "ZTS", "SYK", "BDX", "ELV", "HUM", "MCK"
]

# 관계 키워드 패턴
RELATIONSHIP_PATTERNS = {
    "supplier": [
        r"(?:our |the )?(?:primary |major |key |principal )?supplier[s]?(?:\s+include|\s+are|\s+such as)?[\s:]+([A-Z][A-Za-z\s&,]+)",
        r"(?:we |the company )?(?:source[s]? |purchase[s]? |procure[s]? )(?:from|through)\s+([A-Z][A-Za-z\s&,]+)",
        r"(?:manufactured |produced |supplied )(?:by|from)\s+([A-Z][A-Za-z\s&,]+)",
    ],
    "customer": [
        r"(?:our |the )?(?:largest |major |key |principal )?customer[s]?(?:\s+include|\s+are)?[\s:]+([A-Z][A-Za-z\s&,]+)",
        r"(?:we |the company )?(?:sell[s]? |provide[s]? )(?:to|services? to)\s+([A-Z][A-Za-z\s&,]+)",
        r"revenue[s]? from\s+([A-Z][A-Za-z\s&,]+)",
    ],
    "competitor": [
        r"(?:our |the )?(?:primary |major |key )?competitor[s]?(?:\s+include|\s+are)?[\s:]+([A-Z][A-Za-z\s&,]+)",
        r"(?:we )?compete[s]? (?:with|against)\s+([A-Z][A-Za-z\s&,]+)",
        r"competition from\s+([A-Z][A-Za-z\s&,]+)",
    ],
    "subsidiary": [
        r"(?:our )?(?:wholly[- ]owned )?subsidiar(?:y|ies)(?:\s+include)?[\s:]+([A-Z][A-Za-z\s&,]+)",
        r"(?:we )?(?:own[s]?|acquired)\s+([A-Z][A-Za-z\s&,]+)",
    ],
    "partner": [
        r"(?:our |the )?(?:strategic )?partner(?:ship)?[s]?(?:\s+with|\s+include)?[\s:]+([A-Z][A-Za-z\s&,]+)",
        r"(?:joint venture|collaboration|alliance)\s+(?:with|between)\s+([A-Z][A-Za-z\s&,]+)",
    ],
}

# 알려진 기업명 목록 (매칭 정확도 향상용)
KNOWN_COMPANIES = set([
    "Apple", "Microsoft", "Google", "Alphabet", "Amazon", "Meta", "Facebook",
    "NVIDIA", "Tesla", "TSMC", "Taiwan Semiconductor", "Broadcom", "Qualcomm",
    "Intel", "AMD", "Samsung", "SK Hynix", "Micron", "Texas Instruments",
    "JPMorgan", "Goldman Sachs", "Morgan Stanley", "Bank of America", "Wells Fargo",
    "Visa", "Mastercard", "American Express", "PayPal",
    "Johnson & Johnson", "Pfizer", "Merck", "AbbVie", "Bristol-Myers",
    "UnitedHealth", "CVS", "Cigna", "Anthem", "Humana",
    "Walmart", "Target", "Costco", "Amazon", "Home Depot",
    "Coca-Cola", "PepsiCo", "McDonald's", "Starbucks", "Nike", "Disney",
    "ExxonMobil", "Chevron", "ConocoPhillips", "Shell", "BP",
    "AT&T", "Verizon", "T-Mobile", "Comcast", "Charter",
    "Boeing", "Lockheed Martin", "Raytheon", "General Dynamics", "Northrop Grumman",
    "Caterpillar", "Deere", "3M", "Honeywell", "General Electric",
    "Oracle", "Salesforce", "Adobe", "SAP", "ServiceNow", "Intuit",
    "Foxconn", "Hon Hai", "Pegatron", "Wistron", "Luxshare",
])


def get_user_agent():
    """SEC API 요청에 필요한 User-Agent"""
    email = os.getenv("SEC_API_USER_AGENT", "researcher@university.edu")
    return f"Mozilla/5.0 (compatible; ResearchBot/1.0; +mailto:{email})"


def get_company_cik_map() -> Dict[str, dict]:
    """티커-CIK 매핑 조회"""
    headers = {
        "User-Agent": get_user_agent(),
        "Accept": "application/json"
    }
    
    url = "https://www.sec.gov/files/company_tickers.json"
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    
    cik_map = {}
    for item in data.values():
        ticker = item.get("ticker", "").upper()
        cik = str(item.get("cik_str", "")).zfill(10)
        title = item.get("title", "")
        cik_map[ticker] = {"cik": cik, "title": title}
    
    return cik_map


def get_10k_filing_url(cik: str, headers: dict) -> Optional[Tuple[str, str]]:
    """가장 최근 10-K 파일링 URL 조회"""
    submissions_url = f"{SEC_EDGAR_URL}/submissions/CIK{cik}.json"
    
    try:
        response = requests.get(submissions_url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        recent_filings = data.get("filings", {}).get("recent", {})
        forms = recent_filings.get("form", [])
        accessions = recent_filings.get("accessionNumber", [])
        primary_docs = recent_filings.get("primaryDocument", [])
        filing_dates = recent_filings.get("filingDate", [])
        
        for i, form in enumerate(forms):
            if form == "10-K":
                accession = accessions[i].replace("-", "")
                primary_doc = primary_docs[i]
                filing_date = filing_dates[i]
                
                doc_url = f"{SEC_BASE_URL}/Archives/edgar/data/{cik.lstrip('0')}/{accession}/{primary_doc}"
                return doc_url, filing_date
        
        return None, None
    
    except Exception as e:
        print(f"      10-K 조회 오류: {e}")
        return None, None


def download_10k_document(url: str, headers: dict) -> Optional[str]:
    """10-K 문서 다운로드"""
    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"      다운로드 오류: {e}")
        return None


def extract_text_from_html(html_content: str) -> str:
    """HTML에서 텍스트 추출"""
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 스크립트, 스타일 제거
    for tag in soup(["script", "style", "meta", "link"]):
        tag.decompose()
    
    # 텍스트 추출
    text = soup.get_text(separator=" ", strip=True)
    
    # 정리
    text = re.sub(r'\s+', ' ', text)
    
    return text


def extract_sections(text: str) -> Dict[str, str]:
    """10-K 주요 섹션 추출"""
    sections = {}
    
    # Item 1 - Business
    item1_pattern = r"(?:ITEM\s*1\.?\s*[-–—]?\s*BUSINESS)(.*?)(?:ITEM\s*1A|ITEM\s*2)"
    match = re.search(item1_pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        sections["business"] = match.group(1)[:50000]  # 최대 50K 문자
    
    # Item 1A - Risk Factors
    item1a_pattern = r"(?:ITEM\s*1A\.?\s*[-–—]?\s*RISK\s*FACTORS)(.*?)(?:ITEM\s*1B|ITEM\s*2)"
    match = re.search(item1a_pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        sections["risk_factors"] = match.group(1)[:50000]
    
    # Item 7 - MD&A
    item7_pattern = r"(?:ITEM\s*7\.?\s*[-–—]?\s*MANAGEMENT)(.*?)(?:ITEM\s*7A|ITEM\s*8)"
    match = re.search(item7_pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        sections["mda"] = match.group(1)[:50000]
    
    return sections


def extract_relationships(text: str, source_company: str) -> List[Dict]:
    """텍스트에서 기업 관계 추출"""
    relationships = []
    
    for rel_type, patterns in RELATIONSHIP_PATTERNS.items():
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            
            for match in matches:
                # 매치된 기업명 정리
                companies = clean_company_names(match)
                
                for company in companies:
                    if company and len(company) > 2:
                        relationships.append({
                            "source": source_company,
                            "target": company,
                            "type": rel_type,
                        })
    
    # 알려진 기업명 직접 검색
    for known_company in KNOWN_COMPANIES:
        if known_company.lower() in text.lower() and known_company != source_company:
            # 이미 추가된 관계인지 확인
            existing = any(r["target"].lower() == known_company.lower() for r in relationships)
            if not existing:
                relationships.append({
                    "source": source_company,
                    "target": known_company,
                    "type": "mentioned",
                })
    
    return relationships


def clean_company_names(text: str) -> List[str]:
    """기업명 정리 및 분리"""
    # 콤마, and 등으로 분리
    companies = re.split(r'[,;]|\band\b|\bor\b', text)
    
    cleaned = []
    for company in companies:
        company = company.strip()
        # 불필요한 단어 제거
        company = re.sub(r'\b(Inc|Corp|Corporation|LLC|Ltd|Company|Co)\b\.?', '', company, flags=re.IGNORECASE)
        company = company.strip(" .,")
        
        # 최소 길이 확인
        if len(company) > 2 and not company.lower() in ["the", "our", "their", "such"]:
            cleaned.append(company)
    
    return cleaned


def save_document(ticker: str, content: str, sections: Dict, output_dir: Path):
    """문서 및 섹션 저장"""
    ticker_dir = output_dir / ticker
    ticker_dir.mkdir(parents=True, exist_ok=True)
    
    # 전체 텍스트 저장
    with open(ticker_dir / "full_text.txt", "w", encoding="utf-8") as f:
        f.write(content)
    
    # 섹션별 저장
    for section_name, section_text in sections.items():
        with open(ticker_dir / f"{section_name}.txt", "w", encoding="utf-8") as f:
            f.write(section_text)


def main():
    """메인 실행"""
    print("=" * 70)
    print("📥 SEC 10-K 문서 다운로드 및 관계 추출")
    print("=" * 70)
    
    # 출력 디렉토리
    output_dir = Path("data/10k_documents")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # CIK 매핑 로드
    print("\n📋 CIK 매핑 로드 중...")
    cik_map = get_company_cik_map()
    print(f"   {len(cik_map)}개 회사 정보 로드됨")
    
    headers = {
        "User-Agent": get_user_agent(),
        "Accept-Encoding": "gzip, deflate",
    }
    
    # 관계 데이터 저장용
    all_relationships = []
    processed_companies = []
    
    print(f"\n📊 {len(TOP_COMPANIES)}개 기업 10-K 처리 중...\n")
    
    for i, ticker in enumerate(TOP_COMPANIES, 1):
        lookup_ticker = ticker.replace("-", "")
        company_info = cik_map.get(ticker) or cik_map.get(lookup_ticker)
        
        if not company_info:
            print(f"  [{i:3d}/{len(TOP_COMPANIES)}] {ticker}: ❌ CIK 없음")
            continue
        
        cik = company_info["cik"]
        company_name = company_info["title"]
        
        print(f"  [{i:3d}/{len(TOP_COMPANIES)}] {ticker}: {company_name[:35]:<35}", end="", flush=True)
        
        try:
            # 10-K URL 조회
            doc_url, filing_date = get_10k_filing_url(cik, headers)
            
            if not doc_url:
                print(" ⚠️ 10-K 없음")
                continue
            
            # 이미 다운로드된 경우 스킵
            ticker_dir = output_dir / ticker
            if (ticker_dir / "full_text.txt").exists():
                print(" ⏭️ 이미 존재")
                
                # 관계만 추출
                with open(ticker_dir / "full_text.txt", "r", encoding="utf-8") as f:
                    content = f.read()
                
                relationships = extract_relationships(content[:100000], company_name)
                all_relationships.extend(relationships)
                processed_companies.append({
                    "ticker": ticker,
                    "name": company_name,
                    "filing_date": filing_date or "unknown",
                    "relationships": len(relationships)
                })
                continue
            
            # 문서 다운로드
            html_content = download_10k_document(doc_url, headers)
            
            if not html_content:
                print(" ❌ 다운로드 실패")
                continue
            
            # 텍스트 추출
            text_content = extract_text_from_html(html_content)
            
            # 섹션 추출
            sections = extract_sections(text_content)
            
            # 저장
            save_document(ticker, text_content, sections, output_dir)
            
            # 관계 추출
            relationships = extract_relationships(text_content[:100000], company_name)
            all_relationships.extend(relationships)
            
            processed_companies.append({
                "ticker": ticker,
                "name": company_name,
                "filing_date": filing_date,
                "relationships": len(relationships)
            })
            
            print(f" ✅ {len(relationships)}개 관계")
            
            # Rate limiting
            time.sleep(0.2)
        
        except Exception as e:
            print(f" ❌ 오류: {str(e)[:30]}")
    
    # 결과 저장
    print("\n" + "=" * 70)
    print("💾 결과 저장 중...")
    
    # 관계 데이터 저장
    relationships_df = pd.DataFrame(all_relationships)
    relationships_df.to_csv(output_dir / "relationships.csv", index=False)
    print(f"   관계 데이터: {len(all_relationships)}개 → relationships.csv")
    
    # JSON으로도 저장
    with open(output_dir / "relationships.json", "w", encoding="utf-8") as f:
        json.dump(all_relationships, f, ensure_ascii=False, indent=2)
    
    # 처리된 기업 목록
    processed_df = pd.DataFrame(processed_companies)
    processed_df.to_csv(output_dir / "processed_companies.csv", index=False)
    print(f"   처리된 기업: {len(processed_companies)}개 → processed_companies.csv")
    
    # 요약
    print("\n" + "=" * 70)
    print("📊 추출된 관계 요약:")
    if not relationships_df.empty:
        rel_summary = relationships_df["type"].value_counts()
        for rel_type, count in rel_summary.items():
            print(f"   {rel_type}: {count}개")
    
    print("\n✅ 완료!")
    print(f"   저장 위치: {output_dir}")
    print("=" * 70)


if __name__ == "__main__":
    main()
