import os
import sys
from src.financial_crew.crew import FinnaceCrew

def run_crew():
    final_response = FinnaceCrew().crew().kickoff()
    folder_path = "./src/financial_crew/assets"
    files = os.listdir(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file)
        os.remove(file_path)
    print(final_response)
    return final_response

async def train_crew():
    try:
        final_response = FinnaceCrew().crew().train(n_iterations=int(sys.argv[1]))
        return final_response
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
