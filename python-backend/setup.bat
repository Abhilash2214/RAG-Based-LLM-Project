@echo off
echo Setting up RAG Backend API...

:: Create virtual environment
python -m venv venv

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install dependencies
pip install -r requirements.txt

:: Create necessary directories
mkdir uploads 2>nul
mkdir users_data 2>nul

echo Setup complete! Run 'python app.py' to start the server.
pause