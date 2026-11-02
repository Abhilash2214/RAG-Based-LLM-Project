# 🚀 Quick Start Guide

## Prerequisites Check ✅
```bash
node --version    # Should be 16+
python --version  # Should be 3.8+
pip --version     # Should be available
```

## One-Click Setup & Run 🎯

### Windows Users
```bash
# Clone the project
git clone <repository-url>
cd ragbasedllm

# Run complete setup (installs everything and starts both servers)
setup_and_run.bat
```

### Alternative: Individual Commands
```bash
# Just start both servers (if already set up)
start.bat

# Start only backend
start_backend.bat

# Start only frontend  
start_frontend.bat
```

## Manual Setup (Step by Step) 🔧

### 1. Install Dependencies
```bash
# Frontend dependencies
npm install

# Backend dependencies
cd python-backend
pip install -r requirements.txt
```

### 2. Start Backend
```bash
cd python-backend
python app.py
```
✅ Backend runs on: `http://localhost:5000`

### 3. Start Frontend (New Terminal)
```bash
npm start
```
✅ Frontend runs on: `http://localhost:3000`

## First Time Setup Notes 📝

- **Model Download**: First run will download sentence-transformers model (~90MB)
- **Startup Time**: Initial startup may take 30-60 seconds
- **Dependencies**: All Python packages will auto-install from requirements.txt

## Application URLs 🌐

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | React UI Application |
| Backend API | http://localhost:5000 | Flask REST API |
| RAG System | Integrated | Vector search & embeddings |

## Usage Flow 📋

1. **Open**: http://localhost:3000
2. **Sign In**: Use Google authentication
3. **Upload**: Drag & drop documents
4. **Wait**: RAG processing (auto-indexing)
5. **Chat**: Ask questions about documents
6. **Monitor**: Check dashboard for stats

## Troubleshooting 🔧

### Common Issues:
- **Port 3000 busy**: Change port or kill existing process
- **Port 5000 busy**: Kill existing Flask processes
- **Dependencies**: Run `pip install -r requirements.txt` again
- **Model download**: Wait for sentence-transformers to download

### Reset Everything:
```bash
# Clean install
rmdir node_modules /s
npm install
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

## Features Available ✨

✅ Document Upload (PDF, DOCX, Images)  
✅ RAG-Enhanced Q&A System  
✅ Vector Search & Embeddings  
✅ Real-time Analytics  
✅ Multi-format Processing  
✅ Firebase Authentication  
✅ Modern Glass Morphism UI  

Ready to experience advanced RAG technology! 🎉