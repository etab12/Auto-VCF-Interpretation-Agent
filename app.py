import gradio as gr

from crewai import Crew, Process

from main import (
    supervisor_agent,
    validation_agent,
    analysis_agent,
    literature_agent,
    writer_agent,
    critic_agent,
    validation_task,
    analysis_task,
    literature_task,
    writing_task,
    critic_task,
)


def run_analysis(file):

    if file is None:
        return "Please upload a VCF file."

    file_path = file

    validation_task.description = f"""
    Validate the following VCF file:

    File path:
    {file_path}

    Check whether:
    1. The file is readable.
    2. It follows the VCF structure.
    3. Required VCF information is present.
    4. Variant records appear usable.
    5. There are obvious structural problems.

    Report the validation result and detected issues.
    """

    crew = Crew(
        agents=[
            supervisor_agent,
            validation_agent,
            analysis_agent,
            literature_agent,
            writer_agent,
            critic_agent,
        ],
        tasks=[
            validation_task,
            analysis_task,
            literature_task,
            writing_task,
            critic_task,
        ],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    return str(result)


with gr.Blocks(title="Genomics Variant Analysis") as demo:

    gr.Markdown(
        """
        # Genomics Variant Analysis Agent

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