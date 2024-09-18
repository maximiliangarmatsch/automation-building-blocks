import os
from textwrap import dedent
from crewai import Agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model = "llama-3.1-70b-versatile", api_key = api_key)
def business_analyst() -> Agent:
    return Agent(
        role="Senior Business Analyst",
        goal=dedent(
            """
                Define product vision, prioritize features, and ensure the team delivers maximum value.
                """
        ),
        backstory=dedent(
            """
                You are a senior business analyst with a lot of experience, with a track record of successful deliveries for various industries. 
                You're skilled in agile methodologies and have a deep understanding of both technical and business aspects.
                """
        ),
        allow_delegation=False,
        verbose=True,
        llm = llm,
    )
