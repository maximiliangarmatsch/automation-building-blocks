from textwrap import dedent
from crewai import Agent
from dev_crew.tools.file_write import FileWrite
from dev_crew.tools.file_read import FileRead
from utils.helper.initialize_llm import llm


def backend_developer() -> Agent:
    return Agent(
        role="Senior Backend Developer",
        goal="",
        goal=dedent(
            """
                Design and implement a scalable, secure backend architecture with 
                efficient APIs and database management.
            """
        ),
        backstory=dedent(
            """
                With a lot of backend development experience, you're proficient in languages 
                like Python, GraphQL, NestJs and Node.js, and have extensive knowledge of 
                database systems and cloud platforms. You've successfully built and 
                maintained high-traffic web applications and are well-versed in 
                microservices architecture. You also know how to document starting 
                your app in a markdown file.
            """
        ),
        allow_delegation=True,
        verbose=True,
        llm=llm,
        tools=[FileWrite(), FileRead()],
    )
