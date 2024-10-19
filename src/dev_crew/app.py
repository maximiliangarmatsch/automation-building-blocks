import os
from crewai import Crew, Process
from _agents import Agents
from tasks import Tasks
from dotenv import load_dotenv

load_dotenv()

# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

class WebsiteDevCrew:
    """Website Development Crew"""

    def __init__(self, project_description):
        self.agents = Agents(project_description=project_description)
        self.tasks = Tasks(
            project_description=project_description,
            output_directory="./generated_src",
        )
        self.project_description = project_description

    def run(self):
        crew = Crew(
            agents=[
                self.agents.project_manager(),
                self.agents.ui_ux_designer(),
                self.agents.frontend_developer(),
                self.agents.backend_developer(),
                self.agents.content_writer(),
                self.agents.qa_engineer(),
            ],
            tasks=[
                self.tasks.design_ui_task(agent=self.agents.ui_ux_designer()),
                self.tasks.write_content_task(agent=self.agents.content_writer()),
                self.tasks.develop_frontend_task(
                    agent=self.agents.frontend_developer()
                ),
                self.tasks.develop_backend_task(agent=self.agents.backend_developer()),
                self.tasks.integrate_and_test_task(agent=self.agents.qa_engineer()),
                self.tasks.finalize_project_task(agent=self.agents.project_manager()),
            ],
            process=Process.sequential,
            verbose=True,
        )
        result = crew.kickoff()
        return result


if __name__ == "__main__":
    print("==========================================")
    project = input("What Project would you like to build: \n")
    website_crew = WebsiteDevCrew(project_description=project)
    result = website_crew.run()
    print(result)
