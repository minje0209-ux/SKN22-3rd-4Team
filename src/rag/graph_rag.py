"""
GraphRAG implementation for analyzing relationships between companies
"""
import logging
from typing import List, Dict, Optional, Tuple
import networkx as nx
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)


class GraphRAG:
    """
    Graph-based Retrieval Augmented Generation
    Builds and queries knowledge graphs from financial documents
    """
    
    def __init__(
        self,
        embedding_model: str = "text-embedding-3-small",
        llm_model: str = "gpt-4-turbo-preview",
        api_key: Optional[str] = None
    ):
        """
        Initialize GraphRAG
        
        Args:
            embedding_model: Model for generating embeddings
            llm_model: LLM model for generating responses
            api_key: OpenAI API key
        """
        self.embeddings = OpenAIEmbeddings(
            model=embedding_model,
            openai_api_key=api_key
        )
        self.llm = ChatOpenAI(
            model=llm_model,
            temperature=0.1,
            openai_api_key=api_key
        )
        self.graph = nx.DiGraph()
        
    def extract_entities_and_relationships(
        self,
        text: str,
        company_context: Optional[str] = None
    ) -> Dict:
        """
        Extract entities (companies, products, people) and relationships from text
        
        Args:
            text: Input text to analyze
            company_context: Optional context about the company
            
        Returns:
            Dictionary with entities and relationships
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert financial analyst. Extract entities and relationships from financial documents.
            
            Entities to extract:
            - Companies (and their tickers)
            - Products/Services
            - People (executives, board members)
            - Locations
            - Financial metrics
            
            Relationships to identify:
            - Partnerships
            - Acquisitions
            - Supplier/Customer relationships
            - Competitor relationships
            - Investment relationships
            
            Return the result in JSON format with lists of entities and relationships.
            """),
            ("user", "Company Context: {context}\n\nText to analyze:\n{text}")
        ])
        
        try:
            chain = prompt | self.llm
            response = chain.invoke({
                "context": company_context or "General analysis",
                "text": text
            })
            
            # Parse the response and structure it
            # This is simplified - in production, use structured output
            return {
                "entities": [],
                "relationships": [],
                "raw_response": response.content
            }
            
        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
            return {"entities": [], "relationships": []}
    
    def build_knowledge_graph(
        self,
        documents: List[Dict],
        chunk_size: int = 1000
    ) -> nx.DiGraph:
        """
        Build a knowledge graph from documents
        
        Args:
            documents: List of document dictionaries with text content
            chunk_size: Size of text chunks for processing
            
        Returns:
            NetworkX directed graph
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=200
        )
        
        for doc in documents:
            text = doc.get("text_content", "")
            company = doc.get("ticker", "UNKNOWN")
            
            # Split into chunks
            chunks = text_splitter.split_text(text)
            
            for chunk in chunks:
                # Extract entities and relationships
                result = self.extract_entities_and_relationships(
                    chunk,
                    company_context=company
                )
                
                # Add to graph
                self._add_to_graph(result, source_doc=doc)
        
        logger.info(f"Built graph with {self.graph.number_of_nodes()} nodes "
                   f"and {self.graph.number_of_edges()} edges")
        
        return self.graph
    
    def _add_to_graph(self, extraction_result: Dict, source_doc: Dict):
        """Add extracted entities and relationships to the graph"""
        # Add entities as nodes
        for entity in extraction_result.get("entities", []):
            entity_id = entity.get("id") or entity.get("name")
            if entity_id:
                self.graph.add_node(
                    entity_id,
                    type=entity.get("type"),
                    metadata=entity.get("metadata", {}),
                    source=source_doc.get("file_path")
                )
        
        # Add relationships as edges
        for rel in extraction_result.get("relationships", []):
            source = rel.get("source")
            target = rel.get("target")
            rel_type = rel.get("type")
            
            if source and target:
                self.graph.add_edge(
                    source,
                    target,
                    type=rel_type,
                    weight=rel.get("confidence", 1.0),
                    metadata=rel.get("metadata", {})
                )
    
    def query_graph(
        self,
        query: str,
        max_depth: int = 3,
        top_k: int = 5
    ) -> Dict:
        """
        Query the knowledge graph
        
        Args:
            query: Natural language query
            max_depth: Maximum depth for graph traversal
            top_k: Number of top results to return
            
        Returns:
            Query results with relevant subgraph
        """
        # Generate embedding for query
        query_embedding = self.embeddings.embed_query(query)
        
        # Find relevant nodes (simplified)
        relevant_nodes = self._find_relevant_nodes(query, top_k)
        
        # Extract subgraph
        subgraph = self._extract_subgraph(relevant_nodes, max_depth)
        
        # Generate response using LLM
        response = self._generate_graph_response(query, subgraph)
        
        return {
            "query": query,
            "response": response,
            "relevant_nodes": relevant_nodes,
            "subgraph": subgraph
        }
    
    def _find_relevant_nodes(self, query: str, top_k: int) -> List[str]:
        """Find nodes most relevant to the query"""
        # Simplified - would use embeddings and similarity search
        return list(self.graph.nodes())[:top_k]
    
    def _extract_subgraph(
        self,
        nodes: List[str],
        max_depth: int
    ) -> nx.DiGraph:
        """Extract a subgraph around the given nodes"""
        subgraph_nodes = set(nodes)
        
        for node in nodes:
            # Get neighbors up to max_depth
            try:
                neighbors = nx.single_source_shortest_path_length(
                    self.graph,
                    node,
                    cutoff=max_depth
                )
                subgraph_nodes.update(neighbors.keys())
            except nx.NodeNotFound:
                continue
        
        return self.graph.subgraph(subgraph_nodes).copy()
    
    def _generate_graph_response(
        self,
        query: str,
        subgraph: nx.DiGraph
    ) -> str:
        """Generate a response based on the query and subgraph"""
        # Convert subgraph to text description
        graph_context = self._subgraph_to_text(subgraph)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a financial analyst assistant. Answer the question based on the knowledge graph context provided.
            Be specific and cite relationships and entities from the graph.
            """),
            ("user", "Graph Context:\n{context}\n\nQuestion: {query}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "context": graph_context,
            "query": query
        })
        
        return response.content
    
    def _subgraph_to_text(self, subgraph: nx.DiGraph) -> str:
        """Convert subgraph to text description"""
        descriptions = []
        
        # Describe nodes
        for node in subgraph.nodes(data=True):
            node_id, data = node
            node_type = data.get("type", "Entity")
            descriptions.append(f"{node_type}: {node_id}")
        
        # Describe edges
        for edge in subgraph.edges(data=True):
            source, target, data = edge
            rel_type = data.get("type", "related to")
            descriptions.append(f"{source} {rel_type} {target}")
        
        return "\n".join(descriptions)
    
    def analyze_company_relationships(
        self,
        company: str,
        relationship_types: Optional[List[str]] = None
    ) -> Dict:
        """
        Analyze relationships for a specific company
        
        Args:
            company: Company ticker or name
            relationship_types: Types of relationships to analyze
            
        Returns:
            Analysis results
        """
        if company not in self.graph:
            return {"error": f"Company {company} not found in graph"}
        
        # Get all relationships
        relationships = {
            "outgoing": list(self.graph.successors(company)),
            "incoming": list(self.graph.predecessors(company))
        }
        
        # Calculate centrality metrics
        centrality = {
            "degree": nx.degree_centrality(self.graph).get(company, 0),
            "betweenness": nx.betweenness_centrality(self.graph).get(company, 0),
            "pagerank": nx.pagerank(self.graph).get(company, 0)
        }
        
        return {
            "company": company,
            "relationships": relationships,
            "centrality": centrality,
            "total_connections": len(relationships["outgoing"]) + len(relationships["incoming"])
        }
