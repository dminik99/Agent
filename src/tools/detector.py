import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from crewai.tools import tool

@tool("train_supervised_detector")
def train_supervised_detector(csv_path_and_label: str) -> str:
    """
    Ez az eszköz egy felügyelt (supervised) ML modellt tanít a megadott adatokon.
    Bemeneti formátum: 'fajl_utvonal.csv|cel_valtozo_neve'.
    Visszatér a modell pontossági metrikáival (pl. Accuracy).
    """
    try:
        path, label_col = csv_path_and_label.split('|')
        df = pd.read_csv(path)
        
        if label_col not in df.columns:
            return f"Error: Label column '{label_col}' not found."

        le = LabelEncoder()
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = le.fit_transform(df[col].astype(str))
            
        X = df.drop(columns=[label_col])
        y = df[label_col]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        clf = RandomForestClassifier(n_estimators=10)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        
        report = classification_report(y_test, y_pred, output_dict=True)

        return f"Model Trained. Metrics (Macro Avg): {report['macro avg']}"
    except Exception as e:
        return f"Supervised training error: {str(e)}"

@tool("train_unsupervised_iforest")
def train_unsupervised_iforest(csv_path: str) -> str:
    """
    Ez az eszköz anomália detektálást végez címkézetlen adatokon Isolation Forest segítségével.
    Bemenet: csv fájl elérési útja. Visszatér a detektált anomáliák számával.
    """
    try:
        df = pd.read_csv(csv_path)
        df_numeric = df.select_dtypes(include=['number']).fillna(0)
        
        iso = IsolationForest(contamination=0.05, random_state=42)
        preds = iso.fit_predict(df_numeric)
        
        n_anomalies = list(preds).count(-1)
        return f"Unsupervised Detection: Found {n_anomalies} anomalies in dataset."
    except Exception as e:
        return f"Unsupervised error: {str(e)}"