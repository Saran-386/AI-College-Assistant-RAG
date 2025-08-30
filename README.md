# 🎓 AI College Assistant - RAG-based Hackathon Project

## 📋 Project Overview

This is a **hackathon-ready** AI College Assistant built with **Streamlit + LangChain RAG** that allows students to:

- 📄 **Upload PDFs/TXTs** of syllabus, notes, and past papers
- 💬 **Ask questions** and get answers with source citations
- 📝 **Generate MCQs** for exam preparation  
- 📋 **Create summaries** for quick revision
- 💾 **Persist knowledge** across sessions

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.10+** (recommended)
- **OpenAI API Key** (for the LLM responses)

### Step 1: Clone or Download
```bash
# If using git
git clone <your-repo-url>
cd ai-college-assistant

# Or download the files directly
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set OpenAI API Key
```bash
# On Windows:
set OPENAI_API_KEY=your_openai_api_key_here

# On macOS/Linux:
export OPENAI_API_KEY=your_openai_api_key_here

# Or create a .env file with:
# OPENAI_API_KEY=your_openai_api_key_here
```

### Step 5: Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

### 1. Upload Documents
- Click "Upload PDFs or TXTs" 
- Select your study materials (syllabus, notes, past papers)
- Click "Build / Update Knowledge Base"
- Wait for processing to complete ✅

### 2. Chat Tab 💬
- Ask questions like:
  - "What's important in Unit 4 IoT?"
  - "Explain Hill Cipher algorithm"
  - "Give me all questions related to Cryptography"

### 3. MCQs Tab 📝
- Enter a topic (e.g., "Unit 2 MAC Protocols")
- Click "Generate 5 MCQs"
- Get exam-style multiple choice questions with answers

### 4. Summaries Tab 🧾
- Enter what you want summarized
- Get 5-point bullet summaries for quick revision

## ⚙️ Configuration

Use the **sidebar settings** to tune the system:

- **Embedding Model**: Choose between fast vs accurate models
- **Chunk Size**: Adjust how documents are split (300-2000 characters)
- **Chunk Overlap**: Set overlap between chunks (0-400 characters)  
- **Top-K**: Number of document chunks to retrieve (1-10)
- **Temperature**: LLM creativity level (0.0-1.0)
- **Persistence**: Save index to disk for reuse

## 🛠️ Hackathon Demo Flow

### For Judges:

1. **Upload a syllabus PDF** 
   - Show: "Computer Science Syllabus.pdf uploaded ✅"

2. **Ask: "What topics are in Unit 2?"**
   - Show: AI highlights IoT architecture, sensors, protocols with page citations

3. **Upload past year question paper**
   - Show: "Past_Papers_2023.pdf processed ✅"

4. **Ask: "Give me all questions related to Hill Cipher"**
   - Show: AI extracts relevant crypto questions with page numbers

5. **Switch to MCQ tab, enter "IoT"**
   - Show: AI generates 5 exam-style MCQs with answers

6. **Switch to Summary tab, ask for "Unit 3 summary"**
   - Show: 5-point revision summary with sources

### Key Demo Points:
- ✅ **Real document processing** (not hard-coded)
- ✅ **Source citations** (filename + page numbers)
- ✅ **Multiple interaction modes** (Q&A, MCQs, Summaries)
- ✅ **Fast local embeddings** (no API costs for embedding)
- ✅ **Persistent knowledge base** (reuse across sessions)

## 🔧 Troubleshooting

### Common Issues:

**1. "No module named 'sentence_transformers'"**
```bash
pip install sentence-transformers>=3.0.1
```

**2. "OpenAI API key not set"**
- Make sure you've set the environment variable
- Or create `.env` file with your key

**3. "FAISS index error"**
- Delete `./rag_index` folder and rebuild
- Or disable persistence in sidebar

**4. "PyPDF read error"**
- Try a different PDF file
- Check if PDF is password protected
- Convert PDF to text first if needed

**5. Slow performance**
- Reduce chunk size in sidebar
- Use smaller embedding model
- Upload fewer/smaller documents

### Performance Tips:
- Keep document uploads focused and small
- Use "all-MiniLM-L6-v2" for faster embedding
- Set chunk size to 500-800 for optimal balance
- Enable persistence to avoid reprocessing

## 🏆 Why This Wins Hackathons

### ✅ **Relevant & Relatable**
- Everyone has struggled with notes/syllabus hunting
- Solves real student pain points

### ✅ **Technically Impressive** 
- Advanced AI (RAG) not just basic chatbot
- Real document processing with citations
- Multiple AI interaction modes

### ✅ **Great Demo Flow**
- Upload → Ask → Get Answer with Sources
- Visual feedback and progress indicators
- Multiple use cases in one app

### ✅ **Scalable & Marketable**
- Easy to pitch as EdTech product
- Can extend to multiple subjects
- Teachers can upload course materials
- Students get instant study help

### ✅ **Hackathon-Friendly**
- Single file architecture
- Minimal configuration needed
- Clear setup instructions
- Works offline after setup

## 🎯 Potential Extensions

### For Advanced Hackathons:
- **Multi-modal**: Add image/diagram analysis
- **Voice Interface**: Ask questions via speech
- **Study Groups**: Share knowledge bases
- **Progress Tracking**: Remember what you've studied
- **Smart Scheduling**: Suggest study plans
- **Mobile App**: React Native version

### Integration Ideas:
- **Learning Management Systems** (Moodle, Canvas)
- **Note-taking Apps** (Notion, Obsidian)
- **Calendar Apps** (Google Calendar for study scheduling)
- **Communication Apps** (Slack/Discord for study groups)

## 📁 Project Structure

```
ai-college-assistant/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This setup guide
├── .env               # Environment variables (optional)
├── .gitignore         # Git ignore file
└── rag_index/         # Persistent vector index (auto-created)
    ├── index.faiss
    └── index.pkl
```

## 🤝 Contributing

This project is designed for hackathons but contributions welcome!

### Key Areas:
- Better PDF parsing (tables, images)
- Additional embedding models
- More LLM providers (Anthropic, Cohere)
- Better prompt engineering
- UI/UX improvements

## 📄 License

Open source - perfect for hackathons and learning!

---

## 🎉 Ready to Hack!

You now have a **production-ready** AI College Assistant that demonstrates:
- Advanced RAG implementation
- Real document processing
- Multiple AI interaction modes  
- Professional UI/UX
- Scalable architecture

**Good luck at your hackathon! 🚀**
