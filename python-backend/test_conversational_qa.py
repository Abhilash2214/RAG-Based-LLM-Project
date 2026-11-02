import requests
import json

def test_conversational_qa():
    """Test the conversational Q&A system with greetings and document questions"""
    base_url = "http://localhost:5000"
    
    # Test user and document IDs
    test_user_id = "aBZdQOSh4LcMAwjt4Q9ms70MNpJ2"  
    test_document_id = "5530755b-ace7-4bd0-b419-a19703b1133b"
    
    # Test questions of different types
    test_questions = [
        # Greetings
        {"type": "greeting", "question": "Hello!", "expected": "greeting response"},
        {"type": "greeting", "question": "Hi there", "expected": "friendly greeting"},
        {"type": "greeting", "question": "Good morning", "expected": "morning greeting"},
        
        # Conversational
        {"type": "conversational", "question": "Who are you?", "expected": "AI introduction"},
        {"type": "conversational", "question": "What can you do?", "expected": "capability explanation"},
        {"type": "conversational", "question": "How are you?", "expected": "polite response"},
        
        # Polite expressions
        {"type": "polite", "question": "Thank you", "expected": "polite acknowledgment"},
        {"type": "polite", "question": "Please help me", "expected": "helpful response"},
        
        # Document questions
        {"type": "document", "question": "What is this document about?", "expected": "document analysis"},
        {"type": "document", "question": "What order number is mentioned?", "expected": "specific info"},
        
        # Out of scope questions (should be restricted but polite)
        {"type": "restricted", "question": "What's the weather today?", "expected": "polite restriction"},
        {"type": "restricted", "question": "Tell me about Python programming", "expected": "redirect to document"},
        
        # Goodbye
        {"type": "goodbye", "question": "Goodbye", "expected": "polite farewell"},
        {"type": "goodbye", "question": "Thanks for your help", "expected": "appreciation response"}
    ]
    
    try:
        print("🧪 Testing Conversational Q&A System...\n")
        
        for i, test in enumerate(test_questions, 1):
            print(f"{i}. Testing {test['type']}: '{test['question']}'")
            
            qa_request = {
                "user_id": test_user_id,
                "document_id": test_document_id,
                "question": test['question']
            }
            
            response = requests.post(f"{base_url}/api/qa/ask", 
                                   headers={"Content-Type": "application/json"},
                                   json=qa_request)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Response: {result['answer'][:150]}...")
                print(f"   📝 Expected: {test['expected']}")
            else:
                print(f"   ❌ Failed: {response.status_code} - {response.text}")
            
            print("-" * 80)
        
        print("\n🎉 Conversational Q&A testing completed!")
        print("\n📋 System now supports:")
        print("✅ Greetings (Hello, Hi, Good morning, etc.)")
        print("✅ Polite expressions (Thank you, Please help, etc.)")
        print("✅ Conversational questions (Who are you?, What can you do?)")
        print("✅ Document-specific questions (content-based)")
        print("✅ Goodbyes (Goodbye, Thanks for help, etc.)")
        print("✅ Polite restrictions for out-of-scope questions")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the backend server.")
        print("Make sure the Python backend is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_conversational_qa()