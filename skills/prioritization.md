# Variant Prioritization

## Purpose

Prioritize candidate variants for research review by integrating the available QC, annotation, and disease-evidence results.

## Procedure

For each candidate variant:

1. Review whether the variant passed the relevant QC checks.

2. Review the variant annotation, including when available:
   - gene
   - consequence
   - predicted impact
   - population allele frequency
   - ClinVar classification
   - transcript and HGVS information

3. Review the disease-evidence findings, including:
   - direct human genetic evidence
   - evidence for the specific variant
   - gene-disease association
   - functional evidence
   - biological or pathway relevance

4. Integrate the available evidence and assign one of the following research-priority levels:
   - HIGH PRIORITY
   - MEDIUM PRIORITY
   - LOW PRIORITY

5. Explain which evidence contributed most strongly to the ranking.

6. Identify important evidence that is still missing.

## Rules

- Do not classify variants as pathogenic, likely pathogenic, benign, or likely benign.
- Do not convert a ClinVar VUS into a pathogenic classification.
- Do not treat rarity alone as sufficient evidence for high priority.
- Do not treat computational predictions alone as sufficient evidence for high priority.
- Do not invent evidence that was not produced by upstream tools or agents.
- Clearly distinguish strong evidence from biological plausibility.
- Reduce confidence when important evidence is missing or conflicting.
- Preserve uncertainty.

## Output

Rank candidates from highest to lowest research priority.

For each candidate report:

- Variant
- Gene
- Priority: HIGH / MEDIUM / LOW
- Key supporting evidence
- Evidence against or conflicting evidence
- Missing evidence
- Brief rationale

Finish with a concise explanation of why the highest-ranked candidates deserve further investigation.
