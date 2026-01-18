from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from langchain_core.messages import AIMessage, HumanMessage

import os
from dotenv import load_dotenv
import logging
from utils.logger import setup_logger
import time

logger = setup_logger()

load_dotenv() 

embedding_model_name= os.getenv("embedding_model_name")
llm_model=os.getenv("llm_model")
embeddings_path=os.getenv('faiss_path')

class WebsiteChatbot:

    def __init__(
        self,
        embedding_model_name=embedding_model_name,
        faiss_path=embeddings_path,
        llm_model=llm_model
    ):
        print("Initializing chatbot...")

        # Embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model_name
        )

        # Load FAISS ONCE
        self.vectorstore = FAISS.load_local(
            faiss_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )

        self.llm = ChatOllama(
            model=llm_model,
            temperature=0
        )

        
        self.chat_history = []

        logger.info("Initializing chatbot")

        logger.info("Loading FAISS index")

        # print("Chatbot ready.")

    def ask_question(self, question: str) -> str:
        print("➡️ Question received:", question)

        logger.info(f"User query received: {question}")

        print(self.vectorstore)
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})

        print(retriever)

        
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are a helpful AI assistant which assists user with the content loaded from the website.
                    Answer the user's question concisely using ONLY the provided context .
                    You may use the conversation history for understanding references.
                    Do not add external information.
                    
                    If the context is irrelevant or missing, politely answer 'The answer is not available on the provided website.'
                    """
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            (
                "system",
                "<context>\n{context}\n</context>"
            ),
            (
                "human",
                "{input}"
            )
        ])


        # Chains (built ONCE)
        combine_docs_chain = create_stuff_documents_chain(
            self.llm, prompt
        )

        rag_chain = create_retrieval_chain(
            retriever,
            combine_docs_chain
        )
        result = rag_chain.invoke({
            "input": question,
            "chat_history": self.chat_history
        })

        logger.info(f"Retrieved {len(result['context'])} documents")

        answer = result["answer"]

        # Update memory
        self.chat_history.extend([
            HumanMessage(content=question),
            AIMessage(content=answer),
        ])
        return answer

        
        
