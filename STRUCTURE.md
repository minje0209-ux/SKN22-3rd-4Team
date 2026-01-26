# Financial Analysis & Investment Insights Bot - Project Structure

## 📁 Complete Directory Structure

```
SKN22-3rd-4Team/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (git-ignored)
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── README.md                      # Project documentation
│
├── config/                        # Configuration files
│   ├── settings.py               # Application settings
│   └── logging_config.py         # Logging configuration
│
├── src/                          # Source code
│   ├── core/                     # Core business logic
│   │   └── (future core modules)
│   │
│   ├── data/                     # Data collection and processing
│   │   ├── sec_collector.py     # SEC EDGAR data downloader
│   │   └── filing_processor.py  # Filing parser and processor
│   │
│   ├── rag/                      # RAG (Retrieval Augmented Generation)
│   │   ├── graph_rag.py         # GraphRAG implementation
│   │   └── vector_store.py      # Vector database operations
│   │
│   ├── sql/                      # SQL and database
│   │   └── text_to_sql.py       # Natural language to SQL converter
│   │
│   ├── ui/                       # Streamlit UI components
│   │   └── pages/               # Page modules
│   │       ├── home.py          # Home page
│   │       ├── data_collection.py  # Data collection page
│   │       ├── graph_analysis.py   # Graph analysis page
│   │       ├── sql_query.py     # SQL query page
│   │       └── insights.py      # Investment insights page
│   │
│   └── utils/                    # Utility functions
│       ├── helpers.py           # General helpers
│       └── financial_calcs.py   # Financial calculations
│
├── tests/                        # Test suite
│   ├── unit/                    # Unit tests
│   │   ├── test_graph_rag.py
│   │   └── test_text_to_sql.py
│   └── integration/             # Integration tests
│       └── (future integration tests)
│
├── data/                        # Data storage
│   ├── raw/                    # Raw SEC filings
│   ├── processed/              # Processed data
│   └── vector_store/           # Vector database storage
│
├── models/                      # Trained models storage
│   └── (model checkpoints)
│
└── notebooks/                   # Jupyter notebooks for analysis
    └── (analysis notebooks)
```

## 🔧 Module Descriptions

### Core Modules

#### `app.py`
- Main Streamlit application entry point
- Navigation and routing
- Custom styling and CSS
- Settings management

#### `config/`
- **settings.py**: Centralized configuration using Pydantic
- **logging_config.py**: Logging setup and configuration

### Data Layer

#### `src/data/`
- **sec_collector.py**: Downloads SEC EDGAR filings (10-K, 10-Q, 8-K)
- **filing_processor.py**: Parses and extracts structured data from filings

### RAG Layer

#### `src/rag/`
- **graph_rag.py**: GraphRAG implementation for relationship analysis
  - Entity extraction
  - Relationship identification
  - Knowledge graph construction
  - Graph querying
  
- **vector_store.py**: Vector database operations using ChromaDB
  - Document embeddings
  - Semantic search
  - Similarity queries

### SQL Layer

#### `src/sql/`
- **text_to_sql.py**: Natural language to SQL conversion
  - Schema management
  - Query generation using LLM
  - Query execution
  - Result formatting

### UI Layer

#### `src/ui/pages/`
- **home.py**: Landing page with overview
- **data_collection.py**: SEC filing download interface
- **graph_analysis.py**: Knowledge graph exploration
- **sql_query.py**: Natural language query interface
- **insights.py**: AI-powered investment recommendations

### Utilities

#### `src/utils/`
- **helpers.py**: General utility functions
- **financial_calcs.py**: Financial ratio calculations

### Tests

#### `tests/`
- **unit/**: Unit tests for individual modules
- **integration/**: Integration tests for workflows

## 🚀 Next Steps

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Run tests**:
   ```bash
   pytest tests/
   ```

## 📝 Notes

- Python 3.12+ is required
- No `__init__.py` files needed (implicit namespace packages)
- All modules use absolute imports from `src/`
- Configuration is managed through environment variables
- Logging is centralized through the logging config
