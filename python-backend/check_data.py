import os
import json

def check_user_data():
    """Check what's in the users_data directory"""
    
    users_data_dir = "users_data"
    
    if not os.path.exists(users_data_dir):
        print("❌ users_data directory doesn't exist")
        return
    
    print("📁 Users Data Directory Contents:")
    
    for user_folder in os.listdir(users_data_dir):
        user_path = os.path.join(users_data_dir, user_folder)
        if os.path.isdir(user_path):
            print(f"\n👤 User: {user_folder}")
            
            # Check library.json
            library_file = os.path.join(user_path, "library.json")
            if os.path.exists(library_file):
                with open(library_file, 'r', encoding='utf-8') as f:
                    library = json.load(f)
                
                print(f"📚 Total documents: {library.get('total_documents', 0)}")
                
                for doc in library.get('documents', []):
                    status = doc.get('metadata', {}).get('processing_status', 'unknown')
                    filename = doc.get('original_filename', 'unknown')
                    has_gemini = doc.get('metadata', {}).get('has_gemini_analysis', False)
                    
                    print(f"  📄 {filename}")
                    print(f"     Status: {status}")
                    print(f"     Gemini Analysis: {'✅' if has_gemini else '❌'}")
                    
                    # Check for errors
                    if 'error' in doc.get('gemini_processing', {}):
                        print(f"     Error: {doc['gemini_processing']['error']}")
                    
                    # Show processing method
                    method = doc.get('gemini_processing', {}).get('processing_method', 'unknown')
                    print(f"     Method: {method}")
            else:
                print("❌ No library.json found")

if __name__ == "__main__":
    check_user_data()