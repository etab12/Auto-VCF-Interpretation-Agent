from crewai import Agent, Task, Crew, Process


# =========================
# Agents
# =========================

supervisor_agent = Agent(
    role="Supervisor",
    goal="Manage the genomics analysis workflow and ensure all stages are completed correctly.",
    backstory=(
        "You are a supervisor responsible for coordinating a team of specialized "
        "genomics agents. You review their outputs and make sure the final report "
        "is complete and consistent."
    ),
    verbose=True
)

validation_agent = Agent(
    role="Genomic Data Validation Specialist",
    goal="Validate the uploaded VCF data before analysis.",
    backstory=(
        "You specialize in checking genomic data quality and VCF structure. "
        "Your job is to identify invalid or incomplete input data before analysis begins."
    ),
    verbose=True
)

analysis_agent = Agent(
    role="Genomic Variant Analysis Specialist",
    goal="Analyze genomic variants and identify relevant gene and disease evidence.",
    backstory=(
        "You specialize in genomic variant analysis. You examine validated variants "
        "and identify relevant genetic and disease-related information without "
        "inventing unsupported evidence."
    ),
    verbose=True
)

literature_agent = Agent(
    role="Scientific Literature Researcher",
    goal="Find scientific evidence related to relevant genes and genomic variants.",
    backstory=(
        "You specialize in biomedical literature research. You search scientific "
        "sources such as PubMed and summarize relevant evidence."
    ),
    verbose=True
)

writer_agent = Agent(
    role="Medical Report Writer",
    goal="Create a clear and structured report from the analysis and literature results.",
    backstory=(
        "You specialize in writing clear scientific reports. You combine verified "
        "results while clearly separating observed data from external evidence."
    ),
    verbose=True
)

critic_agent = Agent(
    role="Report Critic",
    goal="Review the generated report for accuracy, consistency, and unsupported claims.",
    backstory=(
        "You are a critical reviewer. You identify missing information, contradictions, "
        "unsupported claims, and problems with the sources used in the report."
    ),
    verbose=True
)


# =========================
# Tasks
# =========================

validation_task = Task(
    description=(
        "Validate the provided VCF input. Check whether the file is readable, "
        "has the required VCF structure, and contains usable genomic variant data. "
        "Report any problems found."
    ),
    expected_output=(
        "A validation result stating whether the VCF is valid, "
        "along with any detected issues."
    ),
    agent=validation_agent
)

analysis_task = Task(
    description=(
        "Analyze the genomic variants after successful validation. "
        "Extract relevant variant information and identify available "
        "gene and disease-related evidence."
    ),
    expected_output=(
        "A structured summary of the relevant variants, genes, "
        "and available disease-related evidence."
    ),
    agent=analysis_agent
)

literature_task = Task(
    description=(
        "Research the relevant genes and variants identified during analysis. "
        "Find supporting scientific literature and summarize the relevant evidence."
    ),
    expected_output=(
        "A list of relevant scientific evidence with short summaries "
        "and source identifiers when available."
    ),
    agent=literature_agent
)

writing_task = Task(
    description=(
        "Create a structured final report using the validation, variant analysis, "
        "and literature research results. Clearly separate observed data from "
        "external evidence and include limitations."
    ),
    expected_output=(
        "A clear and structured genomics analysis report with sources "
        "and limitations."
    ),
    agent=writer_agent
)

critic_task = Task(
    description=(
        "Review the generated report. Check factual consistency, missing information, "
        "unsupported claims, and source relevance. Return PASS if the report is ready "
        "or NEEDS_REVISION with specific comments."
    ),
    expected_output=(
        "PASS or NEEDS_REVISION, followed by concise review comments."
    ),
    agent=critic_agent
)


# =========================
# Crew
# =========================

crew = Crew(
    agents=[
        supervisor_agent,
        validation_agent,
        analysis_agent,
        literature_agent,
        writer_agent,
        critic_agent
    ],
    tasks=[
        validation_task,
        analysis_task,
        literature_task,
        writing_task,
        critic_task
    ],
    process=Process.sequential,
    verbose=True
)


# =========================
# Run
# =========================

if __name__ == "__main__":

    result = crew.kickoff()

    print("\n")
    print("=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    print(result)