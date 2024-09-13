import os
from langchain.tools import BaseTool


class FileReadTool(BaseTool):
    name = "File Read Tool"
    description = "Use this tool to read content from a file"

    def _run(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            return f"Error: The file {file_path} does not exist."

        try:
            with open(file_path, "r") as file:
                content = file.read()
            return content
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def _arun(self, file_path: str):
        raise NotImplementedError("FileReadTool does not support async")
