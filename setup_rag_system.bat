@echo off
echo ========================================
echo RAG-Enhanced Document Analysis System
echo ========================================
echo.

echo Installing Python dependencies...
cd python-backend
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ❌ Failed to install Python dependencies
    echo Please check your Python installation and try again
    pause
    exit /b 1
)

echo.
echo ✅ Python dependencies installed successfully!
echo.

echo Starting RAG-Enhanced Backend Server...
echo.
echo The server will start with the following features:
echo - Advanced RAG (Retrieval-Augmented Generation)
echo - FAISS Vector Search
echo - Sentence Transformers Embeddings  
echo - Multi-format Document Processing
echo - Real-time Q&A with Context Awareness
echo.

python app.py

pause