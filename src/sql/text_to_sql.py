"""
Text-to-SQL engine for querying financial data
Converts natural language questions to SQL queries
"""
import logging
from typing import Dict, List, Optional
import duckdb
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from sqlalchemy import create_engine, MetaData, Table, Column, String, Float, Integer, Date

logger = logging.getLogger(__name__)


class TextToSQL:
    """
    Converts natural language questions to SQL queries
    for financial data analysis
    """
    
    def __init__(
        self,
        database_url: str = "duckdb:///:memory:",
        llm_model: str = "gpt-4-turbo-preview",
        api_key: Optional[str] = None
    ):
        """
        Initialize Text-to-SQL engine
        
        Args:
            database_url: Database connection string
            llm_model: LLM model for SQL generation
            api_key: OpenAI API key
        """
        self.database_url = database_url
        self.llm = ChatOpenAI(
            model=llm_model,
            temperature=0,
            openai_api_key=api_key
        )
        
        # Initialize database connection
        if "duckdb" in database_url:
            self.conn = duckdb.connect(database=":memory:")
        else:
            self.engine = create_engine(database_url)
        
        self.schema_info = None
        
    def create_financial_tables(self):
        """Create standard financial tables"""
        
        # Financial Statements table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS financial_statements (
                id INTEGER PRIMARY KEY,
                ticker VARCHAR,
                company_name VARCHAR,
                filing_date DATE,
                period_end_date DATE,
                fiscal_year INTEGER,
                fiscal_quarter INTEGER,
                form_type VARCHAR,
                revenue DECIMAL(18, 2),
                cost_of_revenue DECIMAL(18, 2),
                gross_profit DECIMAL(18, 2),
                operating_expenses DECIMAL(18, 2),
                operating_income DECIMAL(18, 2),
                net_income DECIMAL(18, 2),
                eps DECIMAL(10, 4),
                total_assets DECIMAL(18, 2),
                total_liabilities DECIMAL(18, 2),
                shareholders_equity DECIMAL(18, 2),
                cash_and_equivalents DECIMAL(18, 2),
                total_debt DECIMAL(18, 2),
                operating_cash_flow DECIMAL(18, 2),
                investing_cash_flow DECIMAL(18, 2),
                financing_cash_flow DECIMAL(18, 2)
            )
        """)
        
        # Company Info table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                ticker VARCHAR PRIMARY KEY,
                company_name VARCHAR,
                cik VARCHAR,
                sic_code VARCHAR,
                industry VARCHAR,
                sector VARCHAR,
                market_cap DECIMAL(18, 2),
                employees INTEGER
            )
        """)
        
        # Financial Ratios table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS financial_ratios (
                id INTEGER PRIMARY KEY,
                ticker VARCHAR,
                period_end_date DATE,
                pe_ratio DECIMAL(10, 2),
                pb_ratio DECIMAL(10, 2),
                debt_to_equity DECIMAL(10, 2),
                current_ratio DECIMAL(10, 2),
                quick_ratio DECIMAL(10, 2),
                roe DECIMAL(10, 4),
                roa DECIMAL(10, 4),
                profit_margin DECIMAL(10, 4),
                operating_margin DECIMAL(10, 4),
                asset_turnover DECIMAL(10, 4)
            )
        """)
        
        logger.info("Created financial tables")
        self._update_schema_info()
    
    def _update_schema_info(self):
        """Update schema information for the LLM"""
        try:
            tables_info = self.conn.execute("""
                SELECT table_name, column_name, data_type 
                FROM information_schema.columns 
                WHERE table_schema = 'main'
                ORDER BY table_name, ordinal_position
            """).fetchdf()
            
            schema_text = "Database Schema:\n\n"
            
            for table in tables_info['table_name'].unique():
                schema_text += f"Table: {table}\n"
                table_cols = tables_info[tables_info['table_name'] == table]
                
                for _, row in table_cols.iterrows():
                    schema_text += f"  - {row['column_name']}: {row['data_type']}\n"
                
                schema_text += "\n"
            
            self.schema_info = schema_text
            
        except Exception as e:
            logger.error(f"Error updating schema info: {str(e)}")
            self.schema_info = "Schema information not available"
    
    def natural_language_to_sql(self, question: str) -> Dict:
        """
        Convert natural language question to SQL
        
        Args:
            question: Natural language question
            
        Returns:
            Dictionary with SQL query and explanation
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert SQL developer specializing in financial data analysis.
            Convert the user's natural language question into a valid SQL query.
            
            {schema}
            
            Guidelines:
            - Use proper SQL syntax for DuckDB
            - Include appropriate JOINs when querying multiple tables
            - Use aggregate functions when needed (SUM, AVG, COUNT, etc.)
            - Add appropriate WHERE clauses for filtering
            - Include ORDER BY and LIMIT when relevant
            - Calculate financial ratios when asked
            - Handle date ranges appropriately
            
            Return ONLY the SQL query without any explanation or markdown formatting.
            """),
            ("user", "{question}")
        ])
        
        try:
            chain = prompt | self.llm
            response = chain.invoke({
                "schema": self.schema_info or "Schema not available",
                "question": question
            })
            
            sql_query = response.content.strip()
            
            # Clean up the SQL (remove markdown code blocks if present)
            if sql_query.startswith("```"):
                sql_query = sql_query.split("```")[1]
                if sql_query.startswith("sql"):
                    sql_query = sql_query[3:]
                sql_query = sql_query.strip()
            
            return {
                "question": question,
                "sql": sql_query,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error generating SQL: {str(e)}")
            return {
                "question": question,
                "sql": None,
                "success": False,
                "error": str(e)
            }
    
    def execute_query(self, sql: str) -> Dict:
        """
        Execute SQL query and return results
        
        Args:
            sql: SQL query to execute
            
        Returns:
            Dictionary with results and metadata
        """
        try:
            result_df = self.conn.execute(sql).fetchdf()
            
            return {
                "success": True,
                "data": result_df,
                "row_count": len(result_df),
                "columns": list(result_df.columns)
            }
            
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def query_with_natural_language(self, question: str) -> Dict:
        """
        Complete pipeline: NL question -> SQL -> Results
        
        Args:
            question: Natural language question
            
        Returns:
            Dictionary with query results and metadata
        """
        # Generate SQL
        sql_result = self.natural_language_to_sql(question)
        
        if not sql_result["success"]:
            return sql_result
        
        # Execute query
        execution_result = self.execute_query(sql_result["sql"])
        
        return {
            "question": question,
            "sql": sql_result["sql"],
            "success": execution_result["success"],
            "data": execution_result.get("data"),
            "row_count": execution_result.get("row_count"),
            "error": execution_result.get("error")
        }
    
    def load_data_from_dataframe(
        self,
        df: pd.DataFrame,
        table_name: str
    ):
        """
        Load data from pandas DataFrame into database
        
        Args:
            df: DataFrame to load
            table_name: Name of the table
        """
        try:
            self.conn.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
            logger.info(f"Loaded {len(df)} rows into {table_name}")
            self._update_schema_info()
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
    
    def get_sample_questions(self) -> List[str]:
        """Get sample questions for the UI"""
        return [
            "What is the total revenue for Apple in 2023?",
            "Compare the net income of Microsoft and Google in the last 3 years",
            "Which companies have the highest profit margin?",
            "Show me the debt-to-equity ratio for all tech companies",
            "What is the average P/E ratio in the technology sector?",
            "Find companies with revenue growth greater than 20% year-over-year",
            "Calculate the operating cash flow trend for Tesla",
            "Which companies have the strongest balance sheets?"
        ]
