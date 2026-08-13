# Variant Annotation

## Purpose

Convert variants that pass the QC and filtering stage into structured, interpretable genomic annotations for downstream evidence analysis.

The annotation step should identify what each variant is, where it occurs, which gene or transcript it affects, and what existing genomic or clinical information is available for it.

## Workflow

When given a filtered VCF:

### 1. Verify the input

Before annotation:

- confirm that the VCF passed the QC stage
- confirm that the file is readable
- identify the reference genome build
- ensure the annotation resource uses the same genome build

Do not proceed silently when the genome build is unknown or incompatible with the annotation resource.

### 2. Annotate the variants

Use the available annotation tool, such as VEP, to annotate the variants.

Do not manually infer annotations that can be obtained from the annotation tool.

### 3. Collect variant-level information

For each variant, retrieve available information including:

- chromosome
- genomic position
- reference allele
- alternate allele
- gene symbol
- transcript
- variant consequence
- coding HGVS (HGVSc)
- protein HGVS (HGVSp)
- existing variant identifiers, such as rsID
- population allele frequency, when available
- ClinVar clinical significance, when available

If multiple transcripts or consequences are returned, preserve the relevant information rather than silently selecting one without explanation.

### 4. Preserve variant identity

Every annotation must remain traceable to the original VCF record.

Preserve the original:

- VCF ID
- chromosome
- position
- reference allele
- alternate allele

Do not modify the original input VCF during annotation. Store annotated results separately.

### 5. Assess annotation completeness

After annotation:

- record the number of variants submitted
- record the number successfully annotated
- identify variants with incomplete or missing annotations
- report variants that could not be annotated
- record errors or limitations returned by the annotation tool

Missing information must remain explicitly marked as unavailable rather than inferred.

## Interpretation Boundaries

Annotation describes a variant; it does not by itself determine whether that variant causes disease.

Therefore:

- do not classify a variant as pathogenic solely because it has a high-impact consequence
- do not interpret rarity alone as evidence of pathogenicity
- do not treat missing annotation as evidence that a variant is benign
- do not convert a VUS into pathogenic or benign based on prediction alone
- preserve uncertain or conflicting ClinVar classifications as reported
- distinguish annotation evidence from downstream disease-evidence interpretation

## Rules

- Use annotation tools rather than guessing genomic consequences.
- Never invent genes, transcripts, HGVS expressions, frequencies, identifiers, or clinical classifications.
- Maintain genome-build consistency throughout the workflow.
- Preserve the original variant identity and provenance.
- Clearly report missing or unavailable information.
- Clearly report annotation failures.
- Keep factual annotation separate from disease interpretation.

## Output

Return structured annotation results that can be passed to the downstream Researcher Agent.

For each variant, include available:

- variant identifier and genomic coordinates
- REF and ALT alleles
- gene and transcript
- consequence
- HGVSc and HGVSp
- existing variant identifiers
- population frequency
- ClinVar significance
- annotation warnings or missing fields

Also provide an annotation summary containing:

- total variants submitted
- total variants successfully annotated
- genes identified
- variants with incomplete annotation
- annotation failures
- important limitation