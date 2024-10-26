from crewai import Task
from personal_assistant_crew.agents.prepare_invoice.prepare_invoice_agent import (
    prepare_invoice,
)


gSheet_script_path = "./components/gSheet_script_executor.py"

invoice_preparation_todo = """
    Update data in the Google Sheet template 
    {https://docs.google.com/spreadsheets/d/1HmDjB28iAil25HUByMQBTnKMGu0Vl5pzBhpqXWaFIrM/edit?gid=1194874101#gid=1194874101} \n
    For cell {I8}, set {number of upcoming month and year} and rember 
    that 011 must be added with month and year as {0924011} \n
    For cell {I10}, set {first of the upcoming month} as {01.08.24} \n
    For cell {I11}, set to {last of the upcoming month} as {30.09.24} \n
    For cell {D16}, set {the month to the current month and year}  as {09.24} \n
    For cell {E16}, set {1234}
"""


def invoice_preparation():
    task = Task(
        description=f"""Insert data in to the specific columns according to {invoice_preparation_todo}. 
        Data should be enter in mentioed columns.
        After data enter in each cell then execute {gSheet_script_path} script using SHELLTOOL_EXEC_COMMAND.""",
        agent=prepare_invoice(),
        expected_output="Google sheet template with updated data and a draft email with all the mentioed instructions.",
    )
    return task
