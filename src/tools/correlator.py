import pandas as pd
from crewai.tools import tool

@tool("correlate_events")
def correlate_events(csv_path: str) -> str:
    """
    IP címek és portok alapján keres összefüggéseket a 'file.csv'-ben.
    Kifejezetten a 'saddr' (Source Address) és 'dport' (Destination Port) oszlopokat figyeli.
    Jelzi a legtöbbet kommunikáló IP-ket (Top Talkers) és a port scan gyanút.
    """
    try:
        df = pd.read_csv(csv_path)
        possible_src_cols = ['saddr', 'src_ip', 'source_address', 'source']
        src_col = next((c for c in possible_src_cols if c in df.columns), None)
        
        possible_port_cols = ['dport', 'dst_port', 'dest_port', 'destination_port']
        port_col = next((c for c in possible_port_cols if c in df.columns), None)

        if not src_col:
            return f"Error: Could not find Source IP column. Checked: {possible_src_cols}. Found: {list(df.columns)}"

        top_src = df[src_col].value_counts().head(5).to_dict()
        
        msg = f"Correlation Report on '{src_col}':\n- Top 5 Talkers: {top_src}\n"

        if port_col:
            scanners = df.groupby(src_col)[port_col].nunique()
            suspicious = scanners[scanners > 10].head(5).to_dict()
            msg += f"- Suspicious Scanners (connecting to >10 ports): {suspicious}"
        else:
            msg += "- Port scan check skipped (no destination port column found)."

        return msg
    except Exception as e:
        return f"Correlation failed: {str(e)}"