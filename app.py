import time

import gradio as gr

from crewai import Crew, Process

from agents.analysis import analysis_agent
from agents.research import research_agent
from agents.writer import writer_agent
from agents.critic import critic_agent

from tasks.analysis_task import analysis_task
from tasks.research_task import research_task
from tasks.writer_task import writer_task
from tasks.critic_task import critic_task


# ---------------------------------------------------------------------------
# Core analysis pipeline (unchanged logic, only wrapped for streaming status)
# ---------------------------------------------------------------------------
def run_analysis(file_path):
    """
    Runs the full multi-agent crew and yields UI updates so the user sees
    progress instead of a single frozen "Start Analysis" click.
    Yields: (status_markdown, report_markdown, button_update)
    """
    if file_path is None:
        yield (
            "⚠️ **Please upload a VCF file first.**",
            "",
            gr.update(interactive=True, value="🧬 Start Analysis"),
        )
        return

    # Disable the button and show a running state
    yield (
        "🔄 **Validating and analyzing file...**",
        "",
        gr.update(interactive=False, value="Analyzing..."),
    )

    # Validation is handled as part of the Analysis Agent's task, so the
    # uploaded file path is injected directly into analysis_task.
    analysis_task.description = f"""
    Validate and analyze the uploaded VCF file.

    File path:
    {file_path}

    Steps:
    1. Confirm the file is readable and follows the VCF structure. If it is
       not valid, clearly report the issue and stop.
    2. If valid, extract the relevant genes, variants, and key annotations.

    Report the validation result and, if applicable, the extracted
    genes/variants/analysis results.
    """

    crew = Crew(
        agents=[
            analysis_agent,
            research_agent,
            writer_agent,
            critic_agent,
        ],
        tasks=[
            analysis_task,
            research_task,
            writer_task,
            critic_task,
        ],
        process=Process.sequential,
        verbose=True,
    )

    try:
        yield (
            "🧠 **Running multi-agent analysis** — analysis (incl. "
            "validation) → research → report writing → review. This can "
            "take a few minutes depending on the number of variants.",
            "",
            gr.update(interactive=False, value="Analyzing..."),
        )

        result = crew.kickoff()

        yield (
            "✅ **Analysis complete.**",
            str(result),
            gr.update(interactive=True, value="🧬 Start Analysis"),
        )

    except Exception as e:
        yield (
            "❌ **Analysis failed.** See details below.",
            f"### Error\n\n```\n{str(e)}\n```",
            gr.update(interactive=True, value="🧬 Start Analysis"),
        )


# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
:root {
    --gv-radius: 16px;
}

.gv-header {
    text-align: center;
    padding: 28px 16px 8px 16px;
}

.gv-header h1 {
    font-size: 2.1rem;
    margin-bottom: 4px;
}

.gv-header p {
    opacity: 0.75;
    font-size: 1.02rem;
    margin-top: 0;
}

.gv-card {
    border-radius: var(--gv-radius) !important;
    padding: 18px !important;
}

.gv-status {
    padding: 10px 16px;
    border-radius: 12px;
    font-size: 0.98rem;
}

.gv-report {
    min-height: 220px;
}

.gv-disclaimer {
    font-size: 0.85rem;
    opacity: 0.65;
    text-align: center;
    padding-top: 6px;
}

footer {visibility: hidden}
"""

theme = gr.themes.Soft(
    primary_hue="teal",
    secondary_hue="slate",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "sans-serif"],
    radius_size="lg",
)


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
with gr.Blocks(title="Genomics Variant Analysis", theme=theme, css=CUSTOM_CSS) as demo:

    with gr.Column(elem_classes="gv-header"):
        gr.Markdown(
            """
            # 🧬 Genomics Variant Analysis
            Upload a VCF file and let a team of AI agents validate, analyze,
            research, and report on your genomic variants.
            """
        )

    with gr.Row(equal_height=True):
        # ---------------- Left: upload + controls ----------------
        with gr.Column(scale=2):
            with gr.Group(elem_classes="gv-card"):
                gr.Markdown("### 1. Upload your VCF file")
                file_input = gr.File(
                    label="",
                    file_types=[".vcf"],
                    type="filepath",
                )
                analyze_button = gr.Button(
                    "🧬 Start Analysis",
                    variant="primary",
                    size="lg",
                )
                status_box = gr.Markdown(
                    value="",
                    elem_classes="gv-status",
                )

            with gr.Accordion("ℹ️ How this works", open=False):
                gr.Markdown(
                    """
                    Your file passes through four specialized agents, in order:

                    1. **Analysis** — validates the VCF, then extracts genes,
                       variants, and key annotations.
                    2. **Research** — searches PubMed/NCBI for related evidence.
                    3. **Writer** — drafts a clear, structured report.
                    4. **Critic** — reviews the report for accuracy and clarity.
                    """
                )

            gr.Markdown(
                "This tool summarizes published research evidence. It is "
                "**not** a diagnostic tool and does not provide medical advice.",
                elem_classes="gv-disclaimer",
            )

        # ---------------- Right: report output ----------------
        with gr.Column(scale=3):
            with gr.Group(elem_classes="gv-card"):
                gr.Markdown("### 2. Report")
                output = gr.Markdown(
                    value="_Your report will appear here after analysis._",
                    elem_classes="gv-report",
                )

    analyze_button.click(
        fn=run_analysis,
        inputs=file_input,
        outputs=[status_box, output, analyze_button],
    )


if __name__ == "__main__":
    demo.launch()