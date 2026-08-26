# app.py
import streamlit as st
import requests
import os

# The URL of your FastAPI backend
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RAG Document Intelligence", layout="wide")
st.title("RAG Document Intelligence Platform")
st.write("Upload a PDF and ask natural language questions about it!")

# --- Upload Section ---
st.header("1. Upload Document")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Send the file to the FastAPI backend
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
    
    with st.spinner("Processing and indexing document..."):
        response = requests.post(f"{API_URL}/upload", files=files)
        
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error(f"Upload failed: {response.text}")

st.divider()

# --- Query Section ---
st.header("2. Ask a Question")
question = st.text_input("What would you like to know?", placeholder="e.g., What is the difference between break and continue?")

if st.button("Get Answer"):
    if question:
        with st.spinner("Thinking..."):
            # Send the question to the FastAPI backend
            payload = {"question": question, "top_k": 3}
            response = requests.post(f"{API_URL}/query", json=payload)
            
        if response.status_code == 200:
            data = response.json()
            
            # Display the AI Answer
            st.subheader("Answer:")
            st.write(data["answer"])
            
            # Display the Sources
            st.subheader("Sources Used:")
            for source in data["sources"]:
                st.markdown(f"**Page {source['page']}**: {source['snippet']}")
        else:
            st.error(f"Query failed: {response.text}")
    else:
        st.warning("Please enter a question first.")