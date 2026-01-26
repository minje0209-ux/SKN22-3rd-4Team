"""
Vector store for document embeddings and similarity search
"""
import logging
from pathlib import Path
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

logger = logging.getLogger(__name__)


class VectorStore:
    """Manages vector embeddings for financial documents"""
    
    def __init__(
        self,
        persist_directory: Path,
        collection_name: str = "financial_documents",
        embedding_model: str = "text-embedding-3-small",
        api_key: Optional[str] = None
    ):
        """
        Initialize vector store
        
        Args:
            persist_directory: Directory to persist the vector database
            collection_name: Name of the collection
            embedding_model: Model for generating embeddings
            api_key: OpenAI API key
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(persist_directory),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=embedding_model,
            openai_api_key=api_key
        )
        
        logger.info(f"Initialized vector store with collection: {collection_name}")
    
    def add_documents(
        self,
        documents: List[Dict],
        batch_size: int = 100
    ) -> int:
        """
        Add documents to the vector store
        
        Args:
            documents: List of document dictionaries with 'text' and 'metadata'
            batch_size: Number of documents to process at once
            
        Returns:
            Number of documents added
        """
        total_added = 0
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            texts = [doc.get("text", "") for doc in batch]
            metadatas = [doc.get("metadata", {}) for doc in batch]
            ids = [doc.get("id", f"doc_{i + j}") for j, doc in enumerate(batch)]
            
            try:
                # Generate embeddings
                embeddings = self.embeddings.embed_documents(texts)
                
                # Add to collection
                self.collection.add(
                    embeddings=embeddings,
                    documents=texts,
                    metadatas=metadatas,
                    ids=ids
                )
                
                total_added += len(batch)
                logger.info(f"Added batch {i // batch_size + 1}, total: {total_added}")
                
            except Exception as e:
                logger.error(f"Error adding batch {i // batch_size + 1}: {str(e)}")
        
        logger.info(f"Total documents added: {total_added}")
        return total_added
    
    def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar documents
        
        Args:
            query: Search query
            k: Number of results to return
            filter_dict: Optional metadata filters
            
        Returns:
            List of similar documents with scores
        """
        try:
            # Generate query embedding
            query_embedding = self.embeddings.embed_query(query)
            
            # Search
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                where=filter_dict
            )
            
            # Format results
            documents = []
            for i in range(len(results['ids'][0])):
                documents.append({
                    "id": results['ids'][0][i],
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i]
                })
            
            return documents
            
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            return []
    
    def search_by_company(
        self,
        query: str,
        company: str,
        k: int = 5
    ) -> List[Dict]:
        """
        Search for documents related to a specific company
        
        Args:
            query: Search query
            company: Company ticker or name
            k: Number of results
            
        Returns:
            List of relevant documents
        """
        filter_dict = {"ticker": company}
        return self.similarity_search(query, k, filter_dict)
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection"""
        count = self.collection.count()
        
        return {
            "collection_name": self.collection_name,
            "total_documents": count,
            "persist_directory": str(self.persist_directory)
        }
    
    def delete_collection(self):
        """Delete the entire collection"""
        try:
            self.client.delete_collection(self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection: {str(e)}")
