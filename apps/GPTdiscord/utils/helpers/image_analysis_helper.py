import os
import aiohttp
import io
import requests
import base64
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


async def encode_discord_image(image_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                image_data = await response.read()
                image = Image.open(io.BytesIO(image_data)).convert("RGB")
                if max(image.size) > 1000:
                    image.thumbnail((1000, 1000))
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                return base64.b64encode(buffered.getvalue()).decode("utf-8")


async def analyze_image(base64_image, instructions):
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": instructions},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 400,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}",
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )
    response_json = response.json()
    return response_json
