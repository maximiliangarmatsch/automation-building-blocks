from datetime import datetime
from crewai import Crew
from dotenv import load_dotenv
from invoice_crew.agents.prepare_invoice.prepare_invoice_agent import (
    prepare_invoice,
)
from invoice_crew.agents.prepare_invoice.prepare_invoice_task import (
    invoice_preparation,
)

# Load environment variables
load_dotenv()

date = datetime.today().strftime("%Y-%m-%d")
timezone = datetime.now().astimezone().tzinfo


# Run Agent
def run_invoice_crew():
    crew = Crew(agents=[prepare_invoice()], tasks=[invoice_preparation()])
    result = crew.kickoff()
    print(result)
    return "Crew run initiated", 200
