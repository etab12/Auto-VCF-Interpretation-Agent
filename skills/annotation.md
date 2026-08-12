# Variant Annotation

## Purpose

Collect structured annotation for candidate variants so downstream agents can evaluate biological and disease relevance.

## Procedure

For each variant:

1. Use the available annotation tools.
2. Record, when available:
   - chromosome and position
   - reference and alternate allele
   - gene symbol
   - transcript
   - variant consequence
   - predicted impact
   - HGVS coding change
   - HGVS protein change
   - population allele frequency
   - ClinVar classification
3. Preserve the exact annotation returned by tools or databases.
4. Flag missing or conflicting annotations.
5. Pass the structured annotation to the disease-evidence and prioritization stages.

## Rules

- Do not infer annotations that were not returned by a tool.
- Do not treat rarity alone as evidence of pathogenicity.
- Do not treat a predicted damaging consequence as proof of disease causality.
- Preserve ClinVar classifications exactly as returned.
- Clearly distinguish missing evidence from negative evidence.
- If transcript-specific annotations differ, report the relevant transcript information rather than collapsing them incorrectly.

## Output

For each candidate variant, return a concise structured summary containing:

- Variant
- Gene
- Consequence
- Transcript / HGVS
- Population frequency
- ClinVar classification
- Predicted impact
- Missing or conflicting information
