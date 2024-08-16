
# AI Crew for Financial Decision
## Introduction
This project demonstrates the use of the CrewAI framework to automate the creation of a financial decision. CrewAI orchestrates autonomous AI agents, enabling them to collaborate and execute complex tasks efficiently.

## Running the Script

- **Configure Environment**: Copy `.env.example` and set up the environment variables for [OpenAI](https://platform.openai.com/api-keys) and other tools as needed, like [Serper](serper.dev).

- **Install Dependencies**: Run `poetry lock && poetry install`.
- **Customize**: Modify `src/finance_crew/main.py` to add custom inputs for your agents and tasks.
- **Customize Further**: Check `src/finance_posts/config/agents.yaml` to update your agents and `src/marketing_posts/config/tasks.yaml` to update your tasks.
- **Execute the Script**: Run `poetry run finance_crew` and input your project details.

## Details & Explanation
- **Running the Script**: Execute `poetry run finance_crew`. The script will leverage the CrewAI framework to generate a detailed marketing strategy.
- **Key Components**:
  - `src/finance_crew/main.py`: Main script file.
  - `src/finance_crew/crew.py`: Main crew file where agents and tasks come together, and the main logic is executed.
  - `src/finance_crew/config/agents.yaml`: Configuration file for defining agents.
  - `src/finance_crew/config/tasks.yaml`: Configuration file for defining tasks.
  - `src/finance_crew/tools`: Contains tool classes used by the agents.
