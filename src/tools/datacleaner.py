import pandas as pd
import numpy as np
from crewai.tools import tool

@tool("clean_dataframe")
def clean_dataframe(input_csv_path: str) -> str:
    try:
        df = pd.read_csv(input_csv_path)
        
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        
        for col in df.select_dtypes(include=[np.number]).columns:
            df[col] = df[col].fillna(df[col].median())
        
        output_path = "cleaned_data.csv"
        df.to_csv(output_path, index=False)
        
        schema_info = {c: str(t) for c, t in df.dtypes.items()}
        return f"SUCCESS. Data cleaned and saved to '{output_path}'. Original rows: {len(df)}. Schema: {schema_info}"
    except Exception as e:
        return f"Error during cleaning: {str(e)}"