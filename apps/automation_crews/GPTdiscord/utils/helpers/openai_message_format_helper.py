import openai
from colorama import Fore, Style


def format_error_message(error):
    error_prefix = "Error: "
    try:
        if isinstance(error, openai.OpenAIError):
            if hasattr(error, "response") and error.response:
                try:
                    error_json = error.response.json()
                    code = error.response.status_code
                    error_details = error_json.get("error", {})
                    error_message = error_details.get(
                        "message", "An unspecified error occurred."
                    )
                    return (
                        Fore.RED
                        + error_prefix
                        + f"An OpenAI API error occurred: Error code {code} - {error_message}"
                        + Style.RESET_ALL
                    )
                except ValueError:
                    return (
                        Fore.RED
                        + error_prefix
                        + "An OpenAI API error occurred, but the details were not in a recognizable format."
                        + Style.RESET_ALL
                    )
            else:
                return (
                    Fore.RED
                    + error_prefix
                    + "An OpenAI API error occurred, but no additional details are available."
                    + Style.RESET_ALL
                )
        elif hasattr(error, "response") and error.response is not None:
            try:
                error_json = error.response.json()
                code = error.response.status_code
                return (
                    Fore.RED
                    + error_prefix
                    + f"An HTTP error occurred: Error code {code} - {error_json}"
                    + Style.RESET_ALL
                )
            except ValueError:
                return (
                    Fore.RED
                    + error_prefix
                    + "An error occurred, but the response was not in a recognizable format."
                    + Style.RESET_ALL
                )
        else:
            return Fore.RED + error_prefix + str(error) + Style.RESET_ALL
    except Exception as e:
        return (
            Fore.RED
            + error_prefix
            + f"An unexpected error occurred while formatting the error message: {e}"
            + Style.RESET_ALL
        )
