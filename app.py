# streamlit UI for the Enterprise RAG system
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from src.rbac import authenticate, get_allowed_tags
from src.retriever import retrieve
from src.generator import generate

st.set_page_config(page_title="Enterprise RAG", page_icon="-", layout="wide")

# session state
if "user" not in st.session_state:
    st.session_state.user = None
if "history" not in st.session_state:
    st.session_state.history = []

# login
if st.session_state.user is None:
    st.title("Enterprise RAG — Login")
    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
    if submitted:
        user = authenticate(username, password)
        if user:
            st.session_state.user = {**user, "username": username}
            st.rerun()
        else:
            st.error("Invalid credentials.")

    st.markdown("---")
    st.markdown("**Demo accounts:**")
    demo = {
        "alice / alice123": "HR Manager — HR docs, employee records, compliance",
        "bob / bob123":     "Finance Analyst — Finance reports, budget, compliance",
        "carol / carol123": "IT Admin — IT logs, audit trails, system reports",
        "dave / dave123":   "Executive — All documents",
        "eve / eve123":     "Intern — Public docs only",
    }
    for cred, desc in demo.items():
        st.markdown(f"- `{cred}` → {desc}")
    st.stop()

# main app
user = st.session_state.user

with st.sidebar:
    st.markdown(f"### {user['name']}")
    st.markdown(f"**Role:** `{user['role']}`")
    st.markdown("**Accessible data:**")
    for tag in get_allowed_tags(user["role"]):
        st.markdown(f"- {tag}")
    st.markdown("---")
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.history = []
        st.rerun()
    if st.button("Clear history"):
        st.session_state.history = []
        st.rerun()

st.title("Enterprise RAG Intelligence System")

# chat history
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# input
query = st.chat_input("Ask a question about enterprise data...")
if query:
    st.session_state.history.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving and generating answer..."):
            chunks = retrieve(query, user["role"])
            result = generate(query, chunks)

        st.markdown(result["answer"])

        if result["citations"]:
            with st.expander(f"Sources & Confidence (avg: {result['avg_confidence']})"):
                for c in result["citations"]:
                    st.markdown(f"**[{c['index']}]** `{c['source']}` — confidence: `{c['confidence']}`")

            with st.expander("Retrieved Chunks (Retrieval Trace)"):
                for i, chunk in enumerate(chunks, 1):
                    st.markdown(f"**Chunk {i}** — `{chunk['source']}` ({chunk['type']}) | conf: `{chunk['confidence']}`")
                    st.text(chunk["text"][:400] + ("..." if len(chunk["text"]) > 400 else ""))

        st.session_state.history.append({"role": "assistant", "content": result["answer"]})
