from crewai import Crew

from agents.frontend_developer.frontend_developer import frontend_developer
from agents.frontend_developer.develop_frontend import develop_frontend


class FrontendCrew:
    def __init__(self):
        self.output_directory = "./generated_src"

    def run(self):
        crew = Crew(
            agents=[
                frontend_developer(),
            ],
            tasks=[
                develop_frontend(
                    agent=frontend_developer(),
                    output_directory=self.output_directory,
                ),
            ],
        )

        result = crew.kickoff()
        return result


if __name__ == "__main__":
    print("==========================================")
    frontend_crew = FrontendCrew()
    result = frontend_crew.run()
    print(result)
 