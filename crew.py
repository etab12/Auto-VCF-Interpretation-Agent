from crewai import Crew, Process

from agents.analysis import analysis_agent
from agents.research import research_agent
from agents.writer import writer_agent
from agents.critic import critic_agent

from tasks.analysis_task import analysis_task
from tasks.research_task import research_task
from tasks.writer_task import writer_task
from tasks.critic_task import critic_task


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