@echo off
title Backend Only
color 0C

echo.
echo ==========================================
echo      🔧 Starting Backend Server Only
echo ==========================================
echo.

cd python-backend

echo Starting RAG-Enhanced Backend Server...
echo.
echo Features:
echo ✅ Document Processing & Upload
echo ✅ RAG System with Vector Search
echo ✅ Gemini API Integration
echo ✅ Real-time Q&A Endpoints
echo ✅ Multi-format File Support
echo.
echo Server will start on: http://localhost:5000
echo.

python app.py

pause