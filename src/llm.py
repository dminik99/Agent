from langchain_ollama import ChatOllama

def get_llm():
    model_name = "llama3.1"

    return ChatOllama(
        model=model_name,
        base_url="http://localhost:11434"
    )