import argparse
from crewai import Crew, Task, Process
from src.agents.agents import build_agents


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help=".CSV file with appropriata data")
    parser.add_argument(
        "--label",
        required=False,
        default=None,
        help="Label column used for supervised learning",
    )
    args = parser.parse_args()
    data_cleaner, correlator, detector, explainer, random = build_agents()

    t1 = Task(
        description=f"Clean the CSV and create the scheme for the following file: {args.csv}",
        expected_output="(df, schema) the whole pandas DataFrame including every row and JSON-scheme summary.",
        agent=data_cleaner,
        output_file="./results/task1.txt",
        input=args.csv,
    )
    t2 = Task(
        description=f"Create IP-correlations and sample paths based on the following file: {args.csv} ",
        expected_output="JSON staticstics of n_nodes, n_edges, sample_paths.",
        agent=correlator,
        output_file="./results/task2.txt",
        input=args.csv,
        context=[t1],
    )
    tasks = [t1, t2]

    if args.label:
        t3 = Task(
            description=(
                f"Train a supervised detector and report metrics: path={args.csv} label={args.label}."
                "Explain what each metric is supposed to mean."
            ),
            expected_output="JSON metrics: f1, precision, recall, roc_auc. Short, concise explanation of what each metric means.",
            agent=detector,
            output_file="./results/task3.txt",
            input=f"{args.csv}|{args.label}",
        )
        t4 = Task(
            description=(
                f"Create a top-10 feature list for the explanation: path={args.csv} label={args.label}."
            ),
            expected_output="JSON list with (feature, importance) pairs.",
            agent=explainer,
            output_file="./results/task4.txt",
            input=f"{args.csv}|{args.label}",
        )
        t5 = Task(
            description=(
                "Use the output from task 4 and then explain, how each result came to be, and what they mean exactly."
                "For each feature explain the exact meaning of it in at least one sentence. Do not write any code, just explain in a clear and concise way."
            ),
            agent=random,
            context=[t4],
            expected_output="Plaint text explanation of what each feature means, and how important they are.",
            output_file="./results/task5.txt",
        )
        tasks.extend([t3, t4, t5])

    crew = Crew(
        agents=[data_cleaner, correlator, detector, explainer],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )
    result = crew.kickoff()
    print("\n===== CREW RESULT =====\n")
    print(result)


if __name__ == "__main__":
    main()
