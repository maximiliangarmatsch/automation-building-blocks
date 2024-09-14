from textwrap import dedent

from crewai import Task, Agent


def develop_database(
    agent: Agent, project_description: str, output_directory: str, database_type: str
) -> Task:
    return Task(
        description=dedent(
            f"""
                Design and implement the database for the {project_description}. 
                Use {database_type} for the implementation and ensure that the schema is well 
                optimized for scalability and performance. Save the database files, including 
                any schema definitions, migrations, and scripts in the {output_directory}/database folder.
            """
        ),
        agent=agent,
        expected_output=dedent(
            f"""
                - Database schema definitions, SQL scripts, or NoSQL configurations saved in the {output_directory}/database folder.
                - Migration scripts to set up the database from scratch or migrate from previous versions.
                - A README.md file detailing the setup instructions, including steps to initialize 
                  the database, run migrations, and populate initial data if needed.
                - Documentation on database optimization and security considerations.
            """
        ),
    )
