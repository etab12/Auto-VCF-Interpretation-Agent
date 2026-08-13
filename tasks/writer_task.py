from crewai import Task
from agents.writer import writer_agent

writer_task = Task(
    description=(
        "Write a Markdown genomics report from the analysis and research results.\n\n"
        "Use EXACTLY these section headers in this order:\n"
        "## Summary\n"
        "## Variants Identified\n"
        "## Gene and Disease Evidence\n"
        "## Literature Review\n"
        "## Limitations\n"
        "## Sources\n\n"
        "Rules:\n"
        "- In 'Variants Identified': use a Markdown table with columns: "
        "Chromosome | Position | Ref | Alt | Gene | Clinical Significance.\n"
        "- In 'Gene and Disease Evidence': include each ClinVar link as "
        "[VCV accession](url), e.g. [VCV000479296](https://www.ncbi.nlm.nih.gov/clinvar/variation/479296/)\n"
        "- In 'Literature Review': include each paper as a bullet with "
        "[PMID](url), title, journal. e.g. [PMID 39072245](https://pubmed.ncbi.nlm.nih.gov/39072245/)\n"
        "- Label each fact as **[From VCF]** or **[From external source]**.\n"
        "- Do not make a medical diagnosis.\n"
        "- Do not add unsupported claims."
    ),
    expected_output=(
        "A Markdown report with six ## sections, a variants table, inline "
        "ClinVar and PubMed links, and clear source labelling."
    ),
    agent=writer_agent,
)