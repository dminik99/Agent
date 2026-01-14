import pandas as pd
import numpy as np
from crewai.tools import tool

@tool("clean_dataframe")
def clean_dataframe(input_csv_path: str) -> str:
    """
    Beolvassa a CSV fájlt a megadott útvonalról, elvégzi az adattisztítást 
    (hiányzó értékek pótlása, oszlopnevek javítása), és elmenti az eredményt 
    egy 'cleaned_data.csv' fájlba. Visszatér a művelet eredményével.
    """
    try:
        # 1. Beolvasás
        df = pd.read_csv(input_csv_path)
        
        # 2. Standardizálás
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        
        # 3. Hiányzó adatok kezelése (csak numerikus oszlopokon)
        for col in df.select_dtypes(include=[np.number]).columns:
            df[col] = df[col].fillna(df[col].median())
        
        # 4. Mentés
        output_path = "cleaned_data.csv"
        df.to_csv(output_path, index=False)
        
        # Schema info generálása szövegesen
        schema_info = {c: str(t) for c, t in df.dtypes.items()}
        
        return f"SUCCESS. Data cleaned and saved to '{output_path}'. Original rows: {len(df)}. Schema: {schema_info}"
    except Exception as e:
        return f"Error during cleaning: {str(e)}"