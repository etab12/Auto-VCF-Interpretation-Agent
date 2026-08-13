from crewai import Task
from agents.writer import writer_agent

writer_task = Task(
    description=(
        "Create a structured genomics analysis report using the previous "
        "VCF analysis and scientific research results.\n\n"
        "Include:\n"
        "- VCF validation result\n"
        "- Relevant variants\n"
        "- Relevant genes\n"
        "- Disease-related evidence\n"
        "- Scientific literature\n"
        "- Sources\n"
        "- Limitations\n\n"
        "Clearly distinguish information directly observed in the VCF from "
        "information obtained from external scientific sources.\n\n"
        "Do not make a medical diagnosis and do not add unsupported claims."
    ),
    expected_output=(
        "A clear, structured genomics analysis report containing verified "
        "findings, scientific evidence, sources, and limitations."
    ),
    agent=writer_agent,
)