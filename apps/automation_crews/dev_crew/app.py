# import os
from crewai import Crew, Process
from dev_crew._agents import Agents
from dev_crew.tasks import Tasks

# from utils.helper.initialize_llm import llm


class WebsiteDevCrew:
    def __init__(self, project_description):
        self.agents = Agents(project_description=project_description)
        self.tasks = Tasks(
            project_description=project_description,
            output_directory="./old_generated_src",
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

# Un-Comment to run without Discord Bot
if __name__ == "__main__":
    print("==========================================")
    project = input("What Project would you like to build: \n")
    website_crew = WebsiteDevCrew(project_description=project)
    result = website_crew.run()
    print(result)
