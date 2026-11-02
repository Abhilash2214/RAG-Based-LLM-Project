import requests
import json

def test_backend_api():
    """Test the RAG backend API"""
    base_url = "http://localhost:5000"
    
    try:
        # Test health check
        print("Testing health check...")
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
        
        # Test user library (empty initially)
        test_user_id = "test-user-123"
        print(f"\nTesting user library for {test_user_id}...")
        response = requests.get(f"{base_url}/api/library/{test_user_id}")
        if response.status_code == 200:
            print("✅ Library endpoint working!")
            library = response.json()
            print(f"Library contains {library.get('total_documents', 0)} documents")
        else:
            print(f"❌ Library test failed: {response.status_code}")
        
        print("\n🎉 Backend API is ready for file uploads!")
        print("\nAvailable endpoints:")
        print("- POST /api/upload - Upload files")
        print("- GET /api/library/{user_id} - Get user library")
        print("- GET /api/document/{user_id}/{document_id} - Get document details")
        print("- POST /api/search/{user_id} - Search documents")
        print("- DELETE /api/delete/{user_id}/{document_id} - Delete document")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend server.")
        print("Make sure the Python backend is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_backend_api()