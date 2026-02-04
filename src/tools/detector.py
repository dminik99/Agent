import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from crewai.tools import tool

def _prepare_data(df):
    """Tisztítja az adatokat és kezeli a hiányzó értékeket."""
    garbage_cols = ['pkSeqID', 'seq', 'saddr', 'daddr'] 
    df = df.drop(columns=[c for c in garbage_cols if c in df.columns])
    
    le = LabelEncoder()
    for col in df.select_dtypes(include=['object']).columns:
        if col not in ['category', 'subcategory']:
            df[col] = le.fit_transform(df[col].astype(str))
    
    df = df.fillna(0)
    return df

@tool("analyze_threat_distribution")
def analyze_threat_distribution(csv_path: str) -> str:
    """
    Megvizsgálja a fájlt és visszaadja a fenyegetések statisztikai eloszlását.
    """
    try:
        df = pd.read_csv(csv_path)
        if 'category' not in df.columns:
            return "Hiba: Nem található 'category' oszlop az adathalmazban."
        
        counts = df['category'].value_counts()
        subcounts = df['subcategory'].value_counts()
        
        report = "### Észlelt Fenyegetések Eloszlása:\n"
        for cat, count in counts.items():
            report += f"- {cat}: {count} alkalommal\n"
        
        report += "\n### Részletes altípusok:\n"
        for subcat, count in subcounts.items():
            report += f"- {subcat}: {count} alkalommal\n"
            
        return report
    except Exception as e:
        return f"Hiba az elemzés során: {str(e)}"

@tool("train_and_predict_threats")
def train_and_predict_threats(csv_path: str) -> str:
    """
    Betanít egy osztályozó modellt a támadások típusainak felismerésére, 
    és visszaadja a modell pontosságát.
    """
    try:
        df = pd.read_csv(csv_path)
        
        target = 'category'
        if target not in df.columns:
            return "Hiba: A célváltozó (category) nem található."

        X = _prepare_data(df.drop(columns=[target]))
        y = df[target]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        clf = RandomForestClassifier(n_estimators=50, random_state=42)
        clf.fit(X_train, y_train)
        
        score = clf.score(X_test, y_test)
        
        importances = pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=False).head(3)
        features_str = ", ".join([f"{k} ({v:.2f})" for k, v in importances.items()])

        return (f"Modell betanítva. Pontosság: {score:.2%}\n"
                f"Legfontosabb indikátorok: {features_str}")
    except Exception as e:
        return f"Hiba a tanítás során: {str(e)}"