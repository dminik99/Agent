from crewai import Agent, LLM
from src.tools.datacleaner import clean_dataframe
from src.tools.correlator import correlate_events
from src.tools.detector import train_supervised_detector, train_unsupervised_iforest
from src.tools.explainer import explain_features


def build_agents():
    llm = LLM(model="ollama/llama3.1", base_url="http://localhost:11434")
    data_cleaner = Agent(
        role="DataCleaner",
        goal="Adattisztítás és schema-összefoglaló készítése a megadott CSV-hez.",
        backstory="Tapasztalt adatgondnok, aki érti a SOC logok struktúráját.",
        tools=[clean_dataframe],
        llm=llm,
        verbose=True,
    )
    correlator = Agent(
        role="Correlator",
        goal="Egyszerű hálózati korrelációk és esemény-útvonalak azonosítása.",
        backstory="Hálózatbiztonsági elemző, aki IP kapcsolatokból gyanús láncokat keres.",
        tools=[correlate_events],
        llm=llm,
        verbose=True,
    )
    detector = Agent(
        role="Detector",
        goal="Fő detekciós modell tanítása és metrikák előállítása.",
        backstory="ML mérnök, aki baseline modelleket készít és kiértékel.",
        tools=[train_supervised_detector, train_unsupervised_iforest],
        llm=llm,
        verbose=True,
    )
    explainer = Agent(
        role="Explainer",
        goal="A modell fontos jellemzőinek azonosítása és magyarázata.",
        backstory="XAI szakértő, aki közérthetően fogalmaz a SOC számára.",
        tools=[explain_features],
        llm=llm,
        verbose=True,
    )
    random = Agent(
        role="Explainer",
        goal="A modell fontos jellemzőinek azonosítása és magyarázata.",
        backstory="XAI szakértő, aki közérthetően fogalmaz a SOC számára.",
        # tools=[file_read_tool],
        llm=llm,
        verbose=True,
    )
    return data_cleaner, correlator, detector, explainer, random
