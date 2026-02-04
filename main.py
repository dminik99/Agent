import argparse
import os
from crewai import Crew, Task, Process
from src.agents.agents import build_agents

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="file.csv", help="Path to raw CSV file")
    parser.add_argument("--label", default="attack", help="Target column name (e.g., 'class' or 'label')")
    args = parser.parse_args()

    cleaner, correlator, detector, explainer, reporter = build_agents()

    t1 = Task(
        description=f"Clean the raw file located at: {args.csv}. Save the result to 'cleaned_data.csv'.",
        expected_output="A summary of the cleaning process and the schema of the new file.",
        agent=cleaner,
        output_file="report_step1_clean.txt"
    )

    t2 = Task(
        description="Analyze 'cleaned_data.csv'. Identify the most active source IPs and potential port scanning IPs and top DoS victims.",
        expected_output="Top talkers, scan/recon suspects, and dos victims.",
        agent=correlator,
        context=[t1],
        output_file="report_step2_corr.txt"
    )

    detection_input = f"cleaned_data.csv|{args.label}" if args.label else "cleaned_data.csv"
    
    t3 = Task(
        description=(
        f"Analyze the network traffic data from: {detection_input}. "
        "1. First, use 'analyze_threat_distribution' to identify the primary threat categories and subcategories. "
        "2. If a label (like 'category') is present in the data, use 'train_and_predict_threats' to build a supervised model. "
        "3. Identify the most important technical indicators (features) that signal an attack."
        ),
        expected_output=(
        "A detailed security report including: \n"
        "- Distribution of detected threats (e.g., DoS, DDoS, Reconnaissance counts)\n"
        "- Model performance metrics (Accuracy)\n"
        "- The top 3 technical features that help in identifying these attacks."
        ),
        agent=detector,
        context=[t2],
        output_file="report_step3_detect.txt"
    )

    t4 = Task(
        description=(
        f"Analyze the results from the detection model using: {detection_input}. "
        "1. Identify the top 3-5 features (e.g., srate, stddev, N_IN_Conn_P_SrcIP) that most influenced the classification. "
        "2. For each feature, provide a human-readable technical explanation. "
        "3. Explain why these values are typical for the detected attack category (e.g., why a high 'srate' and low 'stddev' suggest a DoS/DDoS attack)."
        ),
        expected_output=(
        "A structured report containing:\n"
        "- A ranked list of the most important features.\n"
        "- Technical definitions for each (e.g., 'srate' as source-to-destination packet rate).\n"
        "- A brief section explaining the logic behind the detection."
        ),
        agent=explainer,
        context=[t3],
        output_file="report_step4_explain.txt"
)

    t5 = Task(
        description="Create a comprehensive Cyber Security Incident Report based on all previous findings. "
                    "Include: Data Quality, Suspicious Actors, Detection Accuracy, and Key Attack Indicators.",
        expected_output="A professional Markdown formatted report.",
        agent=reporter,
        context=[t1, t2, t3, t4],
        output_file="FINAL_REPORT.md"
    )

    crew = Crew(
        agents=[cleaner, correlator, detector, explainer, reporter],
        tasks=[t1, t2, t3, t4, t5],
        process=Process.sequential,
        verbose=True
    )

    print("### CREWAI SECURITY ANALYZER STARTING... ###")
    result = crew.kickoff()
    print("\n\n################# FINAL RESULT #################\n")
    print(result)

if __name__ == "__main__":
    main()