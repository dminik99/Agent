from langchain_ollama import ChatOllama
from crewai import LLM

def get_llm():
    """
    A CrewAI natív LLM osztályát használjuk.
    A 'model' paraméternél fontos az 'ollama/' prefix!
    """
    return LLM(
        model="ollama/llama3.1",
        base_url="http://localhost:11434"
    )