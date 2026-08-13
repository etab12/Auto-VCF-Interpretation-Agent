from pathlib import Path

from crewai import Agent

# Load the reporting skill so the writer knows how to structure evidence
_SKILL = (
    Path(__file__).parent.parent
    / "skills"
    / "gene_disease_literature_evidence.md"
).read_text(encoding="utf-8")

writer_agent = Agent(
    role="Genomics Report Writer",
    goal=(
        "Create a clear, well-structured plain text report using the verified "
        "analysis and research results, with full source URLs."
    ),
    backstory=(
        "You are a scientific report writer specialising in genomics. "
        "You combine genomic variant analysis and literature findings into a "
        "readable Markdown report. You clearly separate information directly "
        "observed in the VCF from external scientific evidence, include "
        "inline PMID and ClinVar links, and state limitations explicitly. "
        "You follow evidence-evaluation principles from your skill guide.\n\n"
        + _SKILL
    ),
    verbose=True,
)