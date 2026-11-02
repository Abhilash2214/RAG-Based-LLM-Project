@echo off
title RAG-Based LLM Application Setup
color 0A

echo.
echo ==========================================
echo   RAG-Based LLM Application Setup
echo ==========================================
echo.
echo This script will:
echo [1] Install all dependencies
echo [2] Start the backend server
echo [3] Start the frontend application
echo.
pause

echo.
echo [STEP 1/4] Installing Node.js dependencies...
echo.
call npm install
if %errorlevel% neq 0 (
    echo.
    echo ❌ Failed to install Node.js dependencies
    echo Please ensure Node.js is installed and try again
    pause
    exit /b 1
)

echo.
echo [STEP 2/4] Installing Python dependencies...
echo.
cd python-backend
call pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ❌ Failed to install Python dependencies
    echo Please ensure Python 3.8+ is installed and try again
    pause
    exit /b 1
)

echo.
echo ✅ All dependencies installed successfully!
echo.
echo [STEP 3/4] Starting Backend Server...
echo.
echo 🚀 Starting RAG-Enhanced Backend on http://localhost:5000
start "RAG Backend Server" cmd /k "python app.py"

echo.
echo [STEP 4/4] Starting Frontend Application...
echo.
cd ..
timeout /t 3 /nobreak >nul
echo 🚀 Starting React Frontend on http://localhost:3000
start "RAG Frontend App" cmd /k "npm start"

echo.
echo ==========================================
echo       🎉 SETUP COMPLETE! 🎉
echo ==========================================
echo.
echo Your RAG-Based LLM Application is now running:
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend:  http://localhost:5000
echo.
echo Features Available:
echo ✅ Document Upload & Processing
echo ✅ RAG-Enhanced Q&A System
echo ✅ Vector Search & Embeddings
echo ✅ Real-time Analytics Dashboard
echo ✅ Multi-format Document Support
echo.
echo Press any key to open the application...
pause
start http://localhost:3000