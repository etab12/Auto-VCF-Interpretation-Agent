from crewai import Task
from agents.supervisor import supervisor_agent

supervisor_task = Task(
    description=(
        "Supervise the complete genomics analysis workflow. "
        "Review the results produced by the specialized agents and ensure "
        "that the analysis, research, report writing, and criticism stages "
        "are completed correctly.\n\n"
        "Approve the final report only when the required stages are complete "
        "and the report is supported by evidence."
    ),
    expected_output=(
        "A final workflow status indicating whether the report is approved "
        "and ready to present."
    ),
    agent=supervisor_agent,
)