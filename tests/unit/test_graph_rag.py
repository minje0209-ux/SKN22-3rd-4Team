"""
Test suite for GraphRAG module
"""
import pytest
from src.rag.graph_rag import GraphRAG


class TestGraphRAG:
    """Test cases for GraphRAG"""
    
    @pytest.fixture
    def graph_rag(self):
        """Create a GraphRAG instance for testing"""
        return GraphRAG(
            embedding_model="text-embedding-3-small",
            llm_model="gpt-4-turbo-preview"
        )
    
    def test_initialization(self, graph_rag):
        """Test GraphRAG initialization"""
        assert graph_rag is not None
        assert graph_rag.graph is not None
    
    def test_extract_entities_and_relationships(self, graph_rag):
        """Test entity and relationship extraction"""
        text = "Apple Inc. partners with Qualcomm for chipset supply."
        result = graph_rag.extract_entities_and_relationships(text, "AAPL")
        
        assert "entities" in result
        assert "relationships" in result
    
    def test_build_knowledge_graph(self, graph_rag):
        """Test knowledge graph building"""
        documents = [
            {
                "text_content": "Apple Inc. announced partnership with Samsung.",
                "ticker": "AAPL"
            }
        ]
        
        graph = graph_rag.build_knowledge_graph(documents)
        assert graph is not None
        
    def test_query_graph(self, graph_rag):
        """Test graph querying"""
        # Build a simple graph first
        documents = [
            {
                "text_content": "Microsoft partners with OpenAI.",
                "ticker": "MSFT"
            }
        ]
        graph_rag.build_knowledge_graph(documents)
        
        result = graph_rag.query_graph("Tell me about Microsoft's partnerships")
        
        assert "query" in result
        assert "response" in result
