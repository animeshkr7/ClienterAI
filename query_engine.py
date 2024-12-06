# query_engine.py
import chromadb
from llama_index.core import Settings, VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.gemini import Gemini
from typing import Dict, Any, Optional, Tuple
from config import Config
from query_templates import QueryTemplates
from llama_index.embeddings.gemini import GeminiEmbedding

from llama_index.embeddings.huggingface import HuggingFaceEmbedding



class SalesDataQueryEngine:
    def __init__(self):
        """Initialize query engine for existing ChromaDB"""
        self.persist_dir = Config.PERSIST_DIR
        self.collection_name = Config.COLLECTION_NAME
        
        # Initialize Gemini LLM
        self.llm = Gemini(
            model=Config.MODEL_NAME,
            api_key=Config.GEMINI_API_KEY
        )
        
        # Initialize embedding model
        self.embed_model = GeminiEmbedding(
            model_name="models/embedding-001",
            api_key="AIzaSyCsQn7Tj9WydJ_gOco5JIofPn4LhzUUzyU",
            title="this is a document"
        )
        # Set the models in global settings
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        
        # Set up the query engine
        self.query_engine = self._setup_query_engine()

    def _setup_query_engine(self):
        """Set up the query engine from existing ChromaDB"""
        try:
            db = chromadb.PersistentClient(path=self.persist_dir)
            collection = db.get_collection(name=self.collection_name)
            vector_store = ChromaVectorStore(chroma_collection=collection)
            index = VectorStoreIndex.from_vector_store(
                vector_store,
                embed_model=self.embed_model
            )
            
            return index.as_query_engine(
                similarity_top_k=10000,
                response_mode="compact",
                llm=self.llm
            )
        except Exception as e:
            print(f"Error setting up query engine: {str(e)}")
            raise

    def _get_query_type(self, user_query: str) -> Tuple[str, dict]:
        """Classify the query type and extract parameters"""
        prompt = f"""
        Analyze this query: "{user_query}"
        
        Categorize it into one of these types:
        1. yearly_orders - Questions about orders per year
        2. top_customer_by_orders - Questions about customers with most orders
        3. top_5_customers_by_sales - Questions about top customers by sales
        4. product_line_sales - Questions about product line performance
        5. country_sales_distribution - Questions about sales across countries
        6. order_status_counts - Questions about order statuses
        7. monthly_orders - Questions about orders per month
        8. customers_by_country - Questions about customer distribution
        
        Return only the category name and any specific parameters (like year) needed.
        Format: category_name|param1=value1,param2=value2
        Example: monthly_orders|year=2023
        """
        
        response = self.llm.complete(prompt)
        result = response.text.strip()
        
        parts = result.split('|')
        query_type = parts[0].strip()
        
        params = {}
        if len(parts) > 1:
            param_pairs = parts[1].split(',')
            for pair in param_pairs:
                if '=' in pair:
                    key, value = pair.split('=')
                    params[key.strip()] = value.strip()
        
        return query_type, params

    def _get_analytical_query(self, query_type: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Get the structured query based on query type"""
        template = QueryTemplates.TEMPLATES.get(query_type)
        if template and params:
            return template.format(**params)
        return template or "Invalid query type"

    def query(self, user_query: str) -> str:
        """Process and execute a user query"""
        try:
            query_type, params = self._get_query_type(user_query)
            structured_query = self._get_analytical_query(query_type, params)
            response = self.query_engine.query(structured_query)
            return response.response
        except Exception as e:
            return f"Error processing query: {str(e)}"