from textwrap import dedent

from crewai import Agent


class DesignAgents:
    def __init__(self, project_description):
        self.project_description = project_description

    def ui_ux_designer(self) -> Agent:
        return Agent(
            role="Senior UI/UX Designer",
            goal=dedent(
                f"""
                Create a user-centric, accessible, and visually 
                appealing design for the {self.project_description} that 
                aligns with current web design trends and best practices
                """
            ),
            backstory=dedent(
                """
                You're a seasoned senior UI/UX designer with a lot of experience in 
                creating intuitive web interfaces. You've worked on projects ranging from 
                e-commerce platforms to complex web applications, and you're proficient 
                in tools like Figma and Sketch.
                """
            ),
            allow_delegation=True,
            verbose=True,
        )
