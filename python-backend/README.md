# RAG Backend API

A comprehensive Python backend for processing documents and images using Google Gemini API with OCR capabilities.

## Features

- 📁 **File Upload Support**: PDF, DOC, DOCX, XLS, XLSX, Images (PNG, JPG, etc.), TXT, CSV
- 🤖 **Gemini AI Integration**: Advanced OCR and document analysis
- 👤 **User-Specific Storage**: Individual JSON libraries for each user
- 🔍 **Search Functionality**: Full-text search across all documents
- 📊 **Comprehensive Data Extraction**: Text, metadata, and AI analysis
- 🗃️ **CRUD Operations**: Complete document management

## Installation

1. Install Python dependencies:
```bash
cd python-backend
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Gemini API key
```

3. Run the server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- `GET /api/health` - Check API status

### File Operations
- `POST /api/upload` - Upload and process files
- `GET /api/library/{user_id}` - Get user's document library
- `GET /api/document/{user_id}/{document_id}` - Get specific document
- `POST /api/search/{user_id}` - Search user's documents
- `DELETE /api/delete/{user_id}/{document_id}` - Delete document

## File Processing Flow

1. **Upload** → File is saved with unique ID
2. **Text Extraction** → Content extracted based on file type
3. **Gemini Processing** → AI analysis and OCR for images
4. **JSON Storage** → Structured data saved to user's library
5. **Indexing** → Document indexed for search

## Supported File Types

- **Documents**: PDF, DOC, DOCX, TXT, CSV
- **Spreadsheets**: XLS, XLSX
- **Images**: PNG, JPG, JPEG, GIF, BMP, TIFF, SVG
- **Presentations**: PPT, PPTX

## Data Structure

Each document is stored as JSON with:
- Document metadata (ID, filename, size, type)
- Extracted text content
- Gemini AI analysis results
- User association and timestamps
- Processing status and error handling

## Security Features

- File type validation
- Secure filename handling
- User-specific data isolation
- Error handling and logging