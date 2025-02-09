import os
from financial_crew.crew import FinnaceCrew


def run_financial_crew():
    final_response = FinnaceCrew().crew().kickoff()
    folder_path = "./financial_crew/assets"
    files = os.listdir(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file)
        os.remove(file_path)
    print(final_response)
    return final_response


async def train_crew():
    try:
        # final_response = FinnaceCrew().crew().train(n_iterations=int(sys.argv[1]))
        final_response = (
            FinnaceCrew()
            .crew()
            .train(n_iterations=1, filename="./financial_crew/trained_data.pkl")
        )
        return final_response
    except Exception as e:
        raise ValueError(f"An error occurred while training the crew: {e}") from e
