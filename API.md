# API Reference

## Core Modules

### SEC Data Collector

```python
from src.data.sec_collector import SECDataCollector

collector = SECDataCollector(
    user_agent="your-email@example.com",
    download_dir=Path("data/raw")
)
```

#### Methods

##### `download_company_filings(ticker, form_types, limit, after_date, before_date)`
Download SEC filings for a specific company.

**Parameters:**
- `ticker` (str): Company ticker symbol
- `form_types` (List[str]): List of form types (e.g., ["10-K", "10-Q"])
- `limit` (int, optional): Maximum number of filings per form type
- `after_date` (str, optional): Download filings after this date (YYYY-MM-DD)
- `before_date` (str, optional): Download filings before this date (YYYY-MM-DD)

**Returns:** dict with download results

---

### Filing Processor

```python
from src.data.filing_processor import FilingProcessor

processor = FilingProcessor()
```

#### Methods

##### `parse_10k(file_path)`
Parse a 10-K filing and extract structured information.

**Parameters:**
- `file_path` (Path): Path to the 10-K filing

**Returns:** Dict containing text_content, tables, sections, and financial_data

##### `extract_text_chunks(file_path, chunk_size, chunk_overlap)`
Extract text chunks for RAG processing.

**Parameters:**
- `file_path` (Path): Path to the filing
- `chunk_size` (int): Size of each text chunk (default: 1000)
- `chunk_overlap` (int): Overlap between chunks (default: 200)

**Returns:** List of text chunks with metadata

---

### GraphRAG

```python
from src.rag.graph_rag import GraphRAG

graph_rag = GraphRAG(
    embedding_model="text-embedding-3-small",
    llm_model="gpt-4-turbo-preview",
    api_key="your-api-key"
)
```

#### Methods

##### `build_knowledge_graph(documents, chunk_size)`
Build a knowledge graph from documents.

**Parameters:**
- `documents` (List[Dict]): List of document dictionaries
- `chunk_size` (int): Size of text chunks (default: 1000)

**Returns:** NetworkX directed graph

##### `query_graph(query, max_depth, top_k)`
Query the knowledge graph with natural language.

**Parameters:**
- `query` (str): Natural language query
- `max_depth` (int): Maximum depth for graph traversal (default: 3)
- `top_k` (int): Number of top results (default: 5)

**Returns:** Dict with query results and relevant subgraph

##### `analyze_company_relationships(company, relationship_types)`
Analyze relationships for a specific company.

**Parameters:**
- `company` (str): Company ticker or name
- `relationship_types` (List[str], optional): Types of relationships to analyze

**Returns:** Dict with relationship analysis and centrality metrics

---

### Vector Store

```python
from src.rag.vector_store import VectorStore

vector_store = VectorStore(
    persist_directory=Path("data/vector_store"),
    collection_name="financial_documents",
    embedding_model="text-embedding-3-small",
    api_key="your-api-key"
)
```

#### Methods

##### `add_documents(documents, batch_size)`
Add documents to the vector store.

**Parameters:**
- `documents` (List[Dict]): List with 'text' and 'metadata' fields
- `batch_size` (int): Batch size for processing (default: 100)

**Returns:** Number of documents added

##### `similarity_search(query, k, filter_dict)`
Search for similar documents.

**Parameters:**
- `query` (str): Search query
- `k` (int): Number of results (default: 5)
- `filter_dict` (Dict, optional): Metadata filters

**Returns:** List of similar documents with scores

##### `search_by_company(query, company, k)`
Search documents for a specific company.

**Parameters:**
- `query` (str): Search query
- `company` (str): Company ticker or name
- `k` (int): Number of results (default: 5)

**Returns:** List of relevant documents

---

### Text-to-SQL

```python
from src.sql.text_to_sql import TextToSQL

engine = TextToSQL(
    database_url="duckdb:///:memory:",
    llm_model="gpt-4-turbo-preview",
    api_key="your-api-key"
)
```

#### Methods

##### `create_financial_tables()`
Create standard financial tables.

**Returns:** None

##### `natural_language_to_sql(question)`
Convert natural language to SQL.

**Parameters:**
- `question` (str): Natural language question

**Returns:** Dict with SQL query and success status

##### `execute_query(sql)`
Execute SQL query and return results.

**Parameters:**
- `sql` (str): SQL query

**Returns:** Dict with results DataFrame and metadata

##### `query_with_natural_language(question)`
Complete pipeline: NL → SQL → Results.

**Parameters:**
- `question` (str): Natural language question

**Returns:** Dict with SQL, results, and metadata

##### `load_data_from_dataframe(df, table_name)`
Load data from pandas DataFrame.

**Parameters:**
- `df` (DataFrame): DataFrame to load
- `table_name` (str): Name of the table

**Returns:** None

---

## Utility Functions

### Financial Calculations

```python
from src.utils.financial_calcs import *
```

Available functions:
- `calculate_profit_margin(net_income, revenue)`
- `calculate_roe(net_income, shareholders_equity)`
- `calculate_roa(net_income, total_assets)`
- `calculate_current_ratio(current_assets, current_liabilities)`
- `calculate_debt_to_equity(total_debt, shareholders_equity)`
- `calculate_pe_ratio(price, eps)`
- `calculate_pb_ratio(price, book_value_per_share)`
- `calculate_operating_margin(operating_income, revenue)`
- `calculate_asset_turnover(revenue, total_assets)`
- `calculate_eps(net_income, shares_outstanding)`

### Helper Functions

```python
from src.utils.helpers import *
```

Available functions:
- `format_currency(value, currency)` - Format as currency string
- `format_percentage(value, decimals)` - Format as percentage
- `calculate_growth_rate(current, previous)` - Calculate growth rate
- `safe_divide(numerator, denominator, default)` - Safe division
- `parse_sec_date(date_string)` - Parse SEC date formats
- `chunk_list(lst, chunk_size)` - Split list into chunks
- `save_json(data, file_path)` - Save data to JSON
- `load_json(file_path)` - Load data from JSON

---

## Configuration

### Settings

```python
from config.settings import settings

# Access settings
api_key = settings.OPENAI_API_KEY
data_dir = settings.DATA_DIR
llm_model = settings.LLM_MODEL
```

Available settings:
- `BASE_DIR` - Project base directory
- `DATA_DIR` - Data directory path
- `RAW_DATA_DIR` - Raw data directory
- `PROCESSED_DATA_DIR` - Processed data directory
- `VECTOR_STORE_DIR` - Vector store directory
- `MODELS_DIR` - Models directory
- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `NEO4J_URI` - Neo4j connection URI
- `NEO4J_USER` - Neo4j username
- `NEO4J_PASSWORD` - Neo4j password
- `DATABASE_URL` - Database connection string
- `SEC_API_USER_AGENT` - SEC EDGAR user agent
- `EMBEDDING_MODEL` - Embedding model name
- `LLM_MODEL` - LLM model name
- `TEMPERATURE` - LLM temperature
- `MAX_TOKENS` - Maximum tokens
- `CHUNK_SIZE` - Text chunk size
- `CHUNK_OVERLAP` - Chunk overlap size
- `TOP_K_RESULTS` - Number of search results

### Logging

```python
from config.logging_config import setup_logging

logger = setup_logging(log_level="INFO", log_dir=Path("logs"))
```

---

## Examples

### Complete Workflow Example

```python
from pathlib import Path
from config.settings import settings
from data.sec_collector import SECDataCollector
from data.filing_processor import FilingProcessor
from rag.vector_store import VectorStore
from sql.text_to_sql import TextToSQL

# 1. Collect data
collector = SECDataCollector(
    user_agent=settings.SEC_API_USER_AGENT,
    download_dir=settings.RAW_DATA_DIR
)
results = collector.download_company_filings("AAPL", ["10-K"], limit=2)

# 2. Process filings
processor = FilingProcessor()
filing_path = settings.RAW_DATA_DIR / "AAPL/10-K/latest.txt"
parsed = processor.parse_10k(filing_path)

# 3. Create embeddings
chunks = processor.extract_text_chunks(filing_path)
vector_store = VectorStore(
    persist_directory=settings.VECTOR_STORE_DIR,
    api_key=settings.OPENAI_API_KEY
)
documents = [
    {"id": f"chunk_{i}", "text": chunk["text"], "metadata": {"ticker": "AAPL"}}
    for i, chunk in enumerate(chunks)
]
vector_store.add_documents(documents)

# 4. Query data
engine = TextToSQL(api_key=settings.OPENAI_API_KEY)
result = engine.query_with_natural_language("What is Apple's revenue?")
print(result['data'])
```

### GraphRAG Example

```python
from rag.graph_rag import GraphRAG

graph_rag = GraphRAG(api_key=settings.OPENAI_API_KEY)

# Build graph
documents = [
    {
        "text_content": "Apple partners with TSMC for chip manufacturing.",
        "ticker": "AAPL"
    }
]
graph = graph_rag.build_knowledge_graph(documents)

# Query graph
result = graph_rag.query_graph("Who are Apple's manufacturing partners?")
print(result['response'])

# Analyze relationships
analysis = graph_rag.analyze_company_relationships("AAPL")
print(analysis['centrality'])
```
