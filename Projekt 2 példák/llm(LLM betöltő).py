from langchain_ollama import ChatOllama


def get_llm():
    """Itt hivom be az LLM-et, ha más modellt használnék csak kicsrélem a nevet"""
    model = "llama3.1"
    return ChatOllama(model=model, base_url="http://localhost:11434/")
