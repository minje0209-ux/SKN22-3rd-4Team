import asyncio
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

async def test_model():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    models_to_test = ["gemini-flash-latest", "gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-1.0-pro"]
    
    for model_name in models_to_test:
        print(f"\nTesting model: {model_name}")
        try:
            response = await client.aio.models.generate_content(
                model=model_name,
                contents="Hello, suggest one keyword.",
            )
            print(f"SUCCESS: {model_name}")
            print(f"Response: {response.text}")
            return # Stop after first success if you want, or remove to test all
        except Exception as e:
            print(f"FAILED: {model_name}")
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_model())
