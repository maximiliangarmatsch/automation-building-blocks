from datetime import datetime
from crewai import Task, Crew
from dotenv import load_dotenv
from agents.prepare_invoice.prepare_invoice_agent import prepare_invoice
from agents.prepare_invoice.prepare_invoice_task import invoice_preparation
# Load environment variables
load_dotenv()

date = datetime.today().strftime("%Y-%m-%d")
timezone = datetime.now().astimezone().tzinfo
# Setup Todo

# Create and Execute Agent.
def run_crew():
    crew = Crew(agents=[prepare_invoice()], tasks=[invoice_preparation()])
    result = crew.kickoff()
    print(result)
    return "Crew run initiated", 200
run_crew()
