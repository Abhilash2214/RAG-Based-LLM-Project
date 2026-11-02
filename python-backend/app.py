import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import google.generativeai as genai
from werkzeug.utils import secure_filename
import uuid
import json
from datetime import datetime
import mimetypes
from PIL import Image
import PyPDF2
from docx import Document
import openpyxl
from dotenv import load_dotenv
from rag_system import RAGSystem

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing. Add it to python-backend/.env")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)

# Initialize RAG System
rag_system = RAGSystem(api_key=GEMINI_API_KEY)

# Configuration
UPLOAD_FOLDER = 'uploads'
USERS_DATA_FOLDER = 'users_data'
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 
    'xls', 'xlsx', 'csv', 'ppt', 'pptx', 'bmp', 'tiff', 'svg'
}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(USERS_DATA_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_data_path(user_id):
    """Get the path to user's data directory"""
    user_dir = os.path.join(USERS_DATA_FOLDER, user_id)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

def get_predefined_response(question_type, question):
    """Get predefined responses for common questions"""
    import random
    
    responses = {
        'greeting': [
            "Hello! I'm here to help you analyze your documents. What would you like to know about your uploaded files?",
            "Hi there! I can help you understand and explore the content of your documents. How can I assist you today?",
            "Good day! I'm your document analysis assistant. Feel free to ask me questions about your uploaded files.",
            "Hello! Welcome to your document Q&A system. I'm ready to help you explore your content."
        ],
        'conversational': {
            'who are you': "I'm your personal document analysis assistant, powered by Gemini AI. I help you understand and explore the content of your uploaded documents.",
            'what can you do': "I can analyze your uploaded documents, answer questions about their content, extract specific information, and help you understand complex data. Just ask me anything about your files!",
            'how are you': "I'm doing great and ready to help you explore your documents! What would you like to know about your files?",
            'what is your name': "I'm your document analysis assistant! I don't have a specific name, but I'm here to help you with all your document questions.",
            'can you help': "Absolutely! I'm here to help you understand and analyze your documents. What would you like to know?",
            'help me': "Of course! I'm ready to help you explore your documents. What specific information are you looking for?"
        },
        'polite': {
            'thank you': "You're very welcome! I'm happy to help you with your documents. Is there anything else you'd like to know?",
            'thanks': "My pleasure! Feel free to ask more questions about your documents anytime.",
            'please': "Of course! I'm here to help you understand your documents. What would you like to know?",
            'excuse me': "No problem at all! How can I help you with your documents today?"
        },
        'goodbye': [
            "Goodbye! Feel free to come back anytime you need help with your documents.",
            "Thanks for using the document analysis system! Have a great day!",
            "It was my pleasure helping you explore your documents. See you next time!",
            "Farewell! Your documents will be here whenever you need to analyze them again."
        ]
    }
    
    question_lower = question.lower().strip()
    
    if question_type == 'greeting':
        return random.choice(responses['greeting'])
    elif question_type == 'conversational':
        for key, response in responses['conversational'].items():
            if key in question_lower:
                return response
        return "I'm your document analysis assistant! I can help you understand and explore the content of your uploaded files."
    elif question_type == 'polite':
        for key, response in responses['polite'].items():
            if key in question_lower:
                return response
        return "Thank you! I'm happy to help you with your documents. What would you like to know?"
    elif question_type == 'goodbye':
        return random.choice(responses['goodbye'])
    
    return None

def categorize_question(question):
    """Categorize the type of question being asked"""
    question_lower = question.lower().strip()
    
    # Check for document-related keywords first (highest priority)
    document_keywords = [
        'document', 'file', 'content', 'text', 'information', 'data', 'report', 'analysis',
        'what is', 'what are', 'tell me about', 'explain', 'describe', 'summary', 
        'technologies', 'project', 'details', 'findings', 'results', 'conclusion'
    ]
    
    # Check if it's clearly a document question
    if any(keyword in question_lower for keyword in document_keywords):
        # But exclude meta questions about the AI itself
        meta_phrases = ['who are you', 'what are you exactly', 'what is your name', 'introduce yourself']
        if not any(meta in question_lower for meta in meta_phrases):
            return 'document_question'
    
    # Simple greetings (exact matches)
    simple_greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
    if question_lower in simple_greetings or question_lower.startswith(tuple(simple_greetings)):
        return 'greeting'
    
    # Polite expressions
    if question_lower in ['thanks', 'thank you', 'please', 'excuse me']:
        return 'polite'
    
    # Meta/conversational questions about the AI
    meta_questions = ['who are you', 'what can you do', 'what is your name', 'introduce yourself', 'how are you']
    if any(meta in question_lower for meta in meta_questions):
        return 'conversational'
    
    # Goodbye expressions
    goodbyes = ['bye', 'goodbye', 'see you', 'farewell']
    if any(bye in question_lower for bye in goodbyes):
        return 'goodbye'
    
    # Default to document question
    return 'document_question'

def ocr_pdf_with_gemini(file_path):
    """OCR for scanned / image-only PDFs: send the PDF to Gemini and get the text back"""
    try:
        with open(file_path, 'rb') as f:
            pdf_bytes = f.read()
        prompt = (
            "This PDF is a scanned document or image. Extract ALL text exactly as written, "
            "including names, numbers, dates, addresses and table values. "
            "Keep the label and value together, for example 'Name: ...'. "
            "Return only the extracted text."
        )
        response = model.generate_content([
            {"mime_type": "application/pdf", "data": pdf_bytes},
            prompt
        ])
        return (response.text or "").strip()
    except Exception as e:
        print(f"Gemini PDF OCR error: {str(e)}")
        return ""

def extract_text_from_file(file_path, file_type):
    """Extract text from various file types"""
    try:
        if file_type.startswith('image/'):
            # For images, we'll use Gemini API for OCR
            return None  # Will be processed by Gemini
        
        elif file_type == 'application/pdf':
            print("Extracting text from PDF...")
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        page_text = page.extract_text()
                        text += page_text + "\n"
                    print(f"PDF text extraction successful. Length: {len(text)} characters")
                    if len(text.strip()) < 20:
                        print("PDF has no text layer (scanned). Using Gemini OCR...")
                        ocr_text = ocr_pdf_with_gemini(file_path)
                        if ocr_text:
                            return ocr_text
                        return "PDF processed but no readable text found"
                    return text
            except Exception as pdf_error:
                print(f"PDF extraction error: {str(pdf_error)}")
                return f"PDF processing error: {str(pdf_error)}"
        
        elif file_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        
        elif file_type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:
            workbook = openpyxl.load_workbook(file_path)
            text = ""
            for sheet_name in workbook.sheetnames:
                sheet = workbook[sheet_name]
                for row in sheet.iter_rows(values_only=True):
                    text += " ".join([str(cell) for cell in row if cell is not None]) + "\n"
            return text
        
        elif file_type.startswith('text/'):
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        
        else:
            return "Unsupported file type for text extraction"
    
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def process_with_gemini(file_path, file_type, extracted_text=None):
    """Process file using Gemini API for comprehensive analysis"""
    print(f"Processing file: {file_path}, type: {file_type}")
    
    try:
        if file_type.startswith('image/'):
            print("Processing as image with Gemini Vision...")
            # For images, use Gemini's vision capabilities
            image = Image.open(file_path)
            
            prompt = """
            Analyze this image and extract all information:
            1. Any text present (OCR)
            2. Visual description
            3. Objects or elements identified
            4. Context and purpose
            
            Provide your analysis in clear text format.
            """
            
            response = model.generate_content([prompt, image])
            print("Gemini vision processing successful")
            return {
                "ocr_text": response.text,
                "file_type": "image",
                "processing_method": "gemini_vision"
            }
        
        else:
            print("Processing as document with text analysis...")
            # For other files, use the extracted text with Gemini for analysis
            if extracted_text and len(extracted_text.strip()) > 0:
                # Limit text to prevent token issues
                text_sample = extracted_text[:8000] if len(extracted_text) > 8000 else extracted_text
                
                prompt = f"""
                Analyze this document content:
                
                {text_sample}
                
                Provide:
                1. Document summary
                2. Key topics
                3. Important information
                4. Main conclusions
                
                Keep response concise and clear.
                """
                
                response = model.generate_content(prompt)
                print("Gemini text analysis successful")
                return {
                    "extracted_text": extracted_text,
                    "gemini_analysis": response.text,
                    "file_type": "document",
                    "processing_method": "gemini_text_analysis"
                }
            else:
                print("No text content available for analysis")
                return {
                    "message": "File processed but no text content found",
                    "file_type": file_type,
                    "processing_method": "no_text_content"
                }
    
    except Exception as e:
        print(f"Gemini processing error: {str(e)}")
        return {
            "error": f"Gemini processing failed: {str(e)}",
            "extracted_text": extracted_text if extracted_text else None,
            "file_type": file_type,
            "processing_method": "error"
        }

def save_document_data(user_id, document_data):
    """Save document data to user-specific JSON file"""
    user_dir = get_user_data_path(user_id)
    user_library_file = os.path.join(user_dir, 'library.json')
    
    # Load existing library or create new
    if os.path.exists(user_library_file):
        with open(user_library_file, 'r', encoding='utf-8') as f:
            library = json.load(f)
    else:
        library = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "documents": [],
            "total_documents": 0
        }
    
    # Add new document
    library["documents"].append(document_data)
    library["total_documents"] = len(library["documents"])
    library["last_updated"] = datetime.now().isoformat()
    
    # Save updated library
    with open(user_library_file, 'w', encoding='utf-8') as f:
        json.dump(library, f, indent=2, ensure_ascii=False)
    
    # Also save individual document file
    doc_file = os.path.join(user_dir, f"{document_data['document_id']}.json")
    with open(doc_file, 'w', encoding='utf-8') as f:
        json.dump(document_data, f, indent=2, ensure_ascii=False)
    
    return library

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "RAG Backend API is running",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload and process file endpoint"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        user_id = request.form.get('user_id')
        
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            file_id = str(uuid.uuid4())
            filename = secure_filename(file.filename)
            file_extension = filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{file_id}.{file_extension}"
            
            # Save file
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(file_path)
            
            # Get file type
            file_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
            file_size = os.path.getsize(file_path)
            
            # Extract text (if applicable)
            print(f"Extracting text from {filename}...")
            extracted_text = extract_text_from_file(file_path, file_type)
            print(f"Text extraction result: {len(extracted_text) if extracted_text else 0} characters")
            
            # Process with Gemini API
            print("Starting Gemini API processing...")
            gemini_result = process_with_gemini(file_path, file_type, extracted_text)
            print(f"Gemini processing complete: {gemini_result.get('processing_method', 'unknown')}")

            # Images (and other files with no text): use Gemini's OCR text as the document text
            if not (extracted_text and extracted_text.strip()) and gemini_result.get("ocr_text"):
                extracted_text = gemini_result["ocr_text"]
            
            # Process with RAG system for better Q&A capabilities
            print("Processing document with RAG system...")
            rag_processed = False
            if extracted_text and extracted_text.strip():
                try:
                    # Add document to RAG system
                    rag_system.add_document(file_id, extracted_text, {
                        "filename": filename,
                        "file_type": file_type,
                        "user_id": user_id,
                        "upload_timestamp": datetime.now().isoformat()
                    })
                    rag_processed = True
                    print("Document successfully added to RAG system")
                except Exception as e:
                    print(f"RAG processing failed: {str(e)}")
            
            # Prepare document data
            document_data = {
                "document_id": file_id,
                "original_filename": filename,
                "stored_filename": unique_filename,
                "file_path": file_path,
                "file_type": file_type,
                "file_size": file_size,
                "upload_timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "extracted_text": extracted_text,
                "gemini_processing": gemini_result,
                "rag_processed": rag_processed,
                "metadata": {
                    "file_extension": file_extension,
                    "processing_status": (
                        "completed" if "error" not in gemini_result and 
                        ("gemini_analysis" in gemini_result or "ocr_text" in gemini_result)
                        else "error_with_fallback" if "error" in gemini_result
                        else "processed"
                    ),
                    "has_text": bool(extracted_text and extracted_text.strip()),
                    "has_gemini_analysis": "gemini_analysis" in gemini_result or "ocr_text" in gemini_result,
                    "rag_enabled": rag_processed,
                    "error_details": gemini_result.get("error", None) if "error" in gemini_result else None
                }
            }
            
            # Save to user's library
            updated_library = save_document_data(user_id, document_data)
            
            return jsonify({
                "success": True,
                "message": "File uploaded and processed successfully",
                "document_id": file_id,
                "filename": filename,
                "processing_result": gemini_result,
                "library_stats": {
                    "total_documents": updated_library["total_documents"],
                    "last_updated": updated_library["last_updated"]
                }
            })
        
        else:
            return jsonify({"error": "File type not allowed"}), 400
    
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@app.route('/api/library/<user_id>', methods=['GET'])
def get_user_library(user_id):
    """Get user's document library"""
    try:
        user_dir = get_user_data_path(user_id)
        library_file = os.path.join(user_dir, 'library.json')
        
        if os.path.exists(library_file):
            with open(library_file, 'r', encoding='utf-8') as f:
                library = json.load(f)
            return jsonify(library)
        else:
            return jsonify({
                "user_id": user_id,
                "documents": [],
                "total_documents": 0,
                "message": "No library found for user"
            })
    
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve library: {str(e)}"}), 500

@app.route('/api/document/<user_id>/<document_id>', methods=['GET'])
def get_document(user_id, document_id):
    """Get specific document details"""
    try:
        user_dir = get_user_data_path(user_id)
        doc_file = os.path.join(user_dir, f"{document_id}.json")
        
        if os.path.exists(doc_file):
            with open(doc_file, 'r', encoding='utf-8') as f:
                document = json.load(f)
            return jsonify(document)
        else:
            return jsonify({"error": "Document not found"}), 404
    
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve document: {str(e)}"}), 500

@app.route('/api/file/<user_id>/<document_id>', methods=['GET'])
def get_document_file(user_id, document_id):
    """Serve the original uploaded file (view inline, or download with ?download=1)"""
    try:
        user_dir = get_user_data_path(user_id)
        library_file = os.path.join(user_dir, 'library.json')

        if not os.path.exists(library_file):
            return jsonify({"error": "Library not found"}), 404

        with open(library_file, 'r', encoding='utf-8') as f:
            library = json.load(f)

        for doc in library.get("documents", []):
            if doc.get("document_id") == document_id:
                file_path = os.path.abspath(doc["file_path"])
                if not os.path.exists(file_path):
                    return jsonify({"error": "File missing on server"}), 404

                as_attachment = request.args.get('download') == '1'
                return send_file(
                    file_path,
                    mimetype=doc.get("file_type") or "application/octet-stream",
                    as_attachment=as_attachment,
                    download_name=doc.get("original_filename") or os.path.basename(file_path)
                )

        return jsonify({"error": "Document not found"}), 404

    except Exception as e:
        return jsonify({"error": f"Failed to get file: {str(e)}"}), 500

@app.route('/api/search/<user_id>', methods=['POST'])
def search_documents(user_id):
    """Search through user's documents"""
    try:
        search_query = request.json.get('query', '').lower()
        
        if not search_query:
            return jsonify({"error": "Search query is required"}), 400
        
        user_dir = get_user_data_path(user_id)
        library_file = os.path.join(user_dir, 'library.json')
        
        if not os.path.exists(library_file):
            return jsonify({
                "results": [],
                "total_results": 0,
                "query": search_query
            })
        
        with open(library_file, 'r', encoding='utf-8') as f:
            library = json.load(f)
        
        # Search through documents
        results = []
        for doc in library["documents"]:
            # Search in filename, extracted text, and Gemini analysis
            searchable_content = [
                doc.get("original_filename", "").lower(),
                doc.get("extracted_text", "").lower(),
                str(doc.get("gemini_processing", {})).lower()
            ]
            
            if any(search_query in content for content in searchable_content):
                results.append(doc)
        
        return jsonify({
            "results": results,
            "total_results": len(results),
            "query": search_query,
            "searched_in": library["total_documents"]
        })
    
    except Exception as e:
        return jsonify({"error": f"Search failed: {str(e)}"}), 500

@app.route('/api/delete/<user_id>/<document_id>', methods=['DELETE'])
def delete_document(user_id, document_id):
    """Delete a document from user's library"""
    try:
        user_dir = get_user_data_path(user_id)
        library_file = os.path.join(user_dir, 'library.json')
        doc_file = os.path.join(user_dir, f"{document_id}.json")
        
        # Load library
        if not os.path.exists(library_file):
            return jsonify({"error": "Library not found"}), 404
        
        with open(library_file, 'r', encoding='utf-8') as f:
            library = json.load(f)
        
        # Find and remove document
        document_found = False
        for i, doc in enumerate(library["documents"]):
            if doc["document_id"] == document_id:
                # Remove uploaded file
                if os.path.exists(doc["file_path"]):
                    os.remove(doc["file_path"])
                
                # Remove from library
                library["documents"].pop(i)
                library["total_documents"] = len(library["documents"])
                library["last_updated"] = datetime.now().isoformat()
                document_found = True
                break
        
        if not document_found:
            return jsonify({"error": "Document not found"}), 404
        
        # Save updated library
        with open(library_file, 'w', encoding='utf-8') as f:
            json.dump(library, f, indent=2, ensure_ascii=False)
        
        # Remove individual document file
        if os.path.exists(doc_file):
            os.remove(doc_file)
        
        return jsonify({
            "success": True,
            "message": "Document deleted successfully",
            "remaining_documents": library["total_documents"]
        })
    
    except Exception as e:
        return jsonify({"error": f"Delete failed: {str(e)}"}), 500

@app.route('/api/qa/get-document-content/<user_id>/<document_id>', methods=['GET'])
def get_document_for_qa(user_id, document_id):
    """Get document content for Q&A"""
    try:
        user_dir = get_user_data_path(user_id)
        doc_file = os.path.join(user_dir, f"{document_id}.json")
        
        if not os.path.exists(doc_file):
            return jsonify({"error": "Document not found"}), 404
        
        with open(doc_file, 'r', encoding='utf-8') as f:
            document = json.load(f)
        
        # Extract content for Q&A
        content = ""
        
        # Add extracted text if available
        if document.get('extracted_text'):
            content += f"Document Text:\n{document['extracted_text']}\n\n"
        
        # Add Gemini analysis
        gemini_processing = document.get('gemini_processing', {})
        if gemini_processing.get('ocr_text'):
            content += f"OCR Content:\n{gemini_processing['ocr_text']}\n\n"
        if gemini_processing.get('gemini_analysis'):
            content += f"Analysis:\n{gemini_processing['gemini_analysis']}\n\n"
        
        return jsonify({
            "document_id": document_id,
            "filename": document.get('original_filename', 'Unknown'),
            "file_type": document.get('file_type', 'unknown'),
            "content": content.strip(),
            "upload_date": document.get('upload_timestamp', ''),
            "has_content": bool(content.strip())
        })
    
    except Exception as e:
        return jsonify({"error": f"Failed to get document content: {str(e)}"}), 500

@app.route('/api/qa/ask', methods=['POST'])
def ask_question():
    """Ask a question about a specific document using RAG system"""
    try:
        data = request.json
        user_id = data.get('user_id')
        document_id = data.get('document_id')
        question = data.get('question')
        
        print(f"Q&A Request - User: {user_id}, Doc: {document_id}, Question: {question}")
        
        if not all([user_id, document_id, question]):
            return jsonify({"error": "user_id, document_id, and question are required"}), 400
        
        # Get document content
        user_dir = get_user_data_path(user_id)
        doc_file = os.path.join(user_dir, f"{document_id}.json")
        
        if not os.path.exists(doc_file):
            return jsonify({"error": "Document not found"}), 404
        
        with open(doc_file, 'r', encoding='utf-8') as f:
            document = json.load(f)
        
        filename = document.get('original_filename', 'Unknown')
        print(f"Processing Q&A for document: {filename}")
        
        # Categorize the question
        question_type = categorize_question(question)
        print(f"Question type: {question_type}")
        
        # Handle greeting and conversational questions
        if question_type == 'greeting':
            answer = f"Hello! I'm your advanced document analysis assistant powered by RAG (Retrieval-Augmented Generation). I'm currently ready to help you with questions about '{filename}'. What would you like to know about this document?"
        elif question_type == 'polite':
            answer = f"You're welcome! I'm here to help you analyze '{filename}' using advanced AI techniques. Feel free to ask me anything about this document's content."
        elif question_type == 'conversational':
            answer = f"I'm an AI assistant specialized in document analysis using RAG technology. I can help you understand and extract information from your uploaded documents. Right now, I'm ready to answer questions about '{filename}'. You can ask me about its content, key information, or any specific details you need."
        elif question_type == 'goodbye':
            answer = f"Goodbye! Feel free to come back anytime if you have more questions about '{filename}' or other documents. Have a great day!"
        else:
            # Handle document-related questions with RAG system
            print("Using RAG system for document Q&A...")
            
            # Check if document was processed by RAG system
            if document.get('rag_processed', False):
                try:
                    # Use RAG system for enhanced Q&A
                    rag_response = rag_system.ask_question(question, document_id)
                    answer = rag_response['answer']
                    
                    # Add RAG metadata to response
                    rag_metadata = {
                        'rag_enabled': True,
                        'chunks_retrieved': len(rag_response.get('relevant_chunks', [])),
                        'similarity_scores': rag_response.get('similarity_scores', []),
                        'processing_method': 'rag_enhanced'
                    }
                    
                    print(f"RAG response generated with {rag_metadata['chunks_retrieved']} relevant chunks")
                    
                except Exception as rag_error:
                    print(f"RAG system error: {str(rag_error)}")
                    # Fallback to traditional method
                    answer = fallback_document_qa(document, question, filename)
                    rag_metadata = {
                        'rag_enabled': False,
                        'processing_method': 'fallback_gemini',
                        'rag_error': str(rag_error)
                    }
            else:
                # Use traditional method if RAG processing failed
                answer = fallback_document_qa(document, question, filename)
                rag_metadata = {
                    'rag_enabled': False,
                    'processing_method': 'traditional_gemini',
                    'reason': 'document_not_rag_processed'
                }
        
        # Save Q&A to history
        qa_entry = {
            "question": question,
            "answer": answer,
            "timestamp": datetime.now().isoformat(),
            "document_id": document_id,
            "document_filename": filename,
            "question_type": question_type,
            "rag_metadata": rag_metadata if 'rag_metadata' in locals() else None
        }
        
        # Save to user's Q&A history
        qa_history_file = os.path.join(user_dir, 'qa_history.json')
        if os.path.exists(qa_history_file):
            with open(qa_history_file, 'r', encoding='utf-8') as f:
                qa_history = json.load(f)
        else:
            qa_history = {"user_id": user_id, "qa_sessions": []}
        
        qa_history["qa_sessions"].append(qa_entry)
        
        # Keep only last 100 Q&A sessions
        if len(qa_history["qa_sessions"]) > 100:
            qa_history["qa_sessions"] = qa_history["qa_sessions"][-100:]
        
        with open(qa_history_file, 'w', encoding='utf-8') as f:
            json.dump(qa_history, f, indent=2, ensure_ascii=False)
        
        print(f"Q&A completed successfully")
        
        return jsonify({
            "question": question,
            "answer": answer,
            "document_filename": filename,
            "timestamp": qa_entry["timestamp"],
            "question_type": question_type,
            "rag_metadata": rag_metadata if 'rag_metadata' in locals() else None
        })
    
    except Exception as e:
        print(f"Q&A error: {str(e)}")
        return jsonify({"error": f"Q&A failed: {str(e)}"}), 500

def fallback_document_qa(document, question, filename):
    """Fallback method for Q&A when RAG system fails"""
    # Prepare content for Q&A
    content = ""
    
    # Combine all available content from the JSON
    if document.get('extracted_text'):
        content += f"Extracted Text:\n{document['extracted_text']}\n\n"
    
    gemini_processing = document.get('gemini_processing', {})
    if gemini_processing.get('ocr_text'):
        content += f"OCR Content:\n{gemini_processing['ocr_text']}\n\n"
    if gemini_processing.get('gemini_analysis'):
        content += f"Document Analysis:\n{gemini_processing['gemini_analysis']}\n\n"
    
    # Add metadata information
    metadata = document.get('metadata', {})
    if metadata:
        content += f"File Information:\n"
        content += f"- File Type: {document.get('file_type', 'unknown')}\n"
        content += f"- File Size: {document.get('file_size', 0)} bytes\n"
        content += f"- Upload Date: {document.get('upload_timestamp', 'unknown')}\n\n"
    
    if not content.strip():
        return "I apologize, but there's no readable content available in this document for me to analyze. The document might be corrupted, empty, or in a format that couldn't be processed."
    
    # Create comprehensive prompt for document questions
    prompt = f"""
You are a helpful AI assistant that answers questions based ONLY on the provided document content.

IMPORTANT RULES:
1. Answer ONLY based on the information in the document content below
2. If the question cannot be answered from the document, clearly state "This information is not available in the document"
3. Do not use external knowledge - stick to the document content only
4. Be specific and cite relevant parts when possible
5. If asked about topics not in the document, politely redirect to document content

DOCUMENT: {filename}

DOCUMENT CONTENT:
{content[:15000]}  # Limit to prevent token issues

USER QUESTION: {question}

Please provide a helpful answer based on the document content:"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as gemini_error:
        print(f"Fallback Gemini API error: {str(gemini_error)}")
        return "I apologize, but I'm having trouble processing your question right now. Please try asking again in a moment."

@app.route('/api/qa/history/<user_id>', methods=['GET'])
def get_qa_history(user_id):
    """Get user's Q&A history"""
    try:
        user_dir = get_user_data_path(user_id)
        qa_history_file = os.path.join(user_dir, 'qa_history.json')
        
        if os.path.exists(qa_history_file):
            with open(qa_history_file, 'r', encoding='utf-8') as f:
                qa_history = json.load(f)
            
            # Return last 20 sessions
            recent_sessions = qa_history.get("qa_sessions", [])[-20:]
            return jsonify({
                "user_id": user_id,
                "total_sessions": len(qa_history.get("qa_sessions", [])),
                "recent_sessions": recent_sessions
            })
        else:
            return jsonify({
                "user_id": user_id,
                "total_sessions": 0,
                "recent_sessions": []
            })
    
    except Exception as e:
        return jsonify({"error": f"Failed to get Q&A history: {str(e)}"}), 500

@app.route('/api/rag/stats', methods=['GET'])
def get_rag_stats():
    """Get RAG system statistics"""
    try:
        # Get basic RAG system stats
        stats = {
            "documents_in_rag": rag_system.get_document_count(),
            "total_chunks": rag_system.get_total_chunks(),
            "vector_dimension": rag_system.embedding_dimension,
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "retrieval_method": "FAISS Vector Search",
            "chunk_size": 500,
            "chunk_overlap": 50,
            "similarity_threshold": 0.7,
            "rag_enabled": True,
            "system_status": "operational"
        }
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({
            "error": f"Failed to get RAG stats: {str(e)}",
            "rag_enabled": False,
            "system_status": "error"
        }), 500

@app.route('/api/real-time-stats', methods=['GET'])
def get_real_time_stats():
    """Get real-time dashboard statistics"""
    try:
        # Count total users
        total_users = len([d for d in os.listdir(USERS_DATA_FOLDER) if os.path.isdir(os.path.join(USERS_DATA_FOLDER, d))])
        
        # Count total documents
        total_documents = 0
        total_questions = 0
        rag_documents = 0
        
        for user_dir in os.listdir(USERS_DATA_FOLDER):
            user_path = os.path.join(USERS_DATA_FOLDER, user_dir)
            if os.path.isdir(user_path):
                # Count user documents
                library_file = os.path.join(user_path, 'library.json')
                if os.path.exists(library_file):
                    with open(library_file, 'r', encoding='utf-8') as f:
                        library = json.load(f)
                        user_docs = len(library.get('documents', []))
                        total_documents += user_docs
                        
                        # Count RAG-enabled documents
                        for doc in library.get('documents', []):
                            if doc.get('rag_processed', False):
                                rag_documents += 1
                
                # Count Q&A sessions
                qa_file = os.path.join(user_path, 'qa_history.json')
                if os.path.exists(qa_file):
                    with open(qa_file, 'r', encoding='utf-8') as f:
                        qa_history = json.load(f)
                        total_questions += len(qa_history.get('qa_sessions', []))
        
        # Calculate processing rates
        rag_adoption_rate = (rag_documents / total_documents * 100) if total_documents > 0 else 0
        
        return jsonify({
            "total_users": total_users,
            "total_documents": total_documents,
            "total_questions": total_questions,
            "rag_documents": rag_documents,
            "rag_adoption_rate": round(rag_adoption_rate, 1),
            "documents_per_user": round(total_documents / total_users, 1) if total_users > 0 else 0,
            "questions_per_document": round(total_questions / total_documents, 1) if total_documents > 0 else 0,
            "timestamp": datetime.now().isoformat(),
            "system_health": "excellent" if rag_adoption_rate > 80 else "good" if rag_adoption_rate > 50 else "fair"
        })
    
    except Exception as e:
        return jsonify({"error": f"Failed to get real-time stats: {str(e)}"}), 500

if __name__ == '__main__':
    print("Starting RAG-Enhanced Document Analysis Backend API...")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Users data folder: {USERS_DATA_FOLDER}")
    print("✅ Gemini API configured and ready")
    print("✅ RAG System initialized with FAISS vector search")
    print("✅ Sentence Transformers embedding model loaded")
    print("✅ Advanced document processing capabilities enabled")
    print("\nRAG System Features:")
    print("- Vector-based document search")
    print("- Semantic chunk retrieval")
    print("- Retrieval-Augmented Generation")
    print("- Multi-format document support")
    print("- Real-time Q&A with context awareness")
    print("\nAPI Server starting on http://0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)