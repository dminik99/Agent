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
        df = pd.read_csv(input_csv_path)

        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        
        target_columns = ['pkseqid', 'proto', 'saddr', 'sport', 'daddr', 'dport', 'n_in_conn_p_srcip', 'n_in_conn_p_dstip', 'attack', 'category', 'subcategory']
        
        df = df[target_columns]
        
        for col in df.select_dtypes(include=[np.number]).columns:
            df[col] = df[col].fillna(df[col].median())
        
        output_path = "cleaned_data.csv"
        
              
        #df['NNN'] = df['NNN'].round(5)
        
        
        
        df.to_csv(output_path, index=False)
        
        schema_info = {c: str(t) for c, t in df.dtypes.items()}
        
        return f"SUCCESS. Data cleaned and saved to '{output_path}'. Original rows: {len(df)}. Schema: {schema_info}"
    except Exception as e:
        return f"Error during cleaning: {str(e)}"