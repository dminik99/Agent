import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from crewai.tools import tool

@tool("explain_features")
def explain_features(csv_path_and_label: str) -> str:
    """
    Ez az eszköz kiszámolja a Feature Importance értékeket.
    Segít megérteni, hogy mely hálózati jellemzők (pl. src_bytes, count)
    alapján döntött a modell a támadásról.
    Bemenet: 'fajl_utvonal.csv|cel_valtozo_neve'.
    Visszatér a top 5 legfontosabb jellemző listájával.
    """
    try:
        path, label_col = csv_path_and_label.split('|')
        df = pd.read_csv(path)
        
        le = LabelEncoder()
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = le.fit_transform(df[col].astype(str))
            
        X = df.drop(columns=[label_col])
        y = df[label_col]
        
        clf = RandomForestClassifier(n_estimators=10, random_state=42)
        clf.fit(X, y)
        
        importances = pd.Series(clf.feature_importances_, index=X.columns)
        top_10 = importances.nlargest(10).to_dict()
        
        return f"Top 10 Influential Features for Attack Detection: {top_10}"
    except Exception as e:
        return f"Explanation error: {str(e)}"