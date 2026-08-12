# Genomics Variant Analysis Agent

A multi-agent workflow for research-oriented genomic variant analysis.

The system takes a **VCF file + disease/phenotype** and coordinates specialized agents to analyze and prioritize candidate variants.

## Workflow

```text
VCF + Disease/Phenotype
        
    QC Agent
        
 Annotation Agent
        
Disease-Evidence Agent
        
Prioritization Agent
        
   Critic Agent
        
   Human Review
```

The workflow is orchestrated with **LangGraph**. Agents use deterministic bioinformatics tools such as `bcftools`, VEP, and literature-search 
tools rather than performing these operations themselves.

## Agent Roles

- **QC Agent**  evaluates VCF quality and basic variant statistics.
- **Annotation Agent**  gathers gene, consequence, frequency, ClinVar, and other variant annotations.
- **Disease-Evidence Agent**  investigates gene/variant relationships with the provided disease or phenotype.
- **Prioritization Agent**  integrates the collected evidence and ranks candidates for research follow-up.
- **Critic Agent**  checks the ranking for missing evidence, unsupported claims, and overinterpretation.

## My Components

```text
agent.py
   LangGraph multi-agent orchestration

 skills/
     qc.md
     annotation.md
     disease_evidence.md
     prioritization.md
     critic.md
```

The `skills/` files define **how each specialist should approach its task**, while `agent.py` controls how information moves between the 
agents.

> This is a research and educational proof of concept. Candidate prioritization is intended for human review and is not a clinical 
pathogenicity classification.
