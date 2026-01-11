from crewai import Agent
from src.llm import get_llm
from src.tools.datacleaner import clean_dataframe
from src.tools.correlator import correlate_events
from src.tools.detector import train_supervised_detector, train_unsupervised_iforest
from src.tools.explainer import explain_features

def build_agents():
    llm = get_llm()
    
    data_cleaner = Agent(
        role="DataCleaner",
        goal="Adattisztítás végrehajtása és séma készítése.",
        backstory="Precíz adatgondnok vagy, aki a nyers logokat emészthető formátumba hozza.",
        tools=[clean_dataframe],
        llm=llm,
        verbose=True,
    )

    correlator = Agent(
        role="Correlator",
        goal="Hálózati összefüggések és gyanús IP címek keresése.",
        backstory="Hálózatbiztonsági elemző, aki a 'cleaned_data.csv'-ből dolgozik.",
        tools=[correlate_events],
        llm=llm,
        verbose=True,
    )

    detector = Agent(
        role="Detector",
        goal="ML modellek futtatása a támadások detektálására.",
        backstory="ML mérnök vagy. Ha van címke, supervised modellt használsz, ha nincs, anomália detektálást.",
        tools=[train_supervised_detector, train_unsupervised_iforest],
        llm=llm,
        verbose=True,
    )

    explainer = Agent(
        role="Explainer",
        goal="Megmagyarázni, miért döntött úgy a modell, ahogy.",
        backstory="XAI (Explainable AI) szakértő, aki a technikai feature-öket (pl. src_bytes) értelmezi.",
        tools=[explain_features],
        llm=llm,
        verbose=True,
    )

    reporter = Agent(
        role="Reporter",
        goal="Vezetői összefoglaló (Incidens Riport) írása az összes előző eredmény alapján.",
        backstory="Kiberbiztonsági tanácsadó, aki az adatokat üzleti kockázattá és érthető jelentéssé formálja.",
        llm=llm,
        verbose=True,
    )

    return data_cleaner, correlator, detector, explainer, reporter