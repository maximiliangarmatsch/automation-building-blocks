from datetime import datetime
from crewai import Task, Crew
from dotenv import load_dotenv
from agents.invoices_netze_preparation_agent import invoices_netze_preparation_agent
from tasks.invoices_netze_preparation_agent_task import invoices_netze_preparation_agent_task
# Load environment variables
load_dotenv()

date = datetime.today().strftime("%Y-%m-%d")
timezone = datetime.now().astimezone().tzinfo
# Setup Todo

# Create and Execute Agent.
def run_crew():
    crew = Crew(agents=[invoices_netze_preparation_agent()], tasks=[invoices_netze_preparation_agent_task()])
    result = crew.kickoff()
    print(result)
    return "Crew run initiated", 200
run_crew()
