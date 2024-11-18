import os
import aiohttp
import io
import requests
import base64
from PIL import Image
from GPTdiscord.utils.helpers.openai_message_format_helper import format_error_message
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


async def handle_image_attachments(message, is_mentioned):
    valid_channel_ids = [int(cid) for cid in os.getenv("CHANNEL_IDS", "").split(",")]
    if not (is_mentioned or message.channel.id in valid_channel_ids):
        return

    for attachment in message.attachments:

        if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            async with message.channel.typing():

                try:
                    base64_image = await encode_discord_image(attachment.url)
                    instructions = (
                        message.content if message.content else "What’s in this image?"
                    )
                    analysis_result = await analyze_image(base64_image, instructions)
                    response_text = (
                        analysis_result.get("choices", [{}])[0]
                        .get("message", {})
                        .get("content", "")
                    )

                    if response_text:
                        await message.channel.send(response_text)

                    else:
                        await message.channel.send(
                            "Sorry, I couldn't analyze the image."
                        )

                except Exception as e:
                    error_details = str(e)
                    if hasattr(e, "response") and e.response is not None:
                        error_details += f" Response: {e.response.text}"
                    formatted_error = format_error_message(error_details)
                    await message.channel.send(formatted_error)
