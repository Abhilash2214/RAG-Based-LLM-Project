# 🤖 Advanced RAG-Based LLM Application

> **A cutting-edge document processing and Q&A application with advanced RAG (Retrieval-Augmented Generation) capabilities**

[![React](https://img.shields.io/badge/React-19.2.0-blue)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://python.org/)
[![Flask](https://img.shields.io/badge/Flask-Backend-red)](https://flask.palletsprojects.com/)
[![Gemini API](https://img.shields.io/badge/Gemini-2.0%20Flash-purple)](https://ai.google.dev/)
[![RAG](https://img.shields.io/badge/RAG-Enabled-orange)](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)

## 🚀 Quick Start

### Prerequisites
```bash
✅ Node.js 16+ installed
✅ Python 3.8+ installed
✅ Git installed
```

### ⚡ One-Click Setup & Run

**Windows:**
```bash
# 1. Clone and setup everything
git clone <your-repo-url>
cd ragbasedllm

# 2. Run the setup script (installs all dependencies)
setup_and_run.bat
```

**Manual Setup:**
```bash
# 1. Install Frontend Dependencies
npm install

# 2. Install Backend Dependencies
cd python-backend
pip install -r requirements.txt

# 3. Start Backend (Terminal 1)
python app.py

# 4. Start Frontend (Terminal 2)
cd ..
npm start
```

## 🎯 Features Overview

### 🧠 Advanced RAG System
- **Vector Search**: FAISS-powered similarity search with 384-dimensional embeddings
- **Semantic Chunking**: Intelligent document segmentation (500 words, 50 overlap)
- **Context Retrieval**: Retrieves most relevant document chunks for accurate responses
- **Hybrid Processing**: Combines vector search with generative AI for enhanced accuracy

### 📄 Document Processing
- **Multi-Format Support**: PDF, DOCX, images, Excel, PowerPoint, and more
- **OCR Capabilities**: Extract text from images and scanned documents
- **Intelligent Analysis**: AI-powered content analysis and metadata extraction
- **Real-time Processing**: Instant document indexing and vector embedding

### 💬 Intelligent Q&A System
- **Context-Aware Responses**: Answers based on retrieved document chunks
- **Question Classification**: Handles greetings, document queries, and conversational input
- **RAG Metadata**: Shows chunk retrieval information and similarity scores
- **Chat History**: Persistent conversation tracking with document context

### 🎨 Modern User Interface
- **Glass Morphism Design**: Beautiful modern UI with TailwindCSS
- **Real-time Dashboard**: Live statistics with RAG system status
- **Responsive Layout**: Works perfectly on desktop and mobile
- **Interactive Elements**: Smooth animations and transitions

## 🏗️ Technical Architecture

### Frontend Stack
- **React 19.2.0**: Modern component-based UI framework
- **TailwindCSS**: Utility-first CSS framework
- **Firebase SDK**: Authentication and user management

### Backend Stack
- **Flask**: Lightweight Python web framework
- **Google Gemini 2.0 Flash**: Advanced language model
- **Sentence Transformers**: State-of-the-art text embeddings
- **FAISS**: Facebook AI Similarity Search for vector operations

### RAG Architecture
```
Documents → Chunking → Embeddings → Vector Store (FAISS)
                                         ↓
User Query → Embedding → Similarity Search → Context Retrieval
                                         ↓
Retrieved Chunks + Query → Gemini API → Enhanced Response
```

## 🛠️ Quick Setup

### Automated Setup (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd ragbasedllm

# Run the automated setup script
setup_rag_system.bat
```

### Manual Setup
```bash
# Frontend
npm install
npm start

# Backend  
cd python-backend
pip install -r requirements.txt
python app.py
```

## 🎯 How to Use

### Step 1: Start the Application
```bash
# Option A: Use the setup script
setup_and_run.bat

# Option B: Manual start
# Terminal 1: Backend
cd python-backend && python app.py

# Terminal 2: Frontend  
npm start
```

### Step 2: Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

### Step 3: Use the Features
1. **🔐 Sign In**: Register or use Google authentication
2. **📄 Upload Documents**: Drag & drop PDF, DOCX, images, etc.
3. **🤖 RAG Processing**: Documents auto-indexed with vector embeddings
4. **💬 Ask Questions**: Select documents and chat with AI
5. **📊 View Analytics**: Monitor RAG system performance

### Step 4: Experience RAG Features
- **Smart Search**: Vector-based document retrieval
- **Context-Aware**: Answers based on relevant document chunks
- **Real-time Stats**: Monitor embedding and retrieval performance
- **Multi-format**: Supports text, images, and complex documents

## 🔌 API Endpoints

- `POST /api/upload` - Upload and process documents with RAG indexing
- `POST /api/qa/ask` - Ask questions with RAG-enhanced responses
- `GET /api/rag/stats` - Get RAG system statistics and health
- `GET /api/real-time-stats` - Get real-time dashboard statistics

## 🧪 RAG System Configuration

- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Dimension**: 384
- **Similarity Method**: Cosine similarity with FAISS
- **Chunk Size**: 500 words with 50-word overlap
- **Retrieval Threshold**: 0.7 similarity score

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
