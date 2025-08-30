#!/usr/bin/env python3
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
        print(f"\n⚠️ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False

    print("\n🎉 All dependencies installed!")
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
    print("🎓 AI College Assistant - Demo Check\n")

    deps_ok = check_dependencies()
    env_ok = check_env()

    print("\n" + "="*50)

    if deps_ok and env_ok:
        print("🚀 Ready to launch! Run:")
        print("   streamlit run app.py")
    elif deps_ok:
        print("📋 Dependencies OK, but set your OpenAI API key first")
    else:
        print("🔧 Install dependencies first, then set API key")

    print("\n📖 See README.md for detailed setup instructions")

if __name__ == "__main__":
    main()
