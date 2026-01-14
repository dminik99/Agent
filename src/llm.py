from langchain_ollama import ChatOllama


def get_llm():
    model = "llama3.1"
    return ChatOllama(model=model, base_url="http://localhost:11434/")