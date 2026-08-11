# Genomics Variants Analysis Agent

An autonomous  agent for a variant data analysis. It reads Many task-specific
**skills** and calls different \**tools** to perform
quality control, annotate variants, and search the
literature for gene–disease evidence.

Built on:

* **LangGraph** for orchestration
* **FastAPI** 
* **MCP** 
* **Streamlit** for the application



```

## Architecture

 
                    ┌──────────────┐
   Streamlit UI ───►│              │
   (app.py)         │  FastAPI     │
                    │  (api.py)    │
   MCP clients ────►│              │
   (mcp\_server.py)  └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  LangGraph   │   agent.py
                    │  agent loop  │   ├─ loads skills/\*.md into system prompt
                    └──────┬───────┘   └─ binds tools/ as callable functions
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
          tools/qc   tools/annotation  tools/literature
              │            │            │
           FastQC/     Ensembl VEP    PubMed /
           MultiQC      ClinVar       PMC
```

The LangGraph graph is a standard ReAct cycle: `agent → tools → agent → …`
until the model stops requesting tool calls. 

\---

## Project structure

```
genomics-agent/
├── README.md
├── requirements.txt
├── .env.example            
├── .gitignore
│
├── config.py               
├── agent.py                
├── api.py                  
├── mcp\_server.py          
├── app.py                  
│
├── skills/                 # Initial skills files 
│   ├── qc.md
│   ├── annotation.md
│   └── literature\_search.md
│
├── tools/                 
│   ├── \_\_init\_\_.py         # TOOLS registry
│   ├── qc.py
│   ├── annotation.py
│   └── literature.py
│
├── data/                   
│   ├── raw/                # input VCF
│   ├── processed/          # QC reports, annotated VCFs
│   └── reference/          # genome builds, panels, gene lists
│
├── notebooks/             # Quick start 
└── tests/
    └── test\_tools.py
```

\---

## Setup

```bash
git clone https://github.com/etab12/Auto-VCF-Interpretation-Agent.git
cd genomics-agent

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate

pip install -r requirements.txt

cp .env.example .env             # copy your API key here 
```

### Required keys

|Variable|Needed for|
|-|-|
|`ANTHROPIC\_API\_KEY`|the agent's LLM|
|`NCBI\_API\_KEY`|higher PubMed rate limits (optional but recommended)|
|`NCBI\_EMAIL`|required by NCBI E-utilities etiquette|

\---

## Running

**Streamlit UI** — easiest way to try it:

```bash
streamlit run app.py
```

**FastAPI service** — for programmatic use:

```bash
uvicorn api:app --reload --port 8000
# docs at http://localhost:8000/docs
```

```bash
curl -X POST http://localhost:8000/chat \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Run QC on data/raw/sample\_R1.fastq.gz and flag any problems"}'
```

**MCP server** — to use the tools from Claude Desktop or an MCP-aware IDE:

```bash
python mcp\_server.py
```

Then add to your MCP client config:

```json
{
  "mcpServers": {
    "genomics": {
      "command": "python",
      "args": \["/absolute/path/to/genomics-agent/mcp\_server.py"]
    }
  }
}
```



\---

## Development

```bash
pytest tests/ -v
ruff check .
```

Adding a tool:

1. Write the function in `tools/`, decorated with `@tool` and a clear docstring —
the docstring *is* the interface the LLM sees.
2. Register it in `tools/\_\_init\_\_.py`.
3. Reference it by name in the relevant `skills/\*.md`.

\---

## License

MIT

