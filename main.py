import json
from gemini_api import get_response

# Load knowledge base
with open("knowledge_base.json") as f:
    data = json.load(f)

context = str(data)

# Conversation history
chat_history = []

print("Multilingual College Assistant (type exit to quit)")

while True:
    query = input("You: ")

    if query.lower() == "exit":
        break

    # Add user message to history
    chat_history.append(f"User: {query}")

    prompt = f"""
    You are a multilingual college assistant.

    RULES:
    - Reply in same language as user
    - Use ONLY this college data
    - Remember previous conversation

    COLLEGE DATA:
    {context}

    CONVERSATION HISTORY:
    {chat_history}

    Latest Question: {query}
    """

    answer = get_response(prompt)

    print("Assistant:", answer)

    # Save assistant reply
    chat_history.append(f"Assistant: {answer}")
