import os
from crewai import Crew
from agents.project_manager.project_manager import project_manager
from agents.project_manager.prepare_document import prepare_document

from agents.business_analyst.business_analyst import business_analyst
from agents.business_analyst.define_product_vision import define_product_vision
from dotenv import load_dotenv
load_dotenv()
os.environ["GROQ_API_KEY"] = "GROQ_API_KEY"

class BusinessCrew:
    """Business Team Crew"""

    def __init__(self, project_description: str):
        self.project_description = project_description

    def run(self):
        crew = Crew(
            agents=[
                project_manager(),
                business_analyst(),
            ],
            tasks=[
                prepare_document(
                    agent=project_manager(),
                    project_description=self.project_description,
                ),
                define_product_vision(agent=business_analyst()),
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
