from pydantic import BaseModel
from typing import Optional


class FileWriteSchema(BaseModel):
    file_path: str
    content: str


class FileWrite:
    name = "File_Write_Tool"
    description = "Use this tool to write content to a file"
    args_schema = FileWriteSchema

    def func(self, file_path: str, content: str) -> str:
        """Execute the file write tool."""
        import os

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            return f"Content successfully written to {file_path}"
        except Exception as e:
            return f"Error writing to file: {str(e)}"

    async def _arun(self, file_path: str, content: str) -> str:
        """Execute the file write tool asynchronously."""
        raise NotImplementedError("FileWriteTool does not support async")
