import time
import json
import google.generativeai as genai
from helper import make_prompt


def get_attractiveness_score(video_path):
    video_file = genai.upload_file(path=video_path)
    while video_file.state.name == "PROCESSING":
        time.sleep(10)
        video_file = genai.get_file(video_file.name)
    if video_file.state.name == "FAILED":
        return {"error": "Video processing failed."}
    prompt = make_prompt("./prompts/attractiveness.txt")
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(
        [prompt, video_file], request_options={"timeout": 600}
    )
    genai.delete_file(video_file.name)
    json_response = response.text.lstrip("`json").rstrip("`")
    if not json_response:
        return {"error": "No response received from GenAI model."}
    data = json.loads(json_response)
    print(data)
    return data
