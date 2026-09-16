from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import streamlit as st
from text_splitter import create_chunks

@st.cache_resource
def create_vector_store(video_id :str):
    chunks = create_chunks(video_id)

    if not chunks:
        return None
  
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

    vectorstore = FAISS.from_documents(chunks,embeddings)

    return vectorstore

