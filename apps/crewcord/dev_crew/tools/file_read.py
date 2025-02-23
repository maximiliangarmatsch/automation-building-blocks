from typing import Type, Optional
from langchain.tools import BaseTool
from pydantic import BaseModel


class FileReadSchema(BaseModel):
    file_path: str


class FileRead:
    name = "File_Read_Tool"
    description = "Use this tool to read content from a file"
    args_schema = FileReadSchema

    def __init__(self):
        pass

    def func(self, file_path: str) -> str:
        """Execute the file read tool."""
        import os

        if not os.path.exists(file_path):
            return f"Error: The file {file_path} does not exist."
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            return content
        except Exception as e:
            return f"Error reading file: {str(e)}"

    async def _arun(self, file_path: str) -> str:
        """Execute the file read tool asynchronously."""
        raise NotImplementedError("FileReadTool does not support async")
