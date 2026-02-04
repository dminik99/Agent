from crewai import Agent
from src.llm import get_llm
from src.tools.datacleaner import clean_dataframe
from src.tools.correlator import correlate_events
from src.tools.detector import analyze_threat_distribution, train_and_predict_threats
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
        role='Detector',
        goal='Azonosítsd be a legveszélyesebb fenyegetéseket a hálózati forgalomban.',
        backstory='Egy kiberbiztonsági szakértő vagy, aki ML modellek segítségével keres anomáliákat és konkrét támadási mintákat.',
        tools=[analyze_threat_distribution, train_and_predict_threats],
        llm=llm,
        verbose=True
    )

    explainer = Agent(
        role="Explainer",
        goal="A detektált hálózati fenyegetések technikai hátterének közérthető magyarázata.",
        backstory=(
            "Te egy kiberbiztonsági szakértő vagy, aki a mesterséges intelligencia döntéseit fordítja le "
            "emberi nyelvre. Nem csak a számokat nézed, hanem érted az összefüggéseket: például ha a "
            "'stddev' (időbeli szórás) alacsony, de a 'srate' (forrás sebesség) magas, az egy automatizált "
            "DDoS támadásra utalhat. Feladatod, hogy elmagyarázd a döntési folyamatot a vezetőség számára."
        ),
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