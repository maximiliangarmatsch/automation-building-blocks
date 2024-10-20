from textwrap import dedent

from crewai import Task, Agent


def develop_backend_task(
    agent: Agent, project_description: str, output_directory: str
) -> Task:
    return Task(
        description=dedent(
            f"""
                Create a simple backend if needed for the {project_description}. 
                Use a technology of your choice and save the files in the {output_directory}/backend folder.
            """
        ),
        agent=agent,
        expected_output=dedent(
            f"""
                Backend code files and API endpoints documentation, saved in the {output_directory}/backend folder.
                And a README.md file stating step-by-step guides to run the application.
            """
        ),
    )
