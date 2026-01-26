"""
Integration test for the complete workflow
"""
import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from sql.text_to_sql import TextToSQL
import pandas as pd


class TestIntegrationWorkflow:
    """Integration tests for the complete analysis workflow"""
    
    @pytest.fixture
    def setup_system(self):
        """Set up the complete system for testing"""
        # Initialize Text-to-SQL
        engine = TextToSQL(database_url="duckdb:///:memory:")
        engine.create_financial_tables()
        
        # Load sample data
        sample_data = pd.DataFrame({
            'ticker': ['AAPL', 'MSFT'],
            'company_name': ['Apple Inc.', 'Microsoft Corp.'],
            'fiscal_year': [2023, 2023],
            'revenue': [383.3e9, 211.9e9],
            'net_income': [101.0e9, 71.6e9],
            'total_assets': [352.8e9, 411.9e9],
            'total_liabilities': [290.0e9, 205.8e9]
        })
        
        engine.load_data_from_dataframe(sample_data, 'financial_statements')
        
        return {
            'engine': engine,
            'sample_data': sample_data
        }
    
    def test_end_to_end_query(self, setup_system):
        """Test complete query workflow from question to results"""
        engine = setup_system['engine']
        
        # Run a simple query
        question = "Show all companies and their revenue"
        result = engine.natural_language_to_sql(question)
        
        assert result['success'] is True
        assert 'SELECT' in result['sql'].upper()
        
        # Execute the query
        execution_result = engine.execute_query(result['sql'])
        
        assert execution_result['success'] is True
        assert len(execution_result['data']) > 0
    
    def test_data_pipeline(self, setup_system):
        """Test the data processing pipeline"""
        sample_data = setup_system['sample_data']
        engine = setup_system['engine']
        
        # Verify data was loaded correctly
        result = engine.execute_query("SELECT COUNT(*) as count FROM financial_statements")
        
        assert result['success'] is True
        count = result['data']['count'][0]
        assert count == len(sample_data)
