import os
from langchain.tools import BaseTool


class FileWriteTool(BaseTool):
    name = "File Write Tool"
    description = "Use this tool to write content to a file"

    def _run(self, file_path: str, content: str) -> str:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, "w") as file:
                file.write(content)
            return f"Content successfully written to {file_path}"
        except Exception as e:
            return f"Error writing to file: {str(e)}"

    def _arun(self, file_path: str, content: str):
        raise NotImplementedError("FileWriteTool does not support async")
