import pandas as pd
from crewai.tools import tool

@tool("correlate_events")
def correlate_events(csv_path: str) -> str:
    """
    IP címek és portok alapján keres összefüggéseket a 'cleaned_data.csv'-ben.
    - Legaktívabb forrás IP-k
    - Recon scan gyanús források
    - Top DoS/DDoS cél IP-k
    """
    try:
        # Inicializáció, oszlopok betöltése, csak támadások figyelembe vétele, output formatálás
        df = pd.read_csv(csv_path)
        required = ["pkseqid", "proto", "saddr", "sport", "daddr", "dport", "attack", "category", "subcategory"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            return f"Error: missing columns: {missing}. Found: {list(df.columns)}"
        
        mal = df[df["attack"] == 1].copy()

        def format_records(records):
            if not records:
                return "  (none)"
            return "\n".join([f"  - {r}" for r in records])

        # --- Top talkers: Forrás IP + kapcsolatok száma ---
        talkers = (
            mal.groupby("saddr")
            .size()
            .sort_values(ascending=False)
            .head(5)
            .reset_index(name="connections")
            .to_dict(orient="records")
        )

        # --- Reconnaisance scan  ---
        recon = mal[mal["category"] == "Reconnaissance"].copy()
        if recon.empty:
            scan_suspects = []
        else:
            stats = recon.groupby("saddr").agg(
                unique_ports=("dport", pd.Series.nunique),
                unique_dsts=("daddr", pd.Series.nunique),
            ).sort_values(["unique_ports", "unique_dsts"], ascending=False)

            scan_suspects = stats[
                (stats["unique_ports"] >= 30) |
                (stats["unique_dsts"] >= 10)
            ].head(5).reset_index().to_dict(orient="records")

        # --- Top 5 DoS/DDoS célpontok ---
        dos_df = mal[mal["category"].isin(["DoS", "DDoS"])].copy()
        if dos_df.empty:
            top_dos_victims = []
        else:
            counts = (
                dos_df.groupby(["daddr", "category"])
                .size()
                .unstack(fill_value=0)
            )
            if "DoS" not in counts.columns:
                counts["DoS"] = 0
            if "DDoS" not in counts.columns:
                counts["DDoS"] = 0

            counts["total_connections"] = counts["DoS"] + counts["DDoS"]
            counts = counts.sort_values("total_connections", ascending=False).head(5)

            top_dos_victims = (
                counts.reset_index()
                .rename(columns={"DoS": "dos_connections", "DDoS": "ddos_connections"})
                [["daddr", "dos_connections", "ddos_connections", "total_connections"]]
                .to_dict(orient="records")
            )

        msg = []
        msg.append("Correlation Report (cleaned_data.csv)")
        msg.append("- Legaktívabb forrás IP-k (attack=1; connections):")
        msg.append(format_records(talkers))
        msg.append(f"- Recon scan gyanús források (Connected to +30 ports OR +10 IPs):")
        msg.append(format_records(scan_suspects))
        msg.append("- Top 5 DoS/DDoS cél IP-k (connections):")
        msg.append(format_records(top_dos_victims))
        return "\n".join(msg)

    except Exception as e:
        return f"Correlation failed: {str(e)}"