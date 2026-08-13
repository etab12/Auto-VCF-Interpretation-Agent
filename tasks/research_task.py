from crewai import Task
from agents.research import research_agent

research_task = Task(
    description=(
        "Using the variants and genes identified by the analysis agent, "
        "search reliable scientific literature for relevant evidence.\n\n"
        "Focus on relevant genes, variants, and possible gene-disease "
        "relationships. Use reliable scientific sources such as PubMed/NCBI.\n\n"
        "For each relevant source, provide the title or identifier when "
        "available and a short explanation of the relevant evidence.\n\n"
        "Do not invent papers, identifiers, or scientific claims."
    ),
    expected_output=(
        "A structured list of relevant scientific sources with identifiers "
        "when available and concise summaries of their relevant evidence."
    ),
    agent=research_agent,
)