import streamlit as st
import requests

st.set_page_config(page_title="Code-Lens AI", page_icon="🔍")

st.title("🔍 Code-Lens: Agentic Codebase Analyst")
st.markdown("### Powered by Endee Vector DB & Groq Llama 3.3")

# Sidebar for Ingestion Status
with st.sidebar:
    st.header("System Status")
    st.success("Endee DB: Connected")
    st.success("LLM: Llama-3.3-70b Active")
    st.info("Ingested Project: WhatBytes_Django")

# User Input
question = st.text_input("Ask a question about the codebase:", placeholder="e.g., How are the database models structured?")

if st.button("Analyze Codebase"):
    if question:
        with st.spinner("Searching Endee DB and generating expert answer..."):
            try:
                # Direct call to your FastAPI backend
                response = requests.post(
                    "http://127.0.0.1:8000/ask", 
                    json={"question": question}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.markdown("#### 🤖 Senior Agent Response:")
                    st.write(data["answer"])
                    
                    with st.expander("View Sources Used"):
                        st.write(f"Retrieved {data['sources_used']} relevant code chunks from Endee.")
                else:
                    st.error(f"API Error: {response.text}")
            except Exception as e:
                st.error(f"Could not connect to Backend: {e}")
    else:
        st.warning("Please enter a question.")