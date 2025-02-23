import re
from datetime import datetime


def parse_image_size(prompt):
    if "--wide" in prompt:
        size = "1792x1024"
        prompt = prompt.replace("--wide", "").strip()
    elif "--square" in prompt:
        size = "1024x1024"
        prompt = prompt.replace("--square", "").strip()
    elif "--tall" in prompt:
        size = "1024x1792"
        prompt = prompt.replace("--tall", "").strip()
    else:
        size = "1024x1024"
    return prompt, size


def generate_unique_filename(prompt, extension=".png"):
    base_filename = re.sub(r"\W+", "", prompt[:80]).lower()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_filename = f"{base_filename}_{timestamp}{extension}"
    return unique_filename
