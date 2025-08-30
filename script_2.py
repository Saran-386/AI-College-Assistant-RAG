# Create requirements.txt file
requirements_content = '''streamlit>=1.36
langchain>=0.2.7
langchain-community>=0.2.7
langchain-openai>=0.1.14
faiss-cpu>=1.8.0
sentence-transformers>=3.0.1
pypdf>=4.2.0
python-dotenv>=1.0.1
pandas>=2.2.2
'''

with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write(requirements_content)

print("✅ Created requirements.txt")

# Create a comprehensive setup guide
setup_guide = '''# 🎓 AI College Assistant - RAG-based Hackathon Project

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
venv\\Scripts\\activate
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
'''

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(setup_guide)

print("✅ Created README.md with comprehensive setup guide")

# Create a .env template file
env_template = '''# AI College Assistant Environment Variables
# Copy this file to .env and add your actual API key

# OpenAI API Key (required for LLM responses)
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Other LLM providers
# ANTHROPIC_API_KEY=your_anthropic_key
# COHERE_API_KEY=your_cohere_key

# Optional: Hugging Face for alternative embeddings
# HUGGINGFACE_API_KEY=your_hf_key
'''

with open('.env.template', 'w', encoding='utf-8') as f:
    f.write(env_template)

print("✅ Created .env.template")

# Create a .gitignore file
gitignore_content = '''# Environment variables
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# RAG Index (optional - remove if you want to commit the index)
rag_index/

# Streamlit
.streamlit/secrets.toml

# Logs
*.log

# Temporary files
temp/
tmp/
uploads/
'''

with open('.gitignore', 'w', encoding='utf-8') as f:
    f.write(gitignore_content)

print("✅ Created .gitignore")

# Create a simple demo script
demo_script = '''#!/usr/bin/env python3
"""
Quick demo script for AI College Assistant
Run this after setting up the environment to test basic functionality
"""

import os
import sys

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'streamlit',
        'langchain',
        'langchain_community', 
        'langchain_openai',
        'sentence_transformers',
        'pypdf',
        'python-dotenv',
        'pandas',
        'faiss'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} - MISSING")
    
    if missing:
        print(f"\\n⚠️ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\\n🎉 All dependencies installed!")
    return True

def check_env():
    """Check environment setup"""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ OpenAI API Key: {api_key[:8]}...{api_key[-4:]}")
    else:
        print("⚠️ OpenAI API Key not set")
        print("Set with: export OPENAI_API_KEY=your_key")
    
    return bool(api_key)

def main():
    print("🎓 AI College Assistant - Demo Check\\n")
    
    deps_ok = check_dependencies()
    env_ok = check_env()
    
    print("\\n" + "="*50)
    
    if deps_ok and env_ok:
        print("🚀 Ready to launch! Run:")
        print("   streamlit run app.py")
    elif deps_ok:
        print("📋 Dependencies OK, but set your OpenAI API key first")
    else:
        print("🔧 Install dependencies first, then set API key")
    
    print("\\n📖 See README.md for detailed setup instructions")

if __name__ == "__main__":
    main()
'''

with open('demo_check.py', 'w', encoding='utf-8') as f:
    f.write(demo_script)

print("✅ Created demo_check.py")

print("\\n🎉 All files created successfully!")
print("\\nProject structure:")
print("├── app.py              # Main Streamlit application")
print("├── requirements.txt    # Python dependencies") 
print("├── README.md          # Comprehensive setup guide")
print("├── .env.template      # Environment variables template")
print("├── .gitignore         # Git ignore rules")
print("└── demo_check.py      # Quick dependency checker")