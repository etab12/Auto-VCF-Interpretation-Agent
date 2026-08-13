# VCF Quality Control

## Purpose

Evaluate whether the input VCF is suitable for downstream variant analysis and identify quality issues that may affect 
interpretation.

## Procedure

When given a VCF:

1. Confirm that the file exists and can be read.

2. Use the available VCF QC tools, such as `bcftools_stats`, to inspect the file.

3. Review available summary information, including:
   - total number of variants
   - SNP count
   - indel count
   - multiallelic variants, when available
   - FILTER status

4. Review available variant-level quality fields when present, such as:
   - QUAL
   - FILTER
   - DP
   - GQ
   - allele depth (AD)

5. Identify obvious quality warnings, malformed records, or missing information.

6. Apply basic filtering for downstream analysis:
   - retain `FILTER=PASS` variants when FILTER information is available
   - do not apply additional QUAL, DP, GQ, or other thresholds unless explicitly specified
   - preserve the original VCF
   - write retained variants to a separate filtered VCF

7. Record:
   - number of variants before filtering
   - number retained
   - number removed
   - reasons for removal

8. Determine whether the resulting VCF is suitable for downstream annotation.

## Rules

- Do not make pathogenicity or disease-relevance claims during QC.
- Do not invent quality metrics that are not present in the VCF or tool output.
- Do not apply arbitrary filtering thresholds unless the user or workflow specifies them.
- Clearly distinguish observed QC findings from recommendations.
- If important QC information is missing, report the limitation.
- Do not treat missing quality information as evidence that a variant failed QC.
- Preserve the original VCF and write any filtered output to a separate file.

## Output

Return a concise QC summary containing:

- file status: PASS, WARNING, or FAIL
- major variant statistics
- important quality observations
- warnings or limitations
- whether downstream annotation can reasonably proceed
