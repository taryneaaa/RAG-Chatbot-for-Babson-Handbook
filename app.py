import os

from dotenv import load_dotenv
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI
import streamlit as st

load_dotenv()

DATA_DIR = "data"

Settings.llm = GoogleGenAI(
    model="gemini-3.5-flash-lite", api_key=os.getenv("GEMINI_API_KEY")
)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")


@st.cache_resource
def get_query_engine():
    """Load the handbook, build a vector index, and return a query engine."""
    if not os.getenv("GEMINI_API_KEY"):
        st.error("GEMINI_API_KEY not found. Add it to your .env file.")
        st.stop()
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine()


st.title("Babson Handbook Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about the Babson student handbook"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    query_engine = get_query_engine()
    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching the handbook..."):
                response = query_engine.query(prompt)
            answer = response.response
        except Exception as error:
            answer = f"Sorry, Gemini returned an error. Please try again in a minute.\n\n{error}"
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
