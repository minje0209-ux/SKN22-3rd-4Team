"""
Quick test to verify settings are loading correctly
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from config.settings import settings
    print("✅ Settings loaded successfully!")
    print(f"\n📊 Configuration:")
    print(f"- Data Directory: {settings.DATA_DIR}")
    print(f"- LLM Model: {settings.LLM_MODEL}")
    print(f"- Embedding Model: {settings.EMBEDDING_MODEL}")
    print(f"- Database URL: {settings.DATABASE_URL}")
    print(f"- OpenAI API Key: {'***' + settings.OPENAI_API_KEY[-10:] if settings.OPENAI_API_KEY else 'Not set'}")
    print(f"\n✅ All settings loaded without errors!")
    
except Exception as e:
    print(f"❌ Error loading settings: {e}")
    import traceback
    traceback.print_exc()
