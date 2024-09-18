from composio_crewai import App, ComposioToolSet, Action
from crewai import Agent
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")
composio_toolset = ComposioToolSet()
tools = composio_toolset.get_tools(apps=[App.GOOGLESHEETS], actions=[Action.SHELLTOOL_EXEC_COMMAND])

def prepare_invoice():
    agent = Agent(
            role = "Google Sheet Agent",
            goal = """You take action on Google Sheet using Google Sheet APIs""",
            backstory = """You are an AI agent responsible for taking actions on Google Sheet on users' behalf. 
            You need to take action on Sheet using Google Sheet APIs. Use correct tools to run APIs from the given tool-set.""",
            verbose = True,
            tools = tools,
            llm = llm,
            cache = False,
        )
    return agent
