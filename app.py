import streamlit as st

from crawler.webloader import WebsiteLoader
from embeddings.vector_store import VectorStoreManager
from qa.web_chatbot import WebsiteChatbot


st.set_page_config(page_title="Website Chatbot", layout="centered")

st.title("Website-based AI Chatbot")

# -----------------------------
# Session state
# -----------------------------
if "indexed" not in st.session_state:
    st.session_state.indexed = False

if "chatbot" not in st.session_state:
    st.session_state.chatbot = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# URL Indexing Section
# -----------------------------
st.subheader("Index a Website")

url = st.text_input("Enter website URL")

if st.button("Index Website"):
    if not url.strip():
        st.error("Please enter a valid URL.")
    else:
        try:
            with st.spinner("Crawling and indexing website..."):
                loader = WebsiteLoader()
                data = loader.load(url)

                store = VectorStoreManager()
                store.create_or_load_vectorstore(
                    text=data["text"],
                    metadata=data["metadata"]
                )

                print('data indexed')

                st.session_state.chatbot = WebsiteChatbot()
                st.session_state.indexed = True
                st.session_state.messages = []

            st.success("Website indexed successfully!")

        except Exception as e:
            st.error(str(e))


# -----------------------------
# Chat Section
# -----------------------------
if st.session_state.indexed:
    st.subheader(" Ask Questions")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask a question about the website")

    if user_input:
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = st.session_state.chatbot.ask_question(user_input)
                st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
else:
    st.info("Please index a website to start chatting.")
