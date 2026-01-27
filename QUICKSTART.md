# Quick Start Guide

## 🚀 Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd SKN22-3rd-4Team
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
OPENAI_API_KEY=sk-your-key-here
NEO4J_PASSWORD=your-password
SEC_API_USER_AGENT=your-email@example.com
```

## 🎯 Running the Application

### Start the Streamlit web interface
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Run the example workflow
```bash
python example_workflow.py
```

### Run the interactive notebook
```bash
jupyter notebook notebooks/quickstart.ipynb
```

## 📊 Usage Workflow

### 1. Data Collection
1. Navigate to **Data Collection** page
2. Enter company ticker symbols (e.g., AAPL, MSFT, GOOGL)
3. Select filing types (10-K, 10-Q, 8-K)
4. Click "Start Collection"

### 2. Graph Analysis
1. Go to **Graph Analysis** page
2. Ask questions about company relationships
3. Explore the knowledge graph visualization
4. View relationship details and metrics

### 3. SQL Queries
1. Open **SQL Query** page
2. Type natural language questions
3. View generated SQL and results
4. Explore sample queries

### 4. Investment Insights
1. Visit **Investment Insights** page
2. Select analysis type (Company Deep Dive, Comparative Analysis, etc.)
3. Choose companies to analyze
4. Review AI-generated recommendations

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_graph_rag.py
```

## 🔧 Optional Setup

### Neo4j (for advanced graph features)
```bash
# Using Docker
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/yourpassword \
  neo4j:latest
```

### ChromaDB (for vector storage)
Already included in the dependencies. No additional setup needed.

## 📝 Example Code

### Using Text-to-SQL
```python
from src.sql.text_to_sql import TextToSQL

engine = TextToSQL()
engine.create_financial_tables()

result = engine.query_with_natural_language(
    "What is Apple's revenue in 2023?"
)
print(result['data'])
```

### Using GraphRAG
```python
from src.rag.graph_rag import GraphRAG

graph_rag = GraphRAG()
documents = [...]  # Your documents
graph = graph_rag.build_knowledge_graph(documents)

result = graph_rag.query_graph(
    "Which companies are partners with Apple?"
)
print(result['response'])
```

### Downloading SEC Filings
```python
from src.data.sec_collector import SECDataCollector
from pathlib import Path

collector = SECDataCollector(
    user_agent="your-email@example.com",
    download_dir=Path("data/raw")
)

results = collector.download_company_filings(
    ticker="AAPL",
    form_types=["10-K"],
    limit=5
)
```

## 🐛 Troubleshooting

### Import Errors
Make sure you're running from the project root and the virtual environment is activated.

### API Key Issues
Verify your `.env` file has the correct API keys:
```bash
cat .env | grep API_KEY
```

### Database Connection Issues
Check that DuckDB is properly installed:
```bash
python -c "import duckdb; print(duckdb.__version__)"
```

### SEC Download Errors
- Ensure your user agent (email) is set in `.env`
- Check SEC EDGAR rate limits (10 requests per second)
- Verify internet connection

## 📚 Resources

- [SEC EDGAR Database](https://www.sec.gov/edgar)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Neo4j Documentation](https://neo4j.com/docs/)

## 🆘 Getting Help

If you encounter issues:
1. Check the logs in the `logs/` directory
2. Review error messages in the Streamlit interface
3. Consult the `STRUCTURE.md` file for architecture details
4. Check API quotas and rate limits

## 🎓 Learning Path

1. **Start Simple**: Use the Streamlit interface to explore features
2. **Try Notebooks**: Run `quickstart.ipynb` to understand components
3. **Run Examples**: Execute `example_workflow.py` to see the full pipeline
4. **Customize**: Modify UI pages or add new analysis features
5. **Advanced**: Integrate Neo4j for advanced graph analytics

Happy analyzing! 📊🚀
