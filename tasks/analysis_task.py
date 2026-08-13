from crewai import Task
from agents.analysis import analysis_agent

analysis_task = Task(
    description=(
        "Validate and analyze the uploaded VCF file.\n\n"
        "First verify that the file is readable and follows the expected "
        "VCF structure. Check required fields and identify obvious structural "
        "problems.\n\n"
        "If the file is valid, analyze the variants and extract relevant "
        "information including chromosome, position, reference allele, "
        "alternative allele, gene, and other available fields.\n\n"
        "Identify available gene or disease-related evidence when possible. "
        "Do not invent information. If information is unavailable, state that "
        "clearly."
    ),
    expected_output=(
        "A structured analysis containing VCF validation results, detected "
        "issues if any, relevant variants, genes, and available disease-related "
        "evidence."
    ),
    agent=analysis_agent,
)