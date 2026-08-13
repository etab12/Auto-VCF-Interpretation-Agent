import gradio as gr

from crewai import Crew, Process

from agents.validation import validation_agent
from agents.analysis import analysis_agent
from agents.research import research_agent
from agents.writer import writer_agent
from agents.critic import critic_agent

from tasks.validation_task import validation_task
from tasks.analysis_task import analysis_task
from tasks.research_task import research_task
from tasks.writer_task import writer_task
from tasks.critic_task import critic_task


def run_analysis(file_path):

    if file_path is None:
        return "Please upload a VCF file."

    # Update the validation task with the uploaded file
    validation_task.description = f"""
    Validate the uploaded VCF file.

    File path:
    {file_path}

    Check:
    1. Whether the file is readable.
    2. Whether it follows the VCF structure.
    3. Whether required VCF information is present.
    4. Whether variant records are usable.
    5. Whether there are obvious structural problems.

    Report the validation result and detected issues.
    """

    crew = Crew(
        agents=[
            validation_agent,
            analysis_agent,
            research_agent,
            writer_agent,
            critic_agent,
        ],
        tasks=[
            validation_task,
            analysis_task,
            research_task,
            writer_task,
            critic_task,
        ],
        process=Process.sequential,
        verbose=True,
    )

    try:
        result = crew.kickoff()

        return str(result)

    except Exception as e:
        return f"Analysis failed:\n\n{str(e)}"


with gr.Blocks(title="Genomics Variant Analysis") as demo:

    gr.Markdown(
        """
        # Genomics Variant Analysis System

        Upload a VCF file to start the multi-agent analysis.
        """
    )

    file_input = gr.File(
        label="Upload VCF File",
        file_types=[".vcf"],
        type="filepath",
    )

    analyze_button = gr.Button("Start Analysis")

    output = gr.Markdown(
        label="Final Report"
    )

    analyze_button.click(
        fn=run_analysis,
        inputs=file_input,
        outputs=output,
    )


if __name__ == "__main__":
    demo.launch()