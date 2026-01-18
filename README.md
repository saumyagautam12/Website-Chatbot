# Website-Chatbot
This project implements a website-based AI chatbot that answers user questions strictly using the content of a given website URL.

It follows a Retrieval-Augmented Generation (RAG) approach, runs fully locally using open-source models, and maintains short-term conversational memory limited to the current session.

Architecture Explanation

    Website Extraction – Extracts clean text from a given URL.

    Chunking – Splits text into overlapping semantic chunks.

    Embedding & Storage – Converts chunks into embeddings and stores them in a vector database.

    Retrieval – Retrieves the most relevant chunks for each query.

    Answer Generation – Uses an LLM to generate grounded answers using retrieved context and session memory.

    UI – A Streamlit interface to index websites and ask questions.

Frameworks Used

    LangChain (v0.3.25) – Used for chunking, retrieval chains, and conversational memory.

    Streamlit – Used for the user interface.

    FAISS – Used as the vector database.

    Ollama – Used to run open-source LLMs locally.

    (LangGraph was not required for this linear RAG workflow.)

LLM Model Used & Why

    Model: llama3.2:1b (via Ollama)

    Reason: Lightweight, fully open-source, runs locally on CPU, and suitable for low-latency demos.

Vector Database Used & Why

    Database: FAISS

    Reason: Fast similarity search, lightweight, open-source, and ideal for local vector storage.

Embedding Strategy

    Model: sentence-transformers/all-MiniLM-L6-v2

    Website text is split into chunks (~500 characters with overlap), embedded into dense vectors, and stored in FAISS for similarity-based retrieval.


Setup & Run Instructions

Install dependencies:

pip install -r requirements.txt


Pull the LLM model:

ollama pull llama3.2:1b


Run the application:

streamlit run app.py
Enter a website URL, index it, and start chatting.



Assumptions, Limitations & Future Improvements
Assumptions

Website content is publicly accessible and text-heavy. Dataset size is moderate.

Limitations


    No long-term or cross-session memory.

    The crawler primarily supports static HTML pages and may not fully extract content from JavaScript-heavy websites.

    The system runs fully locally, and performance is constrained by available CPU and memory resources.

Future Improvements


    Multi-page crawling with depth control.

    Model and embedding selection via UI.

    Chat history optimization to reduce context provided to the llm at the time of response generation

This solution demonstrates a clean, modular, and fully local RAG-based chatbot aligned with assignment requirements and best practices.