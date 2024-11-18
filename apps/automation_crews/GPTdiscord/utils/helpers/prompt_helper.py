def read_prompt(file_path) -> str:
    file_path = file_path
    with open(file_path, "r", encoding="utf8") as file:
        prompt = file.read()
    return prompt
