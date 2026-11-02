# 📚 Project Documentation

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend │    │   Flask Backend  │    │   RAG System    │
│   (Port 3000)   │◄──┤│   (Port 5000)   │◄──┤│   (Integrated)  │
│                 │    │                  │    │                 │
│ • Modern UI     │    │ • Document API   │    │ • FAISS Vector │
│ • Authentication│    │ • Q&A Endpoints  │    │ • Embeddings    │
│ • File Upload   │    │ • Gemini API     │    │ • Similarity    │
│ • Real-time     │    │ • RAG Processing │    │ • Retrieval     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Firebase      │    │   File System    │    │  Vector Store   │
│   Authentication│    │   Document Store │    │  (In Memory)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔧 Technical Stack

### Frontend (React 19.2.0)
- **UI Framework**: React with Hooks
- **Styling**: TailwindCSS + Glass Morphism
- **Authentication**: Firebase SDK
- **Routing**: React Router DOM
- **Icons**: React Icons
- **State Management**: React Context

### Backend (Python Flask)
- **API Framework**: Flask + CORS
- **AI Processing**: Google Gemini 2.0 Flash API
- **Document Processing**: PyPDF2, python-docx, openpyxl, Pillow
- **File Handling**: Werkzeug utilities
- **Environment**: python-dotenv

### RAG System (Advanced)
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **Chunking**: 500 words with 50-word overlap
- **Similarity**: Cosine similarity search
- **Retrieval**: Top-K relevant chunks

## 📁 Project Structure

```
ragbasedllm/
├── 📁 public/                 # React public assets
├── 📁 src/                    # React source code
│   ├── 📁 components/         # React components
│   │   ├── Dashboard.js       # Main dashboard
│   │   ├── Login.js          # Authentication
│   │   └── Profile.js        # User profile
│   ├── 📁 contexts/          # React contexts
│   │   └── AuthContext.js    # Firebase auth
│   └── App.js                # Main React app
├── 📁 python-backend/        # Flask backend
│   ├── app.py                # Main Flask app
│   ├── rag_system.py         # RAG implementation
│   ├── requirements.txt      # Python dependencies
│   ├── 📁 uploads/           # Uploaded files
│   └── 📁 users_data/        # User-specific data
├── package.json              # Node.js dependencies
├── setup_and_run.bat         # Complete setup script
├── start.bat                 # Quick start script
├── start_backend.bat         # Backend only
├── start_frontend.bat        # Frontend only
├── README.md                 # Main documentation
└── QUICK_START.md            # Quick start guide
```

## 🔄 Data Flow

### Document Upload Process
1. **Frontend**: User selects file
2. **API Call**: POST /api/upload
3. **Backend**: File validation & storage
4. **Text Extraction**: Extract text content
5. **Gemini Processing**: AI analysis
6. **RAG Indexing**: Create embeddings & chunks
7. **Storage**: Save to user library
8. **Response**: Return processing results

### Q&A Process
1. **Frontend**: User asks question
2. **API Call**: POST /api/qa/ask
3. **Backend**: Question categorization
4. **RAG Retrieval**: Vector similarity search
5. **Context Building**: Assemble relevant chunks
6. **Gemini Generation**: Generate contextual answer
7. **Response**: Return answer with metadata
8. **Frontend**: Display answer with RAG info

## 🛠️ API Endpoints

### Document Management
```http
POST /api/upload
GET  /api/library/{user_id}
GET  /api/document/{user_id}/{doc_id}
```

### Q&A System
```http
POST /api/qa/ask
GET  /api/qa/history/{user_id}
```

### System Stats
```http
GET /api/rag/stats
GET /api/real-time-stats
```

## ⚙️ Configuration

### Environment Variables
```bash
# Backend (.env file)
GEMINI_API_KEY=your_gemini_api_key
FLASK_ENV=development
```

### Firebase Config
```javascript
// Frontend (src/contexts/AuthContext.js)
const firebaseConfig = {
  apiKey: "your_api_key",
  authDomain: "your_auth_domain",
  // ... other config
}
```

## 🔒 Security Features

- **Firebase Authentication**: Secure user management
- **User Isolation**: Separate data per user
- **File Validation**: Type and size checks
- **API Protection**: User verification on endpoints
- **Error Handling**: Comprehensive error management

## 📊 Monitoring & Analytics

### Real-time Metrics
- Document processing counts
- Q&A session statistics
- RAG system performance
- Storage utilization
- System health indicators

### RAG-Specific Metrics
- Vector store size
- Embedding dimensions
- Retrieval accuracy
- Chunk utilization
- Similarity thresholds

## 🚀 Performance Optimizations

- **Efficient Chunking**: Optimized text segmentation
- **Vector Caching**: In-memory FAISS index
- **Batch Processing**: Multiple documents
- **Memory Management**: Normalized embeddings
- **Real-time Updates**: Live dashboard stats

## 🔧 Development Setup

### Requirements
- Node.js 16+
- Python 3.8+
- 4GB+ RAM (for models)
- 2GB+ storage

### Development Commands
```bash
# Install dependencies
npm install
pip install -r python-backend/requirements.txt

# Development servers
npm run dev          # Frontend with hot reload
python app.py        # Backend with debug mode

# Build for production
npm run build        # Creates build/ folder
```

## 🐛 Debugging

### Common Issues
1. **Model Loading**: First-time download takes time
2. **Memory Usage**: RAG models are memory-intensive
3. **Port Conflicts**: Ensure 3000 and 5000 are free
4. **CORS Issues**: Backend CORS is configured
5. **File Permissions**: Check upload directory access

### Debug Mode
```bash
# Enable Flask debug
export FLASK_ENV=development
python app.py

# React development mode
npm start
```

## 📈 Scaling Considerations

### For Production
- Use production WSGI server (Gunicorn)
- Implement Redis for caching
- Use PostgreSQL for metadata
- Add load balancing
- Implement monitoring (Prometheus)
- Use CDN for static assets

### RAG Scaling
- Persistent vector storage
- Distributed embeddings
- Chunk optimization
- Batch processing
- Model quantization