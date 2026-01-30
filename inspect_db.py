import os
import sys
from dotenv import load_dotenv
from supabase import create_client

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL or SUPABASE_KEY not found in .env")
    sys.exit(1)

supabase = create_client(url, key)

try:
    # Fetch one row to see columns
    response = supabase.table("companies").select("*").limit(1).execute()
    if response.data:
        print("Columns in 'companies' table:")
        print(response.data[0].keys())
    else:
        print("'companies' table is empty.")

    # Check for volume in other tables if not in companies
    # Try stock_prices for volume
    try:
        response_prices = supabase.table("stock_prices").select("*").limit(1).execute()
        if response_prices.data:
            print("\nColumns in 'stock_prices' table:")
            print(response_prices.data[0].keys())
    except Exception as e:
        print(f"\nCould not access 'stock_prices': {e}")

except Exception as e:
    print(f"Error accessing Supabase: {e}")
