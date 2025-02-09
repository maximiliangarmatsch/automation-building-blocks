from textwrap import dedent
from crewai import Task


class Tasks:
    def __init__(self, project_description, output_directory):
        self.project_description = project_description
        self.output_directory = output_directory

    def design_ui_task(self, agent) -> Task:
        return Task(
            description=dedent(
                f"""\
                    Design the user interface for the {self.project_description}. Include layouts for the necessary pages.
                    Generate a sample image of the main interface.
                    Make sure to check with a human if the draft is good before finalizing your answer.
                """
            ),
            agent=agent,
            expected_output="Detailed UI design specifications including color schemes, layout descriptions, and user flow diagrams, and a generated sample image of the main interface.",
            human_input=True,
        )

    def write_content_task(self, agent) -> Task:
        return Task(
            description=f"Write engaging content for the {self.project_description}.",
            agent=agent,
            expected_output="Written content for all pages of the website, including SEO-optimized text and product descriptions.",
        )

    def develop_frontend_task(self, agent) -> Task:
        return Task(
            description=f"Implement the designed UI using React, Tailwind css and any tools necessary to sastify {self.project_description}. Create responsive layouts and interactive elements. Save all files in the {self.output_directory} folder.",
            agent=agent,
            expected_output=f"Neccessary files for all pages, saved in the {self.output_directory} folder. And a README.md file stating step-by-step guides to run the application.",
        )

    def develop_backend_task(self, agent) -> Task:
        return Task(
            description=f"Create a simple backend if needed for the {self.project_description}. Use a technology of your choice and save the files in the {self.output_directory}/backend folder.",
            agent=agent,
            expected_output=f"Backend code files and API endpoints documentation, saved in the {self.output_directory}/backend folder. And a README.md file stating step-by-step guides to run the application.",
        )

    def integrate_and_test_task(self, agent) -> Task:
        return Task(
            description="Integrate the frontend and backend components. Perform thorough testing of all website functionalities, including responsiveness and cross-browser compatibility.",
            agent=agent,
            expected_output="Detailed test report including any identified issues and confirmation of successful integration.",
        )

    def finalize_project_task(self, agent) -> Task:
        return Task(
            description=f"Review all components of the website, write a README.md file on how to start the project,  ensure all files are properly organized in the {self.output_directory} folder, and create a final project report.",
            agent=agent,
            expected_output="Final project report confirming completion of all tasks and proper organization of files in the {self.output_directory} folder",
        )
