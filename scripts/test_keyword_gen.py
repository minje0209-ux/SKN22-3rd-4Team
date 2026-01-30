import sys
import os
import asyncio
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))
# Add scripts to path to import populate_tickers
sys.path.append(os.path.join(os.getcwd(), 'scripts'))

# Import after setting up path
# We need to make sure we can import from populate_tickers
# Since populate_tickers.py is in the same directory, if we run from root, we need to handle it.
# If we run this script from root: python scripts/test_keyword_gen.py
# scripts.populate_tickers might work if scripts is a package, but it's not (no __init__.py usually).
# So adding scripts to path is good.

try:
    from populate_tickers import generate_keywords
except ImportError:
    # effective path hack
    sys.path.append(os.path.dirname(__file__))
    from populate_tickers import generate_keywords

load_dotenv()

async def test():
    test_companies = [
        {"ticker": "AAPL", "korean_name": "애플"},
        {"ticker": "TSLA", "korean_name": "테슬라"},
        {"ticker": "NVDA", "korean_name": "엔비디아"}
    ]
    
    print("Testing keyword generation...")
    for comp in test_companies:
        print(f"\n--- Testing {comp['ticker']} ---")
        keywords = await generate_keywords(comp)
        print(f"Generated {len(keywords)} keywords:")
        print(keywords)

if __name__ == "__main__":
    asyncio.run(test())
