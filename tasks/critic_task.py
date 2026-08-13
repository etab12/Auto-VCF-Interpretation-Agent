from crewai import Task
from agents.critic import critic_agent

critic_task = Task(
    description=(
        "Review the generated genomics report.\n\n"
        "Check:\n"
        "- Factual consistency\n"
        "- Unsupported claims\n"
        "- Missing information\n"
        "- Incorrect interpretation\n"
        "- Source relevance\n"
        "- Whether conclusions are supported by the evidence\n"
        "- Whether limitations are clearly stated\n\n"
        "Return PASS if the report is acceptable.\n"
        "Return NEEDS_REVISION if changes are required and provide concise "
        "revision comments."
    ),
    expected_output=(
        "Either PASS or NEEDS_REVISION followed by concise review comments."
    ),
    agent=critic_agent,
)