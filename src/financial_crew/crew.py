import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from langchain_openai import ChatOpenAI
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, PDFSearchTool
from src.components.pyautogui.gmail import openai_key, serp_api_key

load_dotenv()
os.environ["OPENAI_API_KEY"] = openai_key
os.environ["SERPAPI_API_KEY"] = serp_api_key


file_path = None
llm = ChatOpenAI(model="gpt-4o-mini")
folder_path = "./src/financial_crew/assets"
files = os.listdir(folder_path)
for file in files:
    file_path = os.path.join(folder_path, file)

pdf_search_tool = PDFSearchTool(
    pdf=file_path,
)


@CrewBase
class FinnaceCrew:
    agents_config = "./config/agents.yaml"
    tasks_config = "./config/tasks.yaml"

    @agent
    def admin_research_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["admin_research_assistant"],
            tools=[SerperDevTool(), ScrapeWebsiteTool(), pdf_search_tool],
            verbose=True,
            memory=False,
            llm=llm,
        )

    @agent
    def chief_finance_officer(self) -> Agent:
        return Agent(
            config=self.agents_config["chief_finance_officer"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            memory=False,
            llm=llm,
        )

    @agent
    def chief_excutive_officer(self) -> Agent:
        return Agent(
            config=self.agents_config["chief_executive_officer"],
            verbose=True,
            memory=False,
            llm=llm,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["admin_research_assistant_task"],
            agent=self.admin_research_manager(),
        )

    @task
    def chief_finance_officer_task(self) -> Task:
        return Task(
            config=self.tasks_config["chief_finance_officer_task"],
            agent=self.chief_finance_officer(),
        )

    @task
    def chief_executive_officer_task(self) -> Task:
        return Task(
            config=self.tasks_config["chief_executive_officer_task"],
            agent=self.chief_excutive_officer(),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
