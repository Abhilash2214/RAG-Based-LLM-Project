import requests
import json

def test_qa_api():
    """Test the Q&A API endpoints"""
    base_url = "http://localhost:5000"
    
    # Test user and document IDs (replace with actual ones from your system)
    test_user_id = "aBZdQOSh4LcMAwjt4Q9ms70MNpJ2"
    test_document_id = "5530755b-ace7-4bd0-b419-a19703b1133b"
    
    try:
        print("🧪 Testing Q&A API Endpoints...\n")
        
        # Test 1: Get document content for Q&A
        print("1. Testing document content retrieval...")
        response = requests.get(f"{base_url}/api/qa/get-document-content/{test_user_id}/{test_document_id}")
        if response.status_code == 200:
            doc_content = response.json()
            print("✅ Document content retrieved successfully!")
            print(f"   📄 Filename: {doc_content['filename']}")
            print(f"   📊 Has content: {doc_content['has_content']}")
            print(f"   📝 Content preview: {doc_content['content'][:200]}...")
        else:
            print(f"❌ Failed to get document content: {response.status_code}")
            print(f"   Error: {response.text}")
            return
        
        # Test 2: Ask a question
        print("\n2. Testing Q&A functionality...")
        test_question = "What is this document about? Give me a brief summary."
        
        qa_request = {
            "user_id": test_user_id,
            "document_id": test_document_id,
            "question": test_question
        }
        
        response = requests.post(f"{base_url}/api/qa/ask", 
                               headers={"Content-Type": "application/json"},
                               json=qa_request)
        
        if response.status_code == 200:
            qa_result = response.json()
            print("✅ Q&A successful!")
            print(f"   ❓ Question: {qa_result['question']}")
            print(f"   🤖 Answer: {qa_result['answer'][:300]}...")
            print(f"   📄 Document: {qa_result['document_filename']}")
        else:
            print(f"❌ Q&A failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
        
        # Test 3: Get Q&A history
        print("\n3. Testing Q&A history...")
        response = requests.get(f"{base_url}/api/qa/history/{test_user_id}")
        if response.status_code == 200:
            history = response.json()
            print("✅ Q&A history retrieved!")
            print(f"   📊 Total sessions: {history['total_sessions']}")
            print(f"   📝 Recent sessions: {len(history['recent_sessions'])}")
            
            if history['recent_sessions']:
                latest = history['recent_sessions'][-1]
                print(f"   🕐 Latest Q&A: {latest['question'][:50]}...")
        else:
            print(f"❌ Failed to get Q&A history: {response.status_code}")
        
        print("\n🎉 Q&A API is working properly!")
        print("\n📋 Available endpoints:")
        print("- GET /api/qa/get-document-content/{user_id}/{document_id}")
        print("- POST /api/qa/ask")
        print("- GET /api/qa/history/{user_id}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the backend server.")
        print("Make sure the Python backend is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_qa_api()