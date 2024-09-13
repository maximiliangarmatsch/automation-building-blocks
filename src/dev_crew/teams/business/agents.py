from textwrap import dedent

from crewai import Agent
from dev_crew.tools.file_write_tool import FileWriteTool
from dev_crew.tools.file_read_tool import FileReadTool


class BusinessAgents:
    def __init__(self, project_description):
        self.project_description = project_description

    def project_manager(self) -> Agent:
        return Agent(
            role="Senior Project Manager",
            goal=dedent(
                """
                Coordinate all aspects of the website development, ensure timely delivery,
                and maintain clear communication among team members.
                """
            ),
            backstory=dedent(
                """
                You are a senior project manager with a lot of experience in managing web development projects, with a track record of successful deliveries for various industries. 
                You're skilled in agile methodologies and have a deep understanding of both technical and business aspects of web development.
                """
            ),
            allow_delegation=True,
            verbose=True,
            tools=[FileWriteTool(), FileReadTool()],
        )

    def business_analyst(self) -> Agent:
        return Agent(
            role="Senior Business Analyst",
            goal=dedent(
                """
                Define product vision, prioritize features, and ensure the team delivers maximum value.
                """
            ),
            backstory=dedent(
                """
                You are a senior business analyst with a lot of experience, with a track record of successful deliveries for various industries. 
                You're skilled in agile methodologies and have a deep understanding of both technical and business aspects.
                """
            ),
            allow_delegation=False,
            verbose=True,
        )
