import ollama

MODEL = "qwen2.5:0.5b"

def chat(question:str, context:str, history: str):
    prompt = f"""
You are a helpful assistant. Use the following context to answer the question.
Context: {context}
Question: {question}
History: {history}"""

    response = ollama.chat(model=MODEL, messages=[{"role":"user", "content": prompt}],)

    return response["message"]["content"]