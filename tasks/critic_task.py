from crewai import Task
from agents.critic import critic_agent
from tasks.writer_task import writer_task

critic_task = Task(
    description=(
        "Review the generated genomics report from the Writer Agent.\n\n"
        "Check:\n"
        "- Factual consistency\n"
        "- Unsupported claims\n"
        "- Missing information\n"
        "- Incorrect interpretation\n"
        "- Source relevance\n"
        "- Whether conclusions are supported by the evidence\n"
        "- Whether limitations are clearly stated\n\n"
        "If the report is acceptable: write PASS on the first line, then output "
        "the full report exactly as written by the Writer Agent without any changes.\n"
        "If changes are required: write NEEDS_REVISION on the first line, followed "
        "by concise revision comments."
    ),
    expected_output=(
        "Either:\n"
        "PASS\n<full report text>\n\n"
        "or:\n"
        "NEEDS_REVISION\n<revision comments>"
    ),
    agent=critic_agent,
    context=[writer_task],
)