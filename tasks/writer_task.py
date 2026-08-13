from crewai import Task
from agents.writer import writer_agent

writer_task = Task(
    description=(
        "Write a plain text genomics report from the analysis and research results.\n\n"
        "Use EXACTLY these section titles in this order:\n"
        "SUMMARY\n"
        "VARIANTS IDENTIFIED\n"
        "GENE AND DISEASE EVIDENCE\n"
        "LITERATURE REVIEW\n"
        "LIMITATIONS\n"
        "SOURCES\n\n"
        "Rules:\n"
        "- In 'VARIANTS IDENTIFIED': list chromosome, position, ref, alt, gene, "
        "and clinical significance for each variant.\n"
        "- In 'GENE AND DISEASE EVIDENCE': include the full ClinVar URL for each "
        "variant, e.g. https://www.ncbi.nlm.nih.gov/clinvar/variation/479296/\n"
        "- In 'LITERATURE REVIEW': include the full PubMed URL for each paper, "
        "e.g. https://pubmed.ncbi.nlm.nih.gov/12345678/\n"
        "- Clearly label each fact as [From VCF] or [From external source].\n"
        "- Do not make a medical diagnosis.\n"
        "- Do not add unsupported claims."
    ),
    expected_output=(
        "A plain text report with the six required sections, full ClinVar and "
        "PubMed URLs, and clear separation between VCF-observed data and "
        "external evidence."
    ),
    agent=writer_agent,
)