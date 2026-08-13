from crewai import Agent

supervisor_agent = Agent(
    role="Genomics Workflow Supervisor",
    goal=(
        "Coordinate the genomics analysis workflow and ensure that each "
        "stage is completed correctly before the final report is approved."
    ),
    backstory=(
        "You supervise a team of specialized genomics agents. You monitor "
        "their results, ensure information moves correctly between stages, "
        "request revisions when necessary, and approve the final report."
    ),
    verbose=True,
)