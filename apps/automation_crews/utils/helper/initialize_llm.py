import os
from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
api_key = os.getenv("GROQ_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# llm = ChatOpenAI(model="gpt4o-mini", api_key=openai_api_key)
llm = ChatGroq(model="llama-3.1-70b-versatile", api_key=api_key)
