import os

from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process

from tools.vcf_tools import (
    validate_vcf,
    parse_vcf,
)


# =========================================================
# Environment
# =========================================================

load_dotenv()

MODEL = os.getenv(
    "MODEL",
    "openrouter/openai/gpt-oss-20b:free"
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY is missing from .env"
    )


# =========================================================
# Agents
# =========================================================

supervisor_agent = Agent(
    role="Genomics Workflow Supervisor",

    goal=(
        "Coordinate the genomics analysis workflow and make sure "
        "each specialized agent completes its assigned stage."
    ),

    backstory=(
        "You supervise a team of specialized genomics agents. "
        "You make sure that validation happens before analysis, "
        "analysis happens before reporting, and the final report "
        "is reviewed before approval."
    ),

    llm=MODEL,

    verbose=True,
)


validation_agent = Agent(
    role="Genomic Data Validation Specialist",

    goal=(
        "Validate the uploaded VCF file before any genomic analysis "
        "takes place."
    ),

    backstory=(
        "You specialize in genomic data validation and VCF files. "
        "You inspect the actual uploaded file using Python tools. "
        "You never guess whether a VCF is valid."
    ),

    tools=[
        validate_vcf
    ],

    llm=MODEL,

    verbose=True,
)


analysis_agent = Agent(
    role="Genomic Variant Analysis Specialist",

    goal=(
        "Analyze validated genomic variants and extract their "
        "basic genomic information."
    ),

    backstory=(
        "You specialize in genomic variant analysis. "
        "You work only with information extracted from the actual "
        "VCF file and never invent genomic evidence."
    ),

    tools=[
        parse_vcf
    ],

    llm=MODEL,

    verbose=True,
)


literature_agent = Agent(
    role="Scientific Literature Researcher",

    goal=(
        "Research scientific evidence related to genes and variants "
        "identified during genomic analysis."
    ),

    backstory=(
        "You specialize in biomedical literature research. "
        "You summarize scientific evidence and clearly distinguish "
        "available evidence from information that was not found."
    ),

    llm=MODEL,

    verbose=True,
)


writer_agent = Agent(
    role="Genomics Report Writer",

    goal=(
        "Create a clear and structured genomics analysis report."
    ),

    backstory=(
        "You write scientific reports using the results produced by "
        "the other agents. You separate observed variant data from "
        "external scientific evidence and clearly state limitations."
    ),

    llm=MODEL,

    verbose=True,
)


critic_agent = Agent(
    role="Genomics Report Critic",

    goal=(
        "Review the final genomics report for accuracy, consistency, "
        "missing information, and unsupported claims."
    ),

    backstory=(
        "You are a strict scientific reviewer. You check whether "
        "claims are supported by the available evidence and identify "
        "anything that should be corrected before final approval."
    ),

    llm=MODEL,

    verbose=True,
)


# =========================================================
# Tasks
# =========================================================

validation_task = Task(
    description="""
    Validate the uploaded VCF file.

    The file path will be provided at runtime.

    IMPORTANT:
    You MUST use the validate_vcf tool to inspect the actual file.

    Check:
    - File existence
    - VCF readability
    - VCF structure
    - Presence of variant records
    - Number of variants
    - Obvious validation problems

    Do not guess.

    Return a clear validation result and state whether
    the workflow can continue.
    """,

    expected_output="""
    A validation report containing:

    - VALID or INVALID
    - Number of variants
    - Detected problems
    - Whether analysis can continue
    """,

    agent=validation_agent,
)


analysis_task = Task(
    description="""
    Analyze the VCF after successful validation.

    IMPORTANT:
    You MUST use the parse_vcf tool to read the actual VCF file.

    Extract available information such as:

    - Chromosome
    - Position
    - Reference allele
    - Alternative allele

    Do not invent genes, diseases, clinical significance,
    or other genomic evidence.

    Only report information actually available from the file
    or from verified external sources.
    """,

    expected_output="""
    A structured variant analysis containing:

    - Number of variants
    - Variant information
    - Available genomic information
    - Any limitations
    """,

    agent=analysis_agent,

    context=[
        validation_task
    ],
)


literature_task = Task(
    description="""
    Review the results of the genomic analysis.

    Identify relevant genes or variants that require
    scientific literature research.

    For each relevant item:

    - Identify the gene or variant
    - Search for scientific evidence when tools are available
    - Summarize relevant evidence
    - Clearly identify the source
    - Do not invent publications or evidence

    If no literature evidence is available, state that clearly.
    """,

    expected_output="""
    A literature evidence summary containing:

    - Gene or variant
    - Relevant scientific evidence
    - Source information
    - Short explanation
    - Evidence limitations
    """,

    agent=literature_agent,

    context=[
        analysis_task
    ],
)


writing_task = Task(
    description="""
    Create a structured genomics analysis report.

    Use the validation, analysis, and literature results.

    The report should contain:

    1. Input summary
    2. Validation result
    3. Variant analysis
    4. Gene/disease evidence
    5. Literature evidence
    6. Limitations
    7. Sources

    Clearly separate:

    - Information directly observed from the VCF
    - Information obtained from external sources

    Never make a medical diagnosis.

    Use cautious scientific language such as:

    "This variant has been associated with..."

    rather than:

    "The patient has this disease."
    """,

    expected_output="""
    A clear structured genomics research report
    containing findings, evidence, sources, and limitations.
    """,

    agent=writer_agent,

    context=[
        validation_task,
        analysis_task,
        literature_task,
    ],
)


critic_task = Task(
    description="""
    Critically review the generated genomics report.

    Check:

    - Factual consistency
    - Unsupported claims
    - Missing information
    - Contradictions
    - Source relevance
    - Separation between observed data and external evidence
    - Medical safety

    Return:

    PASS

    if the report is acceptable.

    Otherwise return:

    NEEDS_REVISION

    followed by concise revision comments.
    """,

    expected_output="""
    PASS

    or

    NEEDS_REVISION

    followed by specific review comments.
    """,

    agent=critic_agent,

    context=[
        writing_task
    ],
)


# =========================================================
# Crew
# =========================================================

crew = Crew(
    agents=[
        supervisor_agent,
        validation_agent,
        analysis_agent,
        literature_agent,
        writer_agent,
        critic_agent,
    ],

    tasks=[
        validation_task,
        analysis_task,
        literature_task,
        writing_task,
        critic_task,
    ],

    process=Process.sequential,

    verbose=True,
)


# =========================================================
# Run
# =========================================================

def run_crew(file_path: str):

    if not file_path:
        return "No VCF file was provided."

    result = crew.kickoff(
        inputs={
            "file_path": file_path
        }
    )

    return result


if __name__ == "__main__":

    print("=" * 60)
    print("GENOMICS VARIANT ANALYSIS")
    print("=" * 60)

    file_path = input(
        "\nEnter the path to your VCF file: "
    ).strip()

    result = run_crew(file_path)

    print("\n")
    print("=" * 60)
    print("FINAL RESULT")
    print("=" * 60)

    print(result)