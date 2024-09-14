# Import base packages
import os
from datetime import datetime

from composio_crewai import App, ComposioToolSet, Action
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Initialize the language model
llm = ChatOpenAI(model="gpt-4o-mini")

# Define tools for the agents
composio_toolset = ComposioToolSet()
tools = composio_toolset.get_tools(apps=[App.GOOGLESHEETS], actions=[Action.SHELLTOOL_EXEC_COMMAND])

date = datetime.today().strftime("%Y-%m-%d")
timezone = datetime.now().astimezone().tzinfo

# Setup Todo
invoices_netze_preparation_agent_todo = """
    Update data in the Google Sheet template {https://docs.google.com/spreadsheets/d/1HmDjB28iAil25HUByMQBTnKMGu0Vl5pzBhpqXWaFIrM/edit?gid=1194874101#gid=1194874101}.
    For cell {I8}, set {number of upcoming month and year} and rember that 011 must be added with month and year as {0924011}.
    For cell {I10}, set {first of the upcoming month} as {01.08.24}.
    For cell {I11}, set to {last of the upcoming month} as {30.09.24}.
    For cell {D16}, set {the month to the current month and year}  as {09.24}.
    For cell {E16}, set {1234}
"""
googleS_script_path = "./google_script_executor.py"
# Create and Execute Agent.
def run_crew():
    invoices_netze_preparation_agent = Agent(
        role="Google Sheet Agent",
        goal="""You take action on Google Sheet using Google Sheet APIs""",
        backstory="""You are an AI agent responsible for taking actions on Google Sheet on users' behalf. 
        You need to take action on Sheet using Google Sheet APIs. Use correct tools to run APIs from the given tool-set.""",
        verbose=True,
        tools=tools,
        llm=llm,
        cache=False,
    )
    task = Task(
        description=f"""Insert data in to the specific columns according to {invoices_netze_preparation_agent_todo}. And only enter the data in mentioed columns.
        After data enter in each cell then execute {googleS_script_path} script using SHELLTOOL_EXEC_COMMAND.""",
        agent=invoices_netze_preparation_agent,
        expected_output = "if free slot is found",
    )
    crew = Crew(agents=[invoices_netze_preparation_agent], tasks=[task])
    result = crew.kickoff()
    print(result)
    return "Crew run initiated", 200
run_crew()
