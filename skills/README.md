# Genomics Variant Analysis Agent

A multi-agent AI system for genomic variant analysis and research prioritization.

The system accepts a VCF file and coordinates specialized agents for quality control, variant annotation, disease-evidence retrieval, 
prioritization, and critical review.

## Architecture

```text
VCF + Disease/Phenotype
        
        

     QC Agent     
  bcftools / VCF  
       QC         

         

 Annotation Agent 
   VEP / ClinVar  

         

 Disease-Evidence 
      Agent       
 PubMed / NCBI    

         

 Prioritization   
      Agent       

         

   Critic Agent   
 Evidence review  

         
 Ranked Candidates
         
         
   Human Review
```

The workflow is orchestrated using LangGraph. Specialized agents use deterministic bioinformatics tools and external data sources to gather 
evidence before candidate variants are prioritized.

## Project Structure

```text
genomics-agent/

 agent.py                    # LangGraph multi-agent workflow
 config.py                   # Model and application configuration
 requirements.txt            # Python dependencies
 .env                        # API keys and environment variables

 skills/                     # Instructions for specialized agents
    qc.md                   # VCF quality-control procedure
    annotation.md           # Variant annotation procedure
    disease_evidence.md     # Gene-disease evidence procedure
    prioritization.md       # Candidate prioritization procedure
    critic.md               # Evidence review procedure

 tools/                      # Deterministic tools available to agents
    __init__.py             # Tool registry
    vcf_tools.py            # VCF parsing and bcftools operations
    annotation.py           # Variant annotation tools
    literature.py           # Literature/evidence search tools

 data/
    example.vcf             # Example input VCF for demonstration

 api.py                      # FastAPI interface
 app.py                      # Streamlit user interface
```

## Agent Responsibilities

### QC Agent
Evaluates the input VCF and uses deterministic tools such as `bcftools` to identify basic quality-control issues.

### Annotation Agent
Collects variant-level information such as gene, consequence, transcript, HGVS notation, and other available annotations.

### Disease-Evidence Agent
Searches biomedical literature and other evidence sources for relationships between candidate genes and the disease or phenotype being 
investigated.

### Prioritization Agent
Combines QC, annotation, and disease-evidence results to rank candidate variants for research review.

### Critic Agent
Reviews the proposed prioritization for missing evidence, unsupported claims, contradictions, and overinterpretation before producing the 
final result.

## Workflow

```text
Input VCF
   
QC
   
Annotation
   
Disease Evidence
   
Prioritization
   
Critic
   
Ranked Candidates
   
Human Review
```

## Design Principle

The AI agents coordinate the analysis and interpret tool outputs, while deterministic bioinformatics tools perform operations such as VCF 
processing and annotation.

```text
LLM / Agent
    
     decides what analysis is needed
    
Bioinformatics Tool
    
     performs deterministic operation
    
Tool Result
    
     returned to agent
    
Agent reasoning / next step
```

The system is intended for **research-oriented variant prioritization and human review**, not autonomous clinical diagnosis or pathogenicity 
classification.
