def read_prompt(file_path) -> str:
    with open(file_path, "r", encoding="utf8") as file:
        prompt = file.read()
    return prompt
