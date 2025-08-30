import os
import io
import time
from typing import List, Tuple, Optional, Dict
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# LangChain core
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# LLM provider (Now Google via langchain-google-genai)
from langchain_google_genai import ChatGoogleGenerativeAI

# PDF parsing
from pypdf import PdfReader

# -----------------------------
# App Config
# -----------------------------
load_dotenv()
st.set_page_config(page_title="AI College Assistant (RAG)", page_icon="📚", layout="wide")

# Sidebar: Model/Index settings
with st.sidebar:
    st.title("⚙️ Settings")
    st.caption("Tweak these depending on your machine/time")

    EMB_MODEL = st.selectbox(
        "Embedding model",
        ["sentence-transformers/all-MiniLM-L6-v2", "sentence-transformers/all-mpnet-base-v2"],
        index=0,
    )
    CHUNK_SIZE = st.slider("Chunk size", 300, 2000, 800, 50)
    CHUNK_OVERLAP = st.slider("Chunk overlap", 0, 400, 120, 10)
    TOP_K = st.slider("Top-K retrieved chunks", 1, 10, 4)
    TEMPERATURE = st.slider("LLM temperature", 0.0, 1.0, 0.2, 0.1)
    MODEL_NAME = st.selectbox("LLM model", ["gpt-4o-mini", "gpt-4o", "gpt-4o-mini-2024-08-06", "gpt-3.5-turbo"], 0)

    st.divider()
    st.caption("Optional: persist index between runs")
    persist_toggle = st.checkbox("Persist FAISS index (./rag_index)", value=False)
    if persist_toggle:
        index_dir = "./rag_index"
        os.makedirs(index_dir, exist_ok=True)
    else:
        index_dir = None

# -----------------------------
# Helpers
# -----------------------------

def read_pdf(file: io.BytesIO, filename: str) -> List[Document]:
    """Extract text per page from PDF and return as LangChain Documents with metadata."""
    reader = PdfReader(file)
    docs = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            docs.append(Document(page_content=text, metadata={"source": filename, "page": i + 1}))
    return docs

def read_text(file: io.BytesIO, filename: str, encoding: str = "utf-8") -> List[Document]:
    content = file.read().decode(encoding, errors="ignore")
    if content.strip():
        return [Document(page_content=content, metadata={"source": filename, "page": 1})]
    return []

def chunk_documents(docs: List[Document], chunk_size: int, chunk_overlap: int) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)

def build_or_load_vectorstore(chunks: List[Document], emb_model_name: str, persist_dir: Optional[str]) -> FAISS:
    embeddings = HuggingFaceEmbeddings(model_name=emb_model_name)

    if persist_dir and os.path.isdir(persist_dir) and any(
        fname.endswith(".faiss") or fname.endswith(".pkl") for fname in os.listdir(persist_dir)
    ):
        vs = FAISS.load_local(persist_dir, embeddings, allow_dangerous_deserialization=True)
    else:
        vs = FAISS.from_documents(chunks, embeddings)
        if persist_dir:
            vs.save_local(persist_dir)
    return vs

def save_vectorstore(vs: FAISS, persist_dir: str):
    vs.save_local(persist_dir)

def format_sources(docs: List[Document]) -> str:
    seen = []
    for d in docs:
        tag = f"{d.metadata.get('source','?')} p.{d.metadata.get('page','?')}"
        if tag not in seen:
            seen.append(tag)
    return "; ".join(seen)

# -----------------------------
# System Prompts
# -----------------------------

ANSWER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
You are an AI college assistant. Answer the user's question using ONLY the provided context.
- If the answer is not in the context, say you don't have that info.
- Quote important definitions briefly.
- Return a concise, structured answer.
- After the answer, add a 'Sources' line listing file names and pages from the context.
"""),
    ("user", "Question: {question}\n\nContext:\n{context}\n\nReturn your answer."),
])

MCQ_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
Create exam-style MCQs from the provided context. Each MCQ must have:
- A clear question
- 4 options (A–D)
- Correct answer key
- 1-line explanation

Return 5 MCQs in a clean numbered list.
"""),
    ("user", "Generate MCQs on: {topic}\n\nContext:\n{context}"),
])

SUMMARY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Summarize the context into 5 crisp bullet points for quick revision."),
    ("user", "Summarize topic: {topic}\n\nContext:\n{context}"),
])

# -----------------------------
# LLM Init
# -----------------------------

GOOGLE_API_KEY="your-api-key"
if not GOOGLE_API_KEY:
    st.warning("OpenAI API key not set. Set GOOGLE_API_KEY env var to enable answers.")
    
# Use the Gemini model you have access to, e.g., "gemini-1.5-pro-latest" or "gemini-2.5-pro"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=TEMPERATURE)
output_parser = StrOutputParser()

# -----------------------------
# UI Layout
# -----------------------------

st.title("📚 AI College Assistant — RAG")
st.caption("Upload syllabus/notes/past papers. Ask questions. Generate MCQs & summaries. ✨")

col_u, col_idx = st.columns([3, 2], gap="large")

with col_u:
    uploads = st.file_uploader(
        "Upload PDFs or TXTs (you can upload multiple)",
        type=["pdf", "txt"],
        accept_multiple_files=True,
    )
    build_btn = st.button("Build / Update Knowledge Base", type="primary")

with col_idx:
    st.markdown("### 📦 Index Status")
    if persist_toggle and index_dir and os.path.isdir(index_dir):
        existing = [f for f in os.listdir(index_dir) if f.endswith(".faiss") or f.endswith(".pkl")]
        if existing:
            st.success("Found existing FAISS index. You can chat immediately or rebuild.")
        else:
            st.info("No persisted index yet. Upload docs and build.")
    else:
        st.info("In-memory index will be created for this session.")

# Session state holders
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "ingested_docs" not in st.session_state:
    st.session_state.ingested_docs = []  # for display

# -----------------------------
# Build Index
# -----------------------------

if build_btn:
    all_docs: List[Document] = []

    if uploads:
        for up in uploads:
            fname = up.name
            try:
                if fname.lower().endswith(".pdf"):
                    docs = read_pdf(up, fname)
                else:
                    # txt
                    up.seek(0)
                    docs = read_text(up, fname)
                all_docs.extend(docs)
            except Exception as e:
                st.error(f"Failed to read {fname}: {e}")

        if not all_docs:
            st.warning("No readable text found in the uploaded files.")
        else:
            with st.spinner("Chunking and embedding documents…"):
                chunks = chunk_documents(all_docs, CHUNK_SIZE, CHUNK_OVERLAP)
                vs = build_or_load_vectorstore(chunks, EMB_MODEL, index_dir)
                st.session_state.vectorstore = vs
                st.session_state.ingested_docs = [d.metadata for d in chunks[:50]]  # preview

            st.success(f"Knowledge base ready ✅  (chunks: {len(chunks)})")

            if persist_toggle and index_dir:
                save_vectorstore(vs, index_dir)
                st.caption("Index persisted to ./rag_index")
    else:
        # No new uploads; try to load persisted index
        if persist_toggle and index_dir:
            try:
                vs = build_or_load_vectorstore([], EMB_MODEL, index_dir)
                st.session_state.vectorstore = vs
                st.success("Loaded existing index ✅")
            except Exception as e:
                st.error(f"Could not load persisted index: {e}")
        else:
            st.warning("Upload files or enable persistence to load an existing index.")

st.divider()

# -----------------------------
# Tabs: Chat | MCQs | Summaries
# -----------------------------

chat_tab, mcq_tab, sum_tab = st.tabs(["💬 Chat", "📝 MCQs", "🧾 Summaries"])

# -------- Chat Tab --------
with chat_tab:
    st.subheader("Chat with your documents")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_q = st.text_input("Ask a question (e.g., 'Important topics in Unit 3 IoT?')")
    ask_btn = st.button("Ask")

    if ask_btn:
        if not st.session_state.vectorstore:
            st.error("Build the knowledge base first.")
        elif not user_q.strip():
            st.warning("Type a question first.")
        else:
            retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": TOP_K})

            with st.spinner("Retrieving context & thinking…"):
                rel_docs: List[Document] = retriever.get_relevant_documents(user_q)
                context_text = "\n\n".join([d.page_content for d in rel_docs])
                prompt_msgs = ANSWER_PROMPT.format_messages(question=user_q, context=context_text)

                try:
                    response = llm.invoke(prompt_msgs)
                    answer = response.content 
                except Exception as e:
                    answer = f"LLM error: {e}"

                sources = format_sources(rel_docs) if rel_docs else "(no sources)"

            st.session_state.chat_history.append({"q": user_q, "a": answer, "sources": sources})

    # Render history
    for turn in st.session_state.chat_history[::-1]:  # latest first
        with st.container(border=True):
            st.markdown(f"**You:** {turn['q']}")
            st.markdown(f"**Assistant:**\n\n{turn['a']}")
            st.caption(f"Sources: {turn['sources']}")

# -------- MCQ Tab --------
with mcq_tab:
    st.subheader("Generate exam-style MCQs from retrieved context")

    topic = st.text_input("Topic or unit (e.g., 'Hill Cipher', 'Unit 2 MAC Protocols')")
    mcq_btn = st.button("Generate 5 MCQs")

    if mcq_btn:
        if not st.session_state.vectorstore:
            st.error("Build the knowledge base first.")
        elif not topic.strip():
            st.warning("Enter a topic.")
        else:
            retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": TOP_K})

            with st.spinner("Retrieving context & creating MCQs…"):
                rel_docs = retriever.get_relevant_documents(topic)
                context_text = "\n\n".join([d.page_content for d in rel_docs])
                msgs = MCQ_PROMPT.format_messages(topic=topic, context=context_text)

                try:
                    response = llm.invoke(msgs)
                    mcqs = response.content
                except Exception as e:
                    mcqs = f"LLM error: {e}"

                sources = format_sources(rel_docs) if rel_docs else "(no sources)"

            with st.container(border=True):
                st.markdown(mcqs)
                st.caption(f"Sources: {sources}")

# -------- Summaries Tab --------
with sum_tab:
    st.subheader("Quick summaries for revision")

    sum_topic = st.text_input("What do you want summarized? (e.g., 'Unit 3: IoT Protocols')")
    sum_btn = st.button("Make 5-point TL;DR")

    if sum_btn:
        if not st.session_state.vectorstore:
            st.error("Build the knowledge base first.")
        elif not sum_topic.strip():
            st.warning("Enter a topic.")
        else:
            retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": TOP_K})

            with st.spinner("Retrieving context & summarizing…"):
                rel_docs = retriever.get_relevant_documents(sum_topic)
                context_text = "\n\n".join([d.page_content for d in rel_docs])
                msgs = SUMMARY_PROMPT.format_messages(topic=sum_topic, context=context_text)

                try:
                    response = llm.invoke(msgs)
                    tl_dr = response.content
                except Exception as e:
                    tl_dr = f"LLM error: {e}"

                sources = format_sources(rel_docs) if rel_docs else "(no sources)"

            with st.container(border=True):
                st.markdown(tl_dr)
                st.caption(f"Sources: {sources}")

# -----------------------------
# Footer Tips
# -----------------------------

st.divider()
st.markdown(
    """
**Tips for the hackathon**
- Keep uploads small and focused per problem (syllabus + key notes) to improve retrieval quality.
- Tune chunk size/overlap in the sidebar if answers feel out of context.
- Use the MCQ tab to show extra value beyond Q&A (judges love this!).
- If you need CSV/SQL support: parse the data with pandas/SQL, then convert key rows/sections into text docs and add to the index.
- Swap LLM provider by replacing `ChatOpenAI` with your preferred LangChain chat model.
"""
)
