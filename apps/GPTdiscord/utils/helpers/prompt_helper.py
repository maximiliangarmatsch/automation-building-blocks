def read_prompt(file_path) -> str:
    file_path = file_path
    with open(file_path, "r", encoding="utf8") as file:
        prompt = file.read()
    return prompt


def read_and_construct_prompt(message, file_path):
    prompt_template = read_prompt(file_path)
    final_prompt = prompt_template.format(MESSAGE=message)
    return final_prompt
