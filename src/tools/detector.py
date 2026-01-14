import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from crewai.tools import tool

def _prepare_data(df, label_col=None):
    """Segédfüggvény az adatok tisztítására a modell számára."""
    garbage_cols = ['pkseqid', 'seq', 'id', 'stime', 'ltime', 'timestamp']
    cols_to_drop = [c for c in garbage_cols if c in df.columns]
    
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
        print(f"DEBUG: Dropped garbage columns: {cols_to_drop}")

    le = LabelEncoder()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = le.fit_transform(df[col].astype(str))
        
    return df

@tool("train_supervised_detector")
def train_supervised_detector(csv_path_and_label: str) -> str:
    """
    Felügyelt ML modell tanítása. A 'pkseqid' azonosítót automatikusan eldobja.
    Bemenet: 'fajl_utvonal.csv|cel_valtozo_neve'.
    """
    try:
        if '|' not in csv_path_and_label:
            return "Error: Input must be 'filepath.csv|label_column'"
            
        path, label_col = csv_path_and_label.split('|')
        df = pd.read_csv(path)
        
        if label_col not in df.columns:
            return f"Error: Label column '{label_col}' not found."

        df = _prepare_data(df, label_col)
            
        X = df.drop(columns=[label_col])
        y = df[label_col]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        clf = RandomForestClassifier(n_estimators=10)
        clf.fit(X_train, y_train)
        
        score = clf.score(X_test, y_test)
        
        return f"Supervised Model Trained (Garbage dropped). Accuracy: {score:.2f}"
    except Exception as e:
        return f"Supervised training error: {str(e)}"

@tool("train_unsupervised_iforest")
def train_unsupervised_iforest(csv_path: str) -> str:
    """
    Unsupervised anomália detektálás. A 'pkseqid' azonosítót automatikusan eldobja.
    """
    try:
        df = pd.read_csv(csv_path)
        
        df = _prepare_data(df)
        
        df_numeric = df.select_dtypes(include=['number']).fillna(0)
        
        iso = IsolationForest(contamination=0.05, random_state=42)
        preds = iso.fit_predict(df_numeric)
        
        n_anomalies = list(preds).count(-1)
        return f"Unsupervised Detection Complete. Found {n_anomalies} anomalies."
    except Exception as e:
        return f"Unsupervised error: {str(e)}"