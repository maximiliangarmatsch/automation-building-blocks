from crewai import Crew

from teams.business.agents import BusinessAgents
from teams.business.tasks import BusinessTasks


class BusinessCrew:
    """Business Team Crew"""

    def __init__(self, project_description: str):
        self.agents = BusinessAgents(project_description=project_description)
        self.tasks = BusinessTasks(
            project_description=project_description,
            # TODO Keep in global config file
            output_directory="./generated_src",
        )
        self.project_description = project_description

    def run(self):
        crew = Crew(
            agents=[
                self.agents.project_manager(),
                self.agents.business_analyst(),
            ],
            tasks=[
                self.tasks.prepare_document(agent=self.agents.project_manager()),
                self.tasks.define_product_vision_and_prioritize_features(
                    agent=self.agents.business_analyst()
                ),
            ],
        )

        result = crew.kickoff()
        return result


if __name__ == "__main__":
    print("==========================================")
    project = input("What Project would you like to build: \n")
    business_crew = BusinessCrew(project_description=project)
    result = business_crew.run()
    print(result)
