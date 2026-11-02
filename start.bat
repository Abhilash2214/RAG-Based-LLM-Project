@echo off
title Start RAG Application
color 0B

echo.
echo ==========================================
echo     🚀 Starting RAG Application
echo ==========================================
echo.

echo [1/2] Starting Backend Server...
cd python-backend
start "RAG Backend" cmd /k "echo Starting RAG Backend Server... && python app.py"

echo [2/2] Starting Frontend Application...
cd ..
timeout /t 2 /nobreak >nul
start "RAG Frontend" cmd /k "echo Starting React Frontend... && npm start"

echo.
echo ✅ Both servers are starting...
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend:  http://localhost:5000
echo.
timeout /t 3 /nobreak >nul
start http://localhost:3000

echo.
echo Press any key to exit...
pause