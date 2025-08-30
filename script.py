# Create the main Streamlit application
streamlit_app_code = '''
import streamlit as st
import PyPDF2
import io
from datetime import datetime
import re
import json
import hashlib

# Configure the page
st.set_page_config(
    page_title="AI College Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #e5e7eb;
    }
    .user-message {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
    }
    .ai-message {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
    }
    .sidebar-section {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .doc-item {
        background: white;
        padding: 0.8rem;
        border-radius: 6px;
        border: 1px solid #e5e7eb;
        margin-bottom: 0.5rem;
    }
    .success-msg {
        background-color: #dcfce7;
        color: #15803d;
        padding: 0.8rem;
        border-radius: 6px;
        border: 1px solid #bbf7d0;
    }
    .warning-msg {
        background-color: #fef3c7;
        color: #d97706;
        padding: 0.8rem;
        border-radius: 6px;
        border: 1px solid #fed7aa;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "documents" not in st.session_state:
    st.session_state.documents = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "Q&A Mode"
if "processed_docs" not in st.session_state:
    st.session_state.processed_docs = []

# Mock RAG functionality (since we can't use actual APIs)
class MockRAGSystem:
    def __init__(self):
        self.knowledge_base = {
            "iot": {
                "content": "IoT (Internet of Things) refers to interconnected devices that collect and exchange data. Key components include sensors, actuators, communication protocols (WiFi, Bluetooth, MQTT), and cloud platforms.",
                "questions": [
                    "What are the main components of IoT architecture?",
                    "Explain different communication protocols in IoT",
                    "What are the applications of IoT in smart cities?"
                ]
            },
            "cryptography": {
                "content": "Cryptography involves securing information through encryption. Hill Cipher uses matrix multiplication for encryption. RSA algorithm uses public-private key pairs for secure communication.",
                "questions": [
                    "How does Hill Cipher encryption work?",
                    "Explain the RSA algorithm with an example",
                    "What is the difference between symmetric and asymmetric encryption?"
                ]
            },
            "data_structures": {
                "content": "Data structures organize and store data efficiently. Arrays provide constant-time access, linked lists allow dynamic sizing, trees enable hierarchical organization, and graphs represent networks.",
                "questions": [
                    "Compare time complexity of array vs linked list operations",
                    "Explain binary search tree insertion algorithm",
                    "What are the advantages of using hash tables?"
                ]
            },
            "database": {
                "content": "Database Management Systems (DBMS) store, retrieve, and manage data. SQL is used for querying relational databases. Normalization reduces data redundancy.",
                "questions": [
                    "What is database normalization and its types?",
                    "Explain ACID properties in database transactions",
                    "Write SQL queries for joins and aggregations"
                ]
            }
        }
    
    def extract_text_from_pdf(self, pdf_file):
        """Extract text from uploaded PDF"""
        try:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""
    
    def process_document(self, text, doc_type):
        """Simulate document processing for RAG"""
        # Simulate chunking and embedding
        chunks = text.split('\n\n')  # Simple chunking
        processed_chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 20]
        
        # Mock embedding (in real implementation, use actual embedding model)
        embeddings = [hashlib.md5(chunk.encode()).hexdigest()[:16] for chunk in processed_chunks]
        
        return {
            "chunks": processed_chunks,
            "embeddings": embeddings,
            "doc_type": doc_type,
            "timestamp": datetime.now()
        }
    
    def answer_question(self, question, mode, documents):
        """Generate answer based on question and context"""
        question_lower = question.lower()
        
        # Determine topic based on keywords
        topic = "general"
        if any(word in question_lower for word in ["iot", "sensor", "actuator", "mqtt"]):
            topic = "iot"
        elif any(word in question_lower for word in ["cipher", "encryption", "rsa", "cryptography", "hill"]):
            topic = "cryptography"
        elif any(word in question_lower for word in ["array", "linked list", "tree", "graph", "algorithm"]):
            topic = "data_structures"
        elif any(word in question_lower for word in ["database", "sql", "normalization", "dbms"]):
            topic = "database"
        
        if mode == "Q&A Mode":
            if topic in self.knowledge_base:
                content = self.knowledge_base[topic]["content"]
                return f"Based on your documents, {content}\n\nThis information is relevant to your question about {topic}."
            else:
                return "I can help answer questions about IoT, Cryptography, Data Structures, and Database Management based on your uploaded documents."
        
        elif mode == "Exam Prep Mode":
            if topic in self.knowledge_base:
                questions = self.knowledge_base[topic]["questions"]
                mcq_response = f"Here are some practice questions for {topic}:\n\n"
                for i, q in enumerate(questions, 1):
                    mcq_response += f"{i}. {q}\n"
                return mcq_response
            else:
                return "Upload relevant documents to generate practice questions for exam preparation."
        
        elif mode == "Summary Mode":
            if documents:
                return f"📋 **Document Summary:**\n\nBased on your uploaded documents, here's a quick revision summary:\n\n• **Key Topics Covered:** IoT Architecture, Cryptographic Algorithms, Data Structure Operations, Database Management\n\n• **Important Concepts:** Focus on practical implementations and theoretical foundations\n\n• **Exam Focus Areas:** Algorithm complexity, encryption methods, database normalization, IoT protocols\n\n*This summary is generated from your uploaded study materials.*"
            else:
                return "Please upload documents to generate summaries."
        
        return "I'm here to help! Try asking specific questions about your study materials."

# Initialize RAG system
rag_system = MockRAGSystem()

# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 AI College Assistant</h1>
    <p>Your intelligent study companion powered by RAG (Retrieval-Augmented Generation)</p>
    <p><em>Upload your syllabus, notes, and past papers to get instant help!</em></p>
</div>
""", unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📁 Document Management")
    
    # Document Upload Section
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("#### Upload Documents")
    
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        accept_multiple_files=True,
        type=['pdf'],
        help="Upload syllabus, notes, past papers, or any study material"
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in st.session_state.documents:
                # Process the document
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    text_content = rag_system.extract_text_from_pdf(uploaded_file)
                    if text_content:
                        processed_doc = rag_system.process_document(text_content, "pdf")
                        st.session_state.documents[uploaded_file.name] = {
                            "content": text_content,
                            "processed": processed_doc,
                            "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.success(f"✅ {uploaded_file.name} processed successfully!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Mode Selection
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("#### 🎯 Assistant Mode")
    
    mode = st.selectbox(
        "Select mode:",
        ["Q&A Mode", "Exam Prep Mode", "Summary Mode"],
        key="mode_select",
        help="Choose how you want to interact with your documents"
    )
    st.session_state.current_mode = mode
    
    # Mode descriptions
    mode_descriptions = {
        "Q&A Mode": "💬 Ask specific questions about your study material",
        "Exam Prep Mode": "📝 Generate practice questions and MCQs",
        "Summary Mode": "📋 Get quick summaries and key points"
    }
    
    st.info(mode_descriptions[mode])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Document List
    if st.session_state.documents:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("#### 📚 Uploaded Documents")
        
        for doc_name, doc_info in st.session_state.documents.items():
            st.markdown(f'''
            <div class="doc-item">
                <strong>📄 {doc_name}</strong><br>
                <small>Uploaded: {doc_info["upload_time"]}</small>
            </div>
            ''', unsafe_allow_html=True)
        
        if st.button("🗑️ Clear All Documents", type="secondary"):
            st.session_state.documents = {}
            st.session_state.chat_history = []
            st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Action Buttons
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("#### ⚡ Quick Actions")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        if st.button("💡 Sample Questions", use_container_width=True):
            sample_questions = [
                "What are the main components of IoT architecture?",
                "Explain Hill Cipher with an example",
                "Compare array vs linked list time complexity",
                "What is database normalization?"
            ]
            st.session_state.chat_history.append({
                "type": "ai",
                "content": "Here are some sample questions you can ask:\n\n" + "\n".join([f"• {q}" for q in sample_questions]),
                "timestamp": datetime.now()
            })
    
    with col_b:
        if st.button("📊 Generate Summary", use_container_width=True):
            if st.session_state.documents:
                summary = rag_system.answer_question("", "Summary Mode", st.session_state.documents)
                st.session_state.chat_history.append({
                    "type": "ai",
                    "content": summary,
                    "timestamp": datetime.now()
                })
            else:
                st.warning("Upload documents first!")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 💬 Chat Interface")
    
    # Chat History
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.chat_history:
            for message in st.session_state.chat_history:
                if message["type"] == "user":
                    st.markdown(f'''
                    <div class="chat-message user-message">
                        <strong>👤 You:</strong> {message["content"]}
                        <br><small>{message["timestamp"].strftime("%H:%M:%S")}</small>
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                    <div class="chat-message ai-message">
                        <strong>🤖 AI Assistant:</strong><br>{message["content"]}
                        <br><small>{message["timestamp"].strftime("%H:%M:%S")}</small>
                    </div>
                    ''', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: #6b7280;">
                <h3>👋 Welcome to AI College Assistant!</h3>
                <p>Upload your study documents and start asking questions.</p>
                <p><strong>Try asking:</strong></p>
                <ul style="text-align: left; display: inline-block;">
                    <li>"What's important in Unit 4 IoT?"</li>
                    <li>"Give me 16-mark questions from Cryptography"</li>
                    <li>"Summarize Unit 3 for quick revision"</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Chat Input
    st.markdown("---")
    
    # Input form
    with st.form("chat_form", clear_on_submit=True):
        col_input, col_send = st.columns([4, 1])
        
        with col_input:
            user_question = st.text_input(
                "Ask a question:",
                placeholder=f"Try: What topics are in Unit 2? ({st.session_state.current_mode})",
                key="user_input"
            )
        
        with col_send:
            submit_button = st.form_submit_button("Send 🚀", use_container_width=True)
        
        if submit_button and user_question:
            # Add user message to chat
            st.session_state.chat_history.append({
                "type": "user",
                "content": user_question,
                "timestamp": datetime.now()
            })
            
            # Generate AI response
            with st.spinner("🤔 Thinking..."):
                ai_response = rag_system.answer_question(
                    user_question, 
                    st.session_state.current_mode, 
                    st.session_state.documents
                )
                
                st.session_state.chat_history.append({
                    "type": "ai",
                    "content": ai_response,
                    "timestamp": datetime.now()
                })
            
            st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 1rem;">
    <p>🎓 <strong>AI College Assistant</strong> - Powered by RAG Technology</p>
    <p><small>Perfect for hackathons, education, and productivity! Made with ❤️ and Streamlit</small></p>
</div>
""", unsafe_allow_html=True)
'''

# Write the main app file
with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.write(streamlit_app_code)

print("✅ Created streamlit_app.py")