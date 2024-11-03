from textwrap import dedent
from crewai import Agent
from apps.automation_crews.utils.helper.initialize_llm import llm


def business_analyst() -> Agent:
    return Agent(
        role="Senior Business Analyst",
        goal=dedent(
            """\
                Define product vision, prioritize features, and ensure the team delivers maximum value.
                """
        ),
        backstory=dedent(
            """\
                You are a senior business analyst with a lot of experience, with a track record of successful deliveries for various industries. 
                You're skilled in agile methodologies and have a deep understanding of both technical and business aspects.
                """
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm,
    )
