import os
from langchain.tools import BaseTool


class FileWrite(BaseTool):
    name: str = "File_Write_Tool"
    description: str = "Use this tool to write content to a file"

    def run(self, file_path: str, content: str) -> str:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            return f"Content successfully written to {file_path}"
        except Exception as e:
            return f"Error writing to file: {str(e)}"

    def arun(self, file_path: str, content: str):
        raise NotImplementedError("FileWriteTool does not support async")
