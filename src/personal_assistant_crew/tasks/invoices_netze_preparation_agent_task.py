from crewai import Task
from agents_todo.invoices_netze_preparation_agent_todo import invoices_netze_preparation_agent_todo
from agents.invoices_netze_preparation_agent import invoices_netze_preparation_agent


gSheet_script_path = "./components/gSheet_script_executor.py"
def invoices_netze_preparation_agent_task():
    task = Task(
        description=f"""Insert data in to the specific columns according to {invoices_netze_preparation_agent_todo}. 
        Data should be enter in mentioed columns.
        After data enter in each cell then execute {gSheet_script_path} script using SHELLTOOL_EXEC_COMMAND.""",
        agent = invoices_netze_preparation_agent(),
        expected_output = "Google sheet template with updated data and a draft email with all the mentioed instructions.",
    )
    return task
