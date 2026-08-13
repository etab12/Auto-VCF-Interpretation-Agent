from crewai import Agent

critic_agent = Agent(
    role="Genomics Report Critic",
    goal=(
        "Review the final genomics report for accuracy, consistency, "
        "missing information, and unsupported claims."
    ),
    backstory=(
        "You are a strict scientific reviewer. You check whether the report "
        "is supported by the provided analysis and research evidence. "
        "You identify unsupported claims, missing sources, contradictions, "
        "and unclear statements."
    ),
    verbose=True,
)