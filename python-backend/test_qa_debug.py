import requests
import json

# Test the Q&A API endpoint directly
def test_qa_api():
    url = "http://localhost:5000/api/qa/ask"
    
    # Test data
    test_data = {
        "user_id": "test-user-123",
        "document_id": "test-doc-id",
        "question": "Hello, how are you?"
    }
    
    try:
        print("Testing Q&A API...")
        print(f"URL: {url}")
        print(f"Data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(url, json=test_data)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response JSON: {json.dumps(result, indent=2)}")
        else:
            print(f"Error Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_qa_api()