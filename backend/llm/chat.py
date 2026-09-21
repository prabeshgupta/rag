import ollama

MODEL = "llama3.1:8b"

def chat(question:str, context:str):
    prompt = f"""
You are a helpful assistant. Use the following context to answer the question.
Context: {context}
Question: {question}"""

    response = ollama.chat(model=MODEL, messages=[{"role":"user", "content": prompt}])

    return response["message"]["content"]