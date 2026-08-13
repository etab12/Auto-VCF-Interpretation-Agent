# Variant Annotation

## Purpose

Annotate variants that passed QC and filtering to collect genomic and clinical information needed for downstream analysis.

## Procedure

When given a filtered VCF:

1. Confirm that the VCF passed the QC step and identify the genome build.

2. Use the available annotation tool, such as VEP, to annotate the variants.

3. For each variant, collect available information including:
   - chromosome and position
   - reference and alternate alleles
   - gene
   - transcript
   - variant consequence
   - coding HGVS (HGVSc)
   - protein HGVS (HGVSp)
   - existing variant identifiers, such as rsID
   - population allele frequency, when available
   - ClinVar clinical significance, when available

4. Preserve the original variant identity so each annotation can be traced back to the input VCF.

5. Identify variants for which annotation failed or important annotation fields are missing.

6. Produce structured annotation results for downstream disease-evidence analysis.

## Rules

- Never infer or invent annotations that were not returned by the annotation tool.
- Maintain consistency with the genome build of the input VCF.
- Do not classify a variant as pathogenic based only on its predicted consequence.
- Do not treat rarity alone as evidence of pathogenicity.
- Preserve uncertain or conflicting ClinVar classifications as reported.
- Clearly distinguish missing annotation from evidence that a variant is benign.
- Report annotation failures explicitly.

## Output

Return:

- number of variants submitted for annotation
- number successfully annotated
- structured annotation for each variant
- genes identified
- important missing annotations or failures
- any limitations relevant to downstream analysis
