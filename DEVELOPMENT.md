# Development Guide

## 🏗️ Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit UI Layer                     │
│  (home, data_collection, graph_analysis, sql_query)     │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────┴───────────────────────────────────────┐
│                  Application Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  GraphRAG    │  │ Text-to-SQL  │  │ Vector Store │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────┴───────────────────────────────────────┐
│                    Data Layer                            │
│  ┌──────────────┐  ┌──────────────┐                     │
│  │SEC Collector │  │Filing Parser │                     │
│  └──────────────┘  └──────────────┘                     │
└─────────────────────────────────────────────────────────┘
                  │
┌─────────────────┴───────────────────────────────────────┐
│                  Storage Layer                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ DuckDB   │  │ ChromaDB │  │  Neo4j   │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
```

## 🔨 Adding New Features

### Adding a New UI Page

1. Create a new file in `src/ui/pages/`:
```python
# src/ui/pages/my_feature.py
import streamlit as st

def render():
    st.markdown("# My Feature")
    # Your implementation
```

2. Import and add to navigation in `app.py`:
```python
from ui.pages import my_feature

# In sidebar
page = st.sidebar.radio(
    "Select Page",
    [..., "🆕 My Feature"]
)

# In routing
if page == "🆕 My Feature":
    my_feature.render()
```

### Adding a New Data Source

1. Create collector in `src/data/`:
```python
# src/data/my_data_source.py
class MyDataCollector:
    def __init__(self):
        pass
    
    def collect_data(self):
        # Implementation
        pass
```

2. Add processing logic in `src/data/`:
```python
class MyDataProcessor:
    def process(self, raw_data):
        # Process and structure data
        return structured_data
```

### Adding New Financial Calculations

1. Add functions to `src/utils/financial_calcs.py`:
```python
def calculate_my_ratio(param1: float, param2: float) -> float:
    """Calculate custom financial ratio"""
    if param2 == 0:
        return None
    return param1 / param2
```

2. Use in analysis:
```python
from utils.financial_calcs import calculate_my_ratio

ratio = calculate_my_ratio(value1, value2)
```

## 🧪 Testing Guidelines

### Writing Unit Tests

Create test files in `tests/unit/`:
```python
# tests/unit/test_my_feature.py
import pytest
from src.my_module import MyClass

class TestMyClass:
    @pytest.fixture
    def instance(self):
        return MyClass()
    
    def test_functionality(self, instance):
        result = instance.do_something()
        assert result == expected_value
```

### Writing Integration Tests

Create test files in `tests/integration/`:
```python
# tests/integration/test_my_workflow.py
def test_complete_workflow():
    # Test multiple components working together
    pass
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_my_feature.py

# Run with coverage
pytest --cov=src

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/
```

## 📊 Database Schema

### Financial Statements Table
```sql
CREATE TABLE financial_statements (
    id INTEGER PRIMARY KEY,
    ticker VARCHAR,
    company_name VARCHAR,
    filing_date DATE,
    fiscal_year INTEGER,
    fiscal_quarter INTEGER,
    revenue DECIMAL(18, 2),
    net_income DECIMAL(18, 2),
    total_assets DECIMAL(18, 2),
    ...
)
```

### Adding New Tables

1. Define schema in `src/sql/text_to_sql.py`:
```python
def create_my_table(self):
    self.conn.execute("""
        CREATE TABLE IF NOT EXISTS my_table (
            id INTEGER PRIMARY KEY,
            field1 VARCHAR,
            field2 DECIMAL
        )
    """)
```

2. Update schema info for LLM understanding

## 🎨 UI Customization

### Custom CSS
Add styles in `app.py`:
```python
st.markdown("""
<style>
    .my-custom-class {
        background-color: #f0f0f0;
        padding: 1rem;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)
```

### Custom Components
Create reusable components:
```python
# src/ui/components/metric_card.py
def metric_card(title, value, change):
    st.markdown(f"""
    <div class="metric-card">
        <h3>{title}</h3>
        <p>{value} <span>{change}</span></p>
    </div>
    """, unsafe_allow_html=True)
```

## 🔧 Configuration

### Environment Variables
Add to `.env`:
```env
MY_API_KEY=your-key-here
MY_SETTING=value
```

### Settings
Add to `config/settings.py`:
```python
class Settings(BaseSettings):
    MY_API_KEY: Optional[str] = Field(None, env="MY_API_KEY")
    MY_SETTING: str = Field("default", env="MY_SETTING")
```

## 📝 Code Style

### Python Style Guide
- Follow PEP 8
- Use type hints where possible
- Maximum line length: 100 characters
- Use docstrings for all public functions/classes

### Example:
```python
def my_function(param1: str, param2: int) -> dict:
    """
    Brief description of function
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
    """
    # Implementation
    return {"result": "value"}
```

### Format Code
```bash
# Auto-format with black
black src/

# Check with flake8
flake8 src/

# Type check with mypy
mypy src/
```

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment

#### Using Streamlit Cloud
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Configure secrets in Streamlit settings
4. Deploy

#### Using Docker
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py"]
```

## 🐛 Debugging

### Enable Debug Mode
In `.env`:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### View Logs
```bash
# View application logs
tail -f logs/app_*.log
```

### Streamlit Debugging
```python
# Add debug information
st.write("Debug info:", debug_variable)

# Use expander for debug output
with st.expander("Debug Info"):
    st.json(debug_data)
```

## 📚 Additional Resources

- **Python 3.12 Features**: https://docs.python.org/3.12/whatsnew/3.12.html
- **Streamlit Documentation**: https://docs.streamlit.io
- **DuckDB Documentation**: https://duckdb.org/docs/
- **LangChain Documentation**: https://python.langchain.com/docs/
- **ChromaDB Documentation**: https://docs.trychroma.com/

## 🤝 Contributing

1. Create a feature branch
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation
5. Submit pull request

## 💡 Best Practices

1. **Always use type hints** for better code clarity
2. **Write tests** for all new features
3. **Document complex logic** with comments
4. **Keep functions focused** - single responsibility
5. **Handle errors gracefully** - use try/except with logging
6. **Validate user input** before processing
7. **Use constants** instead of magic numbers
8. **Cache expensive operations** in Streamlit with `@st.cache_data`
