import requests
def execute_url(url):
    """
    Function to execute the given URL and return the status code.
    :param url: URL to execute
    :return: None
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Execution successful, returned 200.")
        else:
            print(f"Execution failed, returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error executing the URL: {e}")
if __name__ == "__main__":
    url = "https://script.google.com/macros/s/AKfycbxr296Bo54_5ffR_239yZoP070R9iPFTGA0PalpGl6qH48mdhMmYwnly4-L1kzfRAFI5A/exec"
    execute_url(url)
