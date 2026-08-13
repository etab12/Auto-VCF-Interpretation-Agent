"""Analyst agent: variant QC + VEP annotation.

Runs after the validation agent. Takes the .vcf.gz the validator cleared,
applies the QC rules in skills/qc.md, then annotates through the Ensembl VEP
REST API following skills/annotation.md.

"""

import os
from functools import lru_cache

from crewai import Agent, Task
from dotenv import load_dotenv

from tools.qc_tool import vcf_qc_stats
from tools.vep_tool import vep_annotate

load_dotenv()

MODEL = os.getenv("MODEL", "openrouter/openai/gpt-oss-20b:free")

# Analyst.py lives at <root>/src/<package>/Analyst.py
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
SKILLS_DIR = os.getenv("SKILLS_DIR", os.path.join(PROJECT_ROOT, "skills"))


# =========================================================
# Skill loading
# =========================================================

@lru_cache(maxsize=None)
def load_skill(name):
    """Read a markdown skill by name ('qc' -> skills/qc.md).

    Braces are escaped because CrewAI interpolates task descriptions with
    .format(**inputs) at kickoff - an unescaped '{' in the markdown (a JSON
    example, a table template) would raise KeyError.
    """
    stem = name[:-3] if name.lower().endswith(".md") else name
    candidates = [
        os.path.join(SKILLS_DIR, stem + ".md"),
        os.path.join(os.path.dirname(__file__), "skills", stem + ".md"),
        os.path.join(PROJECT_ROOT, stem + ".md"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as fh:
                text = fh.read().strip()
            return text.replace("{", "{{").replace("}", "}}")
    raise FileNotFoundError(
        "Skill '%s.md' not found. Looked in: %s. Set SKILLS_DIR to override."
        % (stem, ", ".join(candidates))
    )


def _skill_block(name, label):
    """Wrap skill text in delimiters so the model treats it as spec, not prose."""
    return (
        "<{0}_SKILL source=\"{1}.md\">\n{2}\n</{0}_SKILL>\n\n"
        "The {0} skill above is the complete specification for this task. "
        "Follow its thresholds, rules and report structure exactly. They "
        "override any default assumptions you have.\n\n"
        .format(label, name, load_skill(name))
    )

#=========Agent======================

analysis_agent = Agent(
    role="Genomic Variant Analysis Specialist",
    goal=(
        "Perform quality control, basic filtering, and annotation of an input "
        "VCF using the available genomics tools and skills, then produce "
        "structured variant results for downstream analysis."
    ),
    backstory=(
        "You are a bioinformatics specialist responsible for the first stage "
        "of the genomic variant analysis workflow. You evaluate VCF quality, "
        "apply appropriate basic filtering, and annotate retained variants "
        "using the available tools. You follow the QC and annotation skills "
        "provided to you, preserve variant traceability, report missing or "
        "failed annotations, and never invent genomic or clinical evidence. "
        "Your results are passed to downstream agents for disease-evidence "
        "research and interpretation."
    ),

    llm=MODEL,
    allow_delegation=False,
    max_iter=8,
    verbose=True,
)



# =========================================================
# Tasks
# =========================================================

def build_qc_task(context=None, output_file=None):
    """QC pass. All rules live in skills/qc.md."""
    return Task(
        description=(
            _skill_block("qc", "QC") +
            "The VCF to assess is: {file_path}\n\n"
            "1. Check the validation result in your context. If the file was "
            "reported INVALID, stop and report that instead of running QC.\n"
            "2. Call the vcf_qc_stats tool with vcf_path={file_path}\n"
            "3. Produce the QC report exactly as the QC skill specifies.\n"
        ),
        expected_output=(
            "A QC report following the section structure defined in the QC "
            "skill, ending with a VERDICT line."
        ),
        agent=analysis_agent,
        context=context or [],
        output_file=output_file,
    )


def build_annotation_task(context=None, output_file=None, max_variants=200):
    """Annotation pass. All rules live in skills/annotation.md."""
    return Task(
        description=(
            _skill_block("annotation", "ANNOTATION") +
            "The VCF to annotate is: {file_path}\n\n"
            "1. Read the QC verdict in your context and apply the "
            "prerequisite rule in the annotation skill.\n"
            "2. Call the vep_annotate tool with vcf_path={file_path} and report the variants. Call it once only - it "
            "batches internally.\n"
            "3. Produce the annotation report exactly as the annotation skill "
            "specifies.\n"
        ),
        expected_output=(
            "An annotation report following the section structure defined in "
            "the annotation skill, including the Limitations section."
        ),
        agent=analysis_agent,
        context=context or [],
        output_file=output_file,
    )
