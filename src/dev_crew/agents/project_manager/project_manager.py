from textwrap import dedent

from crewai import Agent
from tools.file_write import FileWrite
from tools.file_read import FileRead


def project_manager() -> Agent:
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
        tools=[FileWrite(), FileRead()],
    )
