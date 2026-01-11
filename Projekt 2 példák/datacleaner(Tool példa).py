from typing import Tuple, Dict
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field
from crewai.tools import tool


class Schema(BaseModel):
    columns: Dict[str, str] = Field(..., description="Oszlopnév -> dtype mapping")
    n_rows: int
    notes: str = ""


def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Egységes kisbetűs és '_' elválasztás
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def _coerce_timestamps(df: pd.DataFrame) -> pd.DataFrame:
    # Próbáljunk 'timestamp' vagy 'time' jellegű oszlopokat datetime-á alakítani
    df = df.copy()
    for col in df.columns:
        if any(k in col for k in ["time", "timestamp", "date"]):
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)
            except Exception:
                pass
    return df


def _fill_missing(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = df[col].fillna(df[col].median())
    for col in df.select_dtypes(exclude=[np.number]).columns:
        df[col] = df[col].fillna("unknown")
    return df


@tool("clean_dataframe")
def clean_dataframe(input_csv_path: str) -> Tuple[pd.DataFrame, Schema]:
    """Olvass be egy CSV-t és végezz alap adattisztítást (oszlop-normalizálás,
    időbélyegek konvertálása, hiányzó értékek pótlása). Visszatér: (df, schema)."""
    df = pd.read_csv(input_csv_path)
    df = _standardize_columns(df)
    df = _coerce_timestamps(df)
    df = _fill_missing(df)
    # dtype összefoglaló
    schema = Schema(
        columns={c: str(t) for c, t in df.dtypes.items()},
        n_rows=len(df),
        notes="Automatikus tisztítás lefutott.",
    )
    return df, schema
