"""
Test suite for Text-to-SQL module
"""
import pytest
from src.sql.text_to_sql import TextToSQL


class TestTextToSQL:
    """Test cases for Text-to-SQL"""
    
    @pytest.fixture
    def text_to_sql(self):
        """Create a TextToSQL instance for testing"""
        engine = TextToSQL(database_url="duckdb:///:memory:")
        engine.create_financial_tables()
        return engine
    
    def test_initialization(self, text_to_sql):
        """Test TextToSQL initialization"""
        assert text_to_sql is not None
        assert text_to_sql.conn is not None
    
    def test_create_tables(self, text_to_sql):
        """Test table creation"""
        # Tables should be created in fixture
        result = text_to_sql.conn.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
        ).fetchall()
        
        table_names = [row[0] for row in result]
        assert "financial_statements" in table_names
        assert "companies" in table_names
        assert "financial_ratios" in table_names
    
    def test_natural_language_to_sql(self, text_to_sql):
        """Test natural language to SQL conversion"""
        question = "What is the total revenue for Apple?"
        result = text_to_sql.natural_language_to_sql(question)
        
        assert result["success"] is True
        assert result["sql"] is not None
        assert "SELECT" in result["sql"].upper()
    
    def test_execute_query(self, text_to_sql):
        """Test SQL query execution"""
        # Simple test query
        sql = "SELECT 1 as test"
        result = text_to_sql.execute_query(sql)
        
        assert result["success"] is True
        assert result["data"] is not None
        assert len(result["data"]) == 1
