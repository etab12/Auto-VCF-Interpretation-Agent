from crewai import Task

from agents.research import research_agent
from tasks.analysis_task import analysis_task


research_task = Task(
    description=(
        "Review the results produced by the Analysis Agent and identify the "
        "relevant genes and genomic variants that require scientific research.\n\n"

        "For each relevant gene or variant:\n"
        "1. Use the provided research tool to search scientific literature.\n"
        "2. Prefer reliable sources such as PubMed/NCBI.\n"
        "3. Identify relevant papers and scientific evidence.\n"
        "4. Provide PMID or other source identifiers when available.\n"
        "5. Provide source links when available.\n"
        "6. Summarize the evidence accurately.\n"
        "7. Clearly distinguish retrieved evidence from interpretation.\n"
        "8. If relevant evidence cannot be found, state: "
        "'No relevant evidence found.'\n\n"

        "Do not rely on memory for specific papers or PMID numbers. "
        "Do not invent missing information. "
        "Do not make a medical diagnosis. "
        "Do not claim that a variant causes a disease unless the retrieved "
        "scientific evidence explicitly supports that statement.\n\n"

        "The Analysis Agent output is provided as context. "
        "Use it to determine which genes and variants should be researched."
    ),

    expected_output=(
        "A structured literature research result containing, when available:\n"
        "- Gene\n"
        "- Variant\n"
        "- Disease or condition\n"
        "- Evidence summary\n"
        "- PMID or source identifier\n"
        "- Source/link\n"
        "- Evidence limitations\n\n"
        "Clearly distinguish retrieved scientific evidence from interpretation. "
        "If no relevant evidence is found, explicitly state "
        "'No relevant evidence found.'"
    ),

    agent=research_agent,

    context=[analysis_task],
)