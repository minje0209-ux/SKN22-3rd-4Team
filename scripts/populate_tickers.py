
import os
import sys
import asyncio
import pandas as pd
import yfinance as yf
from typing import List, Dict
from dotenv import load_dotenv
from supabase import create_client
from google import genai
from google.genai import types

# Add src to path to import modules if needed
sys.path.append(os.path.join(os.getcwd(), 'src'))

load_dotenv()

# Initialize Supabase
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_companies_from_db():
    """Fetch all companies (ticker, korean_name) from Supabase"""
    print("Fetching companies from Supabase...")
    response = supabase.table("companies").select("ticker, korean_name").execute()
    return response.data

def get_volumes_and_sort(companies: List[Dict]) -> List[Dict]:
    """Fetch volume for companies and sort by volume descending"""
    tickers = [c['ticker'] for c in companies]
    print(f"Fetching volume data for {len(tickers)} tickers via yfinance...")
    
    # Batch download is faster
    # tickers string for yfinance
    tickers_str = " ".join(tickers)
    try:
        # download last 1 day data
        data = yf.download(tickers_str, period="1d", progress=False)
        
        # Check if Volume data exists
        if hasattr(data, 'columns') and 'Volume' in data.columns:
            data = data['Volume']
            
            # Calculate recent volume (if multiple days, taking mean, otherwise just the value)
            # Handle cases where data might be simple Series or DataFrame
            if isinstance(data, pd.Series):
                 # Only one ticker
                 volumes = {tickers[0]: data.iloc[-1] if not pd.isna(data.iloc[-1]) else 0}
            else:
                # multiple tickers
                # data.iloc[-1] gives the last row (latest date)
                # Handle potential empty data
                if len(data) > 0:
                    volumes = data.iloc[-1].to_dict()
                else:
                    volumes = {}
        else:
            print("Warning: 'Volume' column not found in yfinance data.")
            volumes = {}
            
        # Add volume to company dict
        for comp in companies:
            t = comp['ticker']
            # yfinance tickers might need mapping or just use direct
            # Sometimes yfinance returns column names not matching exactly if special chars
            # But for US stocks usually fine.
            comp['volume'] = volumes.get(t, 0)
            if pd.isna(comp['volume']):
                comp['volume'] = 0
                
    except Exception as e:
        print(f"Error fetching volumes: {e}")
        # fallback: volume 0
        for comp in companies:
            comp['volume'] = 0
            
    # Sort
    sorted_companies = sorted(companies, key=lambda x: x['volume'], reverse=True)
    return sorted_companies

async def generate_keywords(company: Dict) -> List[str]:
    """Generate keywords using Gemini via google-genai SDK"""
    ticker = company['ticker']
    korean_name = company['korean_name']
    
    system_instruction = (
        "You are a robust keyword generator for a stock search engine designed for Korean users. "
        "Your goal is to generate a comprehensive list of search keywords for a given company so Korean users can find it easily.\n"
        "Generate 10-20 relevant keywords focusing on:\n"
        "1. Korean name variations and synonyms (e.g., 애플, 사과 for Apple)\n"
        "2. Korean transliterations of product names (e.g., 아이폰, 맥북, 갤럭시)\n"
        "3. Common Korean typos or short forms (e.g., 삼전, 앺을)\n"
        "4. Ticker symbol variations (e.g., AAPL, $AAPL)\n"
        "5. English product names and company name.\n\n"
        "Return ONLY a comma-separated list of keywords. Do not include any other text."
    )
    
    user_message = f"Company: {ticker} ({korean_name})"
    
    try:
        response = await client.aio.models.generate_content(
            model="gemini-flash-latest",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )
        )
        
        text = response.text
        # precise parsing
        keywords = [k.strip() for k in text.split(',') if k.strip()]
        
        # Add basic ones to ensure they are present
        basics = [ticker, korean_name, ticker.lower()]
        if korean_name:
             basics.append(korean_name.replace(" ", "")) # Remove spaces for korean name variation
        
        # mix and dedup
        all_keywords = list(set(basics + keywords))
        # Filter out empty strings
        all_keywords = [k.strip() for k in all_keywords if k.strip()]
        print(f"Generated keywords for {ticker}")
        return all_keywords
    except Exception as e:
        print(f"Error generating keywords for {ticker}: {e}")
        # import traceback
        # traceback.print_exc()
        return [ticker, korean_name] if korean_name else [ticker]

async def process_and_insert(companies: List[Dict]):
    """Generate keywords and insert into tickers table"""
    print("Generating keywords and inserting data...")
    
    # We will process in batches to verify progress
    total = len(companies)
    
    # First, clear existing tickers table? Or upsert?
    # User said "insert into this DB newly", implying maybe clearing or just adding.
    # To be safe and clean, let's upsert based on ticker if possible, or user might want clean state.
    # Given the request "create a list... in tickers db", let's assume we want to populate it.
    # I'll use upsert.
    
    # Prepare data for insertion
    insert_data = []
    
    # Limit concurrency for LLM
    semaphore = asyncio.Semaphore(5)
    
    async def process_one(comp):
        async with semaphore:
            print(f"Processing {comp['ticker']}...")
            keywords = await generate_keywords(comp)
            return {
                "ticker": comp['ticker'],
                "korean_name": comp['korean_name'],
                "keywords": keywords
            }

    tasks = [process_one(comp) for comp in companies]
    results = await asyncio.gather(*tasks)
    
    print(f"Prepared {len(results)} records. Inserting into Supabase...")
    
    # Batch insert to Supabase
    try:
        # tickers table id is likely auto-increment.
        # we insert ticker, korean_name, keywords
        response = supabase.table("tickers").upsert(results, on_conflict="ticker").execute()
        if response.data:
            print(f"Insertion complete! Inserted {len(response.data)} records.")
        else:
            print("Insertion complete! (No data returned)")
    except Exception as e:
        print(f"Error inserting into Supabase: {e}")

def main():
    # 1. Get Companies
    companies = get_companies_from_db()
    if not companies:
        print("No companies found.")
        return
    print(f"Found {len(companies)} companies.")
    
    # 2. Sort by Volume
    sorted_companies = get_volumes_and_sort(companies)
    # print top 5 to verify
    print("Top 5 by volume:", [c['ticker'] for c in sorted_companies[:5]])
    
    # 3. Generate Keywords and Insert
    asyncio.run(process_and_insert(sorted_companies))

if __name__ == "__main__":
    main()
