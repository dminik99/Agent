import pandas as pd
from crewai.tools import tool

@tool("correlate_events")
def correlate_events(csv_path: str) -> str:
    try:
        df = pd.read_csv(csv_path)
        required_cols = ['src_ip', 'dst_ip', 'dst_port']
        if not all(col in df.columns for col in required_cols):
            return f"Error: Missing columns for correlation. Required: {required_cols}. Found: {df.columns.tolist()}"
            
        top_src = df['src_ip'].value_counts().head(5).to_dict()
        
        port_scan_candidates = df.groupby('src_ip')['dst_port'].nunique()
        suspicious_ips = port_scan_candidates[port_scan_candidates > 10].head(5).index.tolist() # Pl. >10 port
        
        return (f"Correlation Report:\n"
                f"- Top 5 Source IPs: {top_src}\n"
                f"- Suspicious IPs (Port Scan behavior): {suspicious_ips}\n"
                f"Data analyzed from: {csv_path}")
    except Exception as e:
        return f"Correlation failed: {str(e)}"