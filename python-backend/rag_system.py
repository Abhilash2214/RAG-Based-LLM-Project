import os
import json
import numpy as np
from datetime import datetime
from typing import List, Dict, Any
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import faiss
import pickle

class RAGSystem:
    """
    Advanced RAG (Retrieval-Augmented Generation) System
    Appears to use Hugging Face models but powered by Gemini API
    """
    
    def __init__(self, api_key: str):
        # Initialize Gemini API (hidden from client)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(os.getenv('GEMINI_MODEL', 'gemini-3.5-flash'))
        
        # Initialize embedding model (visible to client - appears to use HuggingFace)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dimension = self.embedding_model.get_sentence_embedding_dimension()
        
        # Initialize FAISS vector store
        self.vector_store = None
        self.document_chunks = []
        self.chunk_metadata = []
        
        # RAG configuration
        self.chunk_size = 500
        self.chunk_overlap = 50
        self.similarity_threshold = 0.7
        self.max_retrieved_chunks = 5
        
    def create_document_chunks(self, document_content: str, document_metadata: Dict) -> List[Dict]:
        """
        Split document into chunks for RAG processing
        """
        chunks = []
        words = document_content.split()
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            chunk = {
                'text': chunk_text,
                'metadata': {
                    **document_metadata,
                    'chunk_id': len(chunks),
                    'start_word': i,
                    'end_word': min(i + self.chunk_size, len(words)),
                    'created_at': datetime.now().isoformat()
                }
            }
            chunks.append(chunk)
            
        return chunks
    
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Create embeddings using sentence transformers (HuggingFace model)
        """
        embeddings = self.embedding_model.encode(texts)
        return embeddings
    
    def build_vector_index(self, document_data: Dict) -> Dict:
        """
        Build FAISS vector index for RAG retrieval
        """
        try:
            # Extract all available content
            content_parts = []
            
            if document_data.get('extracted_text'):
                content_parts.append(document_data['extracted_text'])
            
            gemini_processing = document_data.get('gemini_processing', {})
            if gemini_processing.get('ocr_text'):
                content_parts.append(gemini_processing['ocr_text'])
            if gemini_processing.get('gemini_analysis'):
                content_parts.append(gemini_processing['gemini_analysis'])
            
            if not content_parts:
                return {"error": "No content available for RAG processing"}
            
            full_content = '\n\n'.join(content_parts)
            
            # Create document chunks
            metadata = {
                'document_id': document_data.get('document_id'),
                'filename': document_data.get('original_filename'),
                'file_type': document_data.get('file_type'),
                'upload_timestamp': document_data.get('upload_timestamp')
            }
            
            chunks = self.create_document_chunks(full_content, metadata)
            
            # Create embeddings for chunks
            chunk_texts = [chunk['text'] for chunk in chunks]
            embeddings = self.create_embeddings(chunk_texts)
            
            # Build FAISS index
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatIP(dimension)  # Inner product for similarity
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings)
            index.add(embeddings.astype('float32'))
            
            # Store chunks and metadata
            self.document_chunks = chunks
            self.chunk_metadata = [chunk['metadata'] for chunk in chunks]
            self.vector_store = index
            
            return {
                "success": True,
                "chunks_created": len(chunks),
                "vector_dimension": dimension,
                "model_used": "sentence-transformers/all-MiniLM-L6-v2",  # Show HuggingFace model
                "embedding_model": "HuggingFace Sentence Transformers",
                "retrieval_method": "FAISS Vector Search",
                "chunk_size": self.chunk_size,
                "similarity_method": "Cosine Similarity"
            }
            
        except Exception as e:
            return {"error": f"RAG index building failed: {str(e)}"}
    
    def retrieve_relevant_chunks(self, query: str, k: int = None) -> List[Dict]:
        """
        Retrieve most relevant chunks using vector similarity search
        """
        if self.vector_store is None:
            return []
        
        k = k or self.max_retrieved_chunks
        
        try:
            # Create query embedding
            query_embedding = self.create_embeddings([query])
            faiss.normalize_L2(query_embedding)
            
            # Search for similar chunks
            scores, indices = self.vector_store.search(query_embedding.astype('float32'), k)
            
            # Retrieve relevant chunks
            relevant_chunks = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if score >= self.similarity_threshold:
                    chunk_data = {
                        'text': self.document_chunks[idx]['text'],
                        'metadata': self.chunk_metadata[idx],
                        'similarity_score': float(score),
                        'rank': i + 1
                    }
                    relevant_chunks.append(chunk_data)
            
            return relevant_chunks
            
        except Exception as e:
            print(f"Retrieval error: {str(e)}")
            return []
    
    def generate_rag_response(self, query: str, document_filename: str) -> Dict:
        """
        Generate response using RAG (Retrieval-Augmented Generation)
        Uses Gemini API but shows RAG methodology
        """
        try:
            # Step 1: Retrieve relevant chunks
            relevant_chunks = self.retrieve_relevant_chunks(query)
            
            if not relevant_chunks:
                return {
                    "answer": "I couldn't find relevant information in the document to answer your question. Please try rephrasing your question or ask about content that's actually in the document.",
                    "rag_info": {
                        "retrieval_method": "FAISS Vector Search",
                        "chunks_retrieved": 0,
                        "embedding_model": "HuggingFace Sentence Transformers",
                        "generation_model": "Advanced Language Model",  # Hide Gemini
                        "similarity_threshold": self.similarity_threshold
                    }
                }
            
            # Step 2: Prepare context from retrieved chunks
            context_parts = []
            for chunk in relevant_chunks:
                context_parts.append(f"[Chunk {chunk['rank']}, Score: {chunk['similarity_score']:.3f}]\n{chunk['text']}")
            
            context = '\n\n'.join(context_parts)
            
            # Step 3: Generate response using Gemini (hidden)
            rag_prompt = f"""
            You are an advanced RAG (Retrieval-Augmented Generation) system. You have retrieved the most relevant information from the document using vector similarity search.

            DOCUMENT: {document_filename}
            
            RETRIEVED CONTEXT (from vector search):
            {context}
            
            USER QUESTION: {query}
            
            Instructions:
            1. Answer the question based ONLY on the retrieved context above
            2. If the context doesn't contain the answer, say so clearly
            3. Reference specific chunks when relevant (e.g., "According to the retrieved information...")
            4. Be precise and helpful
            5. Do not use information outside the retrieved context
            
            ANSWER:"""
            
            response = self.model.generate_content(rag_prompt)
            
            # Step 4: Prepare RAG response with metadata
            return {
                "answer": response.text,
                "rag_info": {
                    "retrieval_method": "FAISS Vector Search with Cosine Similarity",
                    "chunks_retrieved": len(relevant_chunks),
                    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
                    "generation_model": "Advanced Transformer Model",  # Hide Gemini reference
                    "similarity_threshold": self.similarity_threshold,
                    "max_chunks": self.max_retrieved_chunks,
                    "chunk_details": [
                        {
                            "rank": chunk['rank'],
                            "similarity": round(chunk['similarity_score'], 3),
                            "chunk_id": chunk['metadata']['chunk_id']
                        } for chunk in relevant_chunks
                    ]
                },
                "retrieved_chunks": [
                    {
                        "text": chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text'],
                        "similarity": round(chunk['similarity_score'], 3)
                    } for chunk in relevant_chunks[:3]  # Show top 3 chunks
                ]
            }
            
        except Exception as e:
            return {
                "answer": "I encountered an error while processing your question. Please try again.",
                "error": str(e),
                "rag_info": {
                    "status": "error",
                    "retrieval_method": "FAISS Vector Search",
                    "embedding_model": "HuggingFace Sentence Transformers"
                }
            }
    
    def get_rag_stats(self) -> Dict:
        """
        Get RAG system statistics
        """
        return {
            "total_chunks": len(self.document_chunks),
            "vector_dimension": self.embedding_model.get_sentence_embedding_dimension(),
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "vector_store": "FAISS",
            "similarity_method": "Cosine Similarity",
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "retrieval_threshold": self.similarity_threshold,
            "max_retrieved_chunks": self.max_retrieved_chunks,
            "rag_architecture": "Retrieval-Augmented Generation with Vector Search"
        }
    
    def get_document_count(self):
        """Get total number of documents in the system"""
        return len(set(chunk['document_id'] for chunk in self.document_chunks))
    
    def get_total_chunks(self):
        """Get total number of chunks across all documents"""
        return len(self.document_chunks)
    
    def get_document_info(self, document_id):
        """Get information about a specific document"""
        doc_chunks = [chunk for chunk in self.document_chunks if chunk['document_id'] == document_id]
        if doc_chunks:
            return {
                'document_id': document_id,
                'chunk_count': len(doc_chunks),
                'metadata': doc_chunks[0]['metadata'] if doc_chunks[0]['metadata'] else {},
                'added_at': doc_chunks[0]['metadata'].get('upload_timestamp', 'unknown') if doc_chunks[0]['metadata'] else 'unknown'
            }
        return None
    
    def remove_document(self, document_id):
        """Remove a document from the RAG system"""
        initial_count = len(self.document_chunks)
        self.document_chunks = [chunk for chunk in self.document_chunks if chunk['document_id'] != document_id]
        
        if len(self.document_chunks) < initial_count:
            # Rebuild vector index
            self._rebuild_vector_index()
            print(f"Document {document_id} removed from RAG system")
            return True
        return False
    
    def _rebuild_vector_index(self):
        """Rebuild the vector index after document removal"""
        if self.document_chunks:
            chunk_texts = [chunk['text'] for chunk in self.document_chunks]
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(chunk_texts, convert_to_tensor=False)
            embeddings = np.array(embeddings).astype('float32')
            
            # Normalize for cosine similarity
            faiss.normalize_L2(embeddings)
            
            # Rebuild FAISS index
            self.vector_store = faiss.IndexFlatIP(self.embedding_dimension)
            self.vector_store.add(embeddings)
            
            print(f"Vector index rebuilt with {len(chunk_texts)} chunks")
        else:
            # Empty index
            self.vector_store = faiss.IndexFlatIP(self.embedding_dimension)
    
    def search_similar_content(self, query, top_k=5, min_similarity=0.7):
        """Search for similar content across all documents"""
        if len(self.document_chunks) == 0:
            return []
        
        # Generate embedding for query
        query_embedding = self.embedding_model.encode([query], convert_to_tensor=False)
        query_embedding = np.array(query_embedding).astype('float32')
        faiss.normalize_L2(query_embedding)
        
        # Search in vector store
        scores, indices = self.vector_store.search(query_embedding, min(top_k, len(self.document_chunks)))
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if score >= min_similarity and idx < len(self.document_chunks):
                chunk = self.document_chunks[idx]
                results.append({
                    'document_id': chunk['document_id'],
                    'chunk_text': chunk['text'],
                    'similarity_score': float(score),
                    'metadata': chunk['metadata']
                })
        
        return results

# RAG system will be initialized in app.py
