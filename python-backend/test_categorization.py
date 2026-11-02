from app import categorize_question

# Test the categorization function
test_questions = [
    "Hello",
    "What are the all technologies used in this project",
    "Tell me about the document",
    "Explain the content",
    "Who are you",
    "Thanks"
]

for question in test_questions:
    result = categorize_question(question)
    print(f"Question: '{question}' -> Category: '{result}'")