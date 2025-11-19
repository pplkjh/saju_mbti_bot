"""
Vector store service using FAISS for document retrieval
"""
import os
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)


class VectorStoreService:
    """FAISS 벡터 스토어 서비스"""

    def __init__(self, vector_store_path: str = "data/vector_store"):
        self.vector_store_path = vector_store_path
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore: Optional[FAISS] = None

    def load(self) -> bool:
        """벡터 스토어 로드"""
        try:
            if os.path.exists(self.vector_store_path):
                self.vectorstore = FAISS.load_local(
                    self.vector_store_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info(f"✅ Vector store loaded from {self.vector_store_path}")
                return True
            else:
                logger.warning(f"⚠️ Vector store not found at {self.vector_store_path}")
                return False
        except Exception as e:
            logger.error(f"❌ Failed to load vector store: {e}")
            return False

    def search(self, query: str, k: int = 3) -> List[str]:
        """유사 문서 검색"""
        if not self.vectorstore:
            logger.warning("Vector store not loaded")
            return []

        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            return [doc.page_content for doc in docs]
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []

    def is_loaded(self) -> bool:
        """벡터 스토어 로드 상태 확인"""
        return self.vectorstore is not None


# 싱글톤 인스턴스
vector_store_service = VectorStoreService()
