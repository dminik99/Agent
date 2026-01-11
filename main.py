import argparse
from crewai import Crew, Task, Process
from src.agents.agents import build_agents

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="ids_logs.csv", help="Path to raw CSV file")
    parser.add_argument("--label", default="class", help="Target column name (e.g., 'class' or 'label')")
    args = parser.parse_args()

    cleaner, correlator, detector, explainer, reporter = build_agents()

    t1 = Task(
        description=f"Clean the raw file located at: {args.csv}. Save the result to 'cleaned_data.csv'.",
        expected_output="A summary of the cleaning process and the schema of the new file.",
        agent=cleaner,
        output_file="report_step1_clean.txt"
    )

    t2 = Task(
        description="Analyze 'cleaned_data.csv'. Identify top talkers and potential port scanning IPs.",
        expected_output="List of suspicious IPs and connection statistics.",
        agent=correlator,
        context=[t1],
        output_file="report_step2_corr.txt"
    )

    detection_input = f"cleaned_data.csv|{args.label}" if args.label else "cleaned_data.csv"
    
    t3 = Task(
        description=f"Train a detection model using input: {detection_input}. If label is present, use supervised, else unsupervised.",
        expected_output="Model performance metrics (e.g., Accuracy, F1) or anomaly counts.",
        agent=detector,
        context=[t2],
        output_file="report_step3_detect.txt"
    )

    t4 = Task(
        description=f"Identify top features driving the attacks using input: {detection_input}.",
        expected_output="List of top features and a brief text explaining what they represent technically.",
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