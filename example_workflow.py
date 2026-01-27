"""
Example script: Download and analyze SEC filings for a company

This script demonstrates the complete workflow:
1. Download SEC filings
2. Process and extract data
3. Build knowledge graph
4. Create vector embeddings
5. Run sample queries
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config.settings import settings
from config.logging_config import setup_logging
from data.sec_collector import SECDataCollector
from data.filing_processor import FilingProcessor
from rag.graph_rag import GraphRAG
from rag.vector_store import VectorStore
from sql.text_to_sql import TextToSQL

import logging

# Setup logging
logger = setup_logging(settings.LOG_LEVEL, Path("logs"))


def main():
    """Main execution function"""
    
    logger.info("=" * 60)
    logger.info("Financial Analysis Bot - Example Workflow")
    logger.info("=" * 60)
    
    # Example company
    ticker = "AAPL"
    
    # Step 1: Initialize components
    logger.info("\n[Step 1] Initializing components...")
    
    collector = SECDataCollector(
        user_agent=settings.SEC_API_USER_AGENT,
        download_dir=settings.RAW_DATA_DIR
    )
    
    processor = FilingProcessor()
    
    graph_rag = GraphRAG(
        embedding_model=settings.EMBEDDING_MODEL,
        llm_model=settings.LLM_MODEL,
        api_key=settings.OPENAI_API_KEY
    )
    
    vector_store = VectorStore(
        persist_directory=settings.VECTOR_STORE_DIR,
        collection_name="financial_documents",
        embedding_model=settings.EMBEDDING_MODEL,
        api_key=settings.OPENAI_API_KEY
    )
    
    text_to_sql = TextToSQL(
        database_url=settings.DATABASE_URL,
        llm_model=settings.LLM_MODEL,
        api_key=settings.OPENAI_API_KEY
    )
    
    logger.info("✓ All components initialized")
    
    # Step 2: Download SEC filings
    logger.info(f"\n[Step 2] Downloading SEC filings for {ticker}...")
    
    # Uncomment to actually download (requires SEC API access)
    # results = collector.download_company_filings(
    #     ticker=ticker,
    #     form_types=["10-K"],
    #     limit=2
    # )
    # logger.info(f"✓ Downloaded filings: {results}")
    
    logger.info("✓ (Skipped - set up SEC API credentials to enable)")
    
    # Step 3: Process filings
    logger.info(f"\n[Step 3] Processing filings...")
    
    # Example: Process a single filing
    # filing_path = settings.RAW_DATA_DIR / f"{ticker}/10-K/latest.txt"
    # if filing_path.exists():
    #     parsed_data = processor.parse_10k(filing_path)
    #     logger.info(f"✓ Processed filing with {len(parsed_data.get('tables', []))} tables")
    
    logger.info("✓ (Skipped - no filings to process yet)")
    
    # Step 4: Build knowledge graph
    logger.info(f"\n[Step 4] Building knowledge graph...")
    
    # Example documents
    example_docs = [
        {
            "text_content": "Apple Inc. partners with TSMC for chip manufacturing. "
                          "The company also works with Qualcomm for wireless technology.",
            "ticker": "AAPL",
            "file_path": "example_doc_1"
        }
    ]
    
    # Uncomment to build graph (requires OpenAI API key)
    # graph = graph_rag.build_knowledge_graph(example_docs)
    # logger.info(f"✓ Built graph with {graph.number_of_nodes()} nodes")
    
    logger.info("✓ (Skipped - set up OpenAI API key to enable)")
    
    # Step 5: Create vector embeddings
    logger.info(f"\n[Step 5] Creating vector embeddings...")
    
    # Uncomment to create embeddings (requires OpenAI API key)
    # chunks = processor.extract_text_chunks(filing_path)
    # documents = [
    #     {
    #         "id": f"chunk_{i}",
    #         "text": chunk["text"],
    #         "metadata": {"ticker": ticker, "chunk_id": i}
    #     }
    #     for i, chunk in enumerate(chunks)
    # ]
    # vector_store.add_documents(documents)
    
    logger.info("✓ (Skipped - set up OpenAI API key to enable)")
    
    # Step 6: Initialize SQL database
    logger.info(f"\n[Step 6] Setting up SQL database...")
    
    text_to_sql.create_financial_tables()
    logger.info("✓ Created financial tables")
    
    # Step 7: Run sample queries
    logger.info(f"\n[Step 7] Running sample queries...")
    
    # Uncomment to run actual queries (requires OpenAI API key and data)
    # question = "What is Apple's total revenue?"
    # result = text_to_sql.query_with_natural_language(question)
    # logger.info(f"Question: {question}")
    # logger.info(f"SQL: {result.get('sql')}")
    
    logger.info("✓ (Skipped - load data first to enable queries)")
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Workflow completed!")
    logger.info("=" * 60)
    logger.info("\nNext steps:")
    logger.info("1. Add your API keys to .env file")
    logger.info("2. Run: streamlit run app.py")
    logger.info("3. Use the web interface to collect and analyze data")
    

if __name__ == "__main__":
    main()
