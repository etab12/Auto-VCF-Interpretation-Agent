# GeneDisease Literature Search and Evidence Evaluation

## Purpose

Investigate the published evidence connecting candidate genes or variants to the disease or phenotype of interest.

This skill combines literature retrieval with evidence evaluation. The goal is not simply to find papers, but to determine what 
the available literature actually supports and how directly that evidence relates to the candidate being investigated.

## Workflow

For each candidate gene or variant:

### 1. Define the search target

Identify:

- the candidate gene
- the specific variant, when available
- the disease or phenotype being investigated
- relevant alternative phenotype terms, when appropriate

Keep the search focused on the biological question provided by the workflow.

### 2. Search the literature

Use the available literature-search tools to search combinations such as:

- gene + disease
- gene + phenotype
- gene + disease mechanism
- specific variant + disease
- specific variant + phenotype

When variant-specific evidence is unavailable, broaden the search to the gene level rather than assuming that gene-level 
evidence applies directly to the variant.

### 3. Identify relevant publications

Prioritize publications that directly address the candidate and phenotype.

For relevant results, record available information such as:

- PMID or other publication identifier
- title
- publication year
- study type
- gene or variant investigated
- disease or phenotype studied

Prefer primary research articles when available and distinguish them from reviews or other secondary sources.

### 4. Classify the evidence

Determine what type of evidence each relevant publication provides.

Possible evidence categories include:

- human genetic evidence
- segregation or family evidence
- case reports or case series
- functional experimental evidence
- cellular evidence
- animal-model evidence
- pathway or mechanistic evidence
- expression or tissue-specific evidence
- indirect biological relevance

A publication may contribute more than one type of evidence.

### 5. Determine the level of support

For each piece of evidence, determine whether it supports:

- the specific variant
- the gene in relation to the disease
- the gene in relation to a related phenotype
- a biological pathway or mechanism only

Do not treat these levels of evidence as equivalent.

Variant-specific evidence is generally more directly relevant to interpretation than broad biological plausibility, but the 
strength of evidence must still be evaluated in context.

### 6. Evaluate relevance and strength

Assess how directly the retrieved evidence relates to the phenotype being investigated.

Consider:

- whether the evidence comes from affected humans
- whether the specific variant was studied
- whether segregation was demonstrated
- whether functional experiments support a biological effect
- whether the experimental model is relevant to the disease
- whether findings have been reproduced
- whether the evidence is direct or indirect

Avoid assigning unsupported certainty when the available evidence is limited.

### 7. Look for conflicting or negative evidence

Do not search only for supporting findings.

When available, identify:

- studies that do not support the proposed association
- conflicting functional results
- conflicting disease associations
- evidence supporting a different mechanism
- limitations that weaken interpretation

Preserve disagreement in the literature rather than forcing a single conclusion.

### 8. Summarize the evidence

Produce a balanced summary describing what is known about the candidate and how strongly the available literature connects it 
to the disease or phenotype.

Clearly separate:

- established findings
- suggestive evidence
- indirect biological plausibility
- uncertainty
- absence of evidence

## Evidence Boundaries

Literature evidence must be interpreted conservatively.

Therefore:

- evidence supporting a gene does not automatically establish pathogenicity of a specific variant
- functional impact does not automatically establish disease causality
- biological plausibility does not equal a demonstrated genedisease association
- absence of retrieved literature does not prove that no evidence exists
- a single publication should not automatically be treated as definitive evidence
- review articles may provide useful context but should not be treated as primary experimental evidence

## Rules

- Use the available literature-search tools rather than inventing references.
- Never fabricate publications, PMIDs, authors, titles, study results, or genedisease associations.
- Base evidence summaries only on information supported by retrieved sources.
- Clearly distinguish variant-specific evidence from gene-level evidence.
- Clearly distinguish direct disease evidence from indirect biological relevance.
- Do not claim causality unless the retrieved evidence supports that conclusion.
- Explicitly report weak, conflicting, indirect, or absent evidence.
- Preserve uncertainty when the literature does not support a clear conclusion.
- Do not make a clinical pathogenicity classification.
- Do not use literature evidence as a substitute for formal clinical variant interpretation.

## Output

For each candidate, provide:

- gene
- variant, when available
- disease or phenotype searched
- search terms or strategy used
- relevant publications and identifiers
- publication or study type, when available
- evidence category
- main findings relevant to the candidate
- whether the evidence is variant-specific, gene-level, phenotype-related, or indirect
- strength and relevance of the evidence
- conflicting or negative evidence
- important study limitations
- overall evidence summary

The output should provide the downstream Writer Agent with a traceable and balanced evidence summary rather than a clinical 
diagnosis or pathogenicity classification.
