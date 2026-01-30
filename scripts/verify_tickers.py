
import os
import sys
from dotenv import load_dotenv
from supabase import create_client

sys.path.append(os.path.join(os.getcwd(), 'src'))
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def verify():
    # Check count
    response = supabase.table("tickers").select("*", count="exact").execute()
    count = response.count
    print(f"Total rows in 'tickers': {count}")
    
    # Check sample
    response = supabase.table("tickers").select("*").limit(5).execute()
    print("\nSample data:")
    for row in response.data:
        print(f"Ticker: {row['ticker']}, Korean: {row['korean_name']}")
        print(f"Keywords: {row['keywords']}")
        print("-" * 20)

if __name__ == "__main__":
    verify()
