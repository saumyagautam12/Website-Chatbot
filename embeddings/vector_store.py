import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter 


from langchain_community.vectorstores import FAISS

import os
from dotenv import load_dotenv
import logging

from utils.logger import setup_logger

logger = setup_logger("chunker")

load_dotenv() 

embedding_model_name= os.getenv("embedding_model_name")
llm_model=os.getenv("llm_model")
embeddings_path=os.getenv('faiss_path')
collection_name=os.getenv('collection_name')




class VectorStoreManager:
    def __init__(
        self,
        persist_directory: str = embeddings_path,
        embedding_model_name: str = embedding_model_name,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ):
        self.persist_directory = persist_directory
        self.collection_name=collection_name,

        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model_name
        )

        

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def _create_chunks(self, text: str, metadata: dict):
        """
        Splits extracted text into LangChain Documents with metadata.
        """

        
        documents = self.text_splitter.create_documents(
            texts=[text],
            metadatas=[metadata]
        )
        return documents

    def create_or_load_vectorstore(self, text: str, metadata: dict):
        """
        Creates embeddings from text chunks and stores them in Faiss.
        """
        # os.makedirs(self.persist_directory, exist_ok=True)
        logger.info("Starting text chunking")

        docs = self._create_chunks(text, metadata)
        # print(documents)

        logger.info(f"Chunking completed | Total chunks created: {len(docs)}")

        if len(docs) == 0:
            logger.error("No chunks created — check input text")

        vectorstore = FAISS.from_documents(docs,self.embeddings)
        vectorstore.save_local(self.persist_directory)

        logger.info(
            f"Vectorstore saved | Path: {self.persist_directory}")
            # f"Total vectors: {vectorstore.index.ntotal}"
        

        return vectorstore
