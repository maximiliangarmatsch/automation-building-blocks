import os
import discord
import requests
from openai import OpenAI
from io import BytesIO
from dotenv import load_dotenv
from GPTdiscord.utils.helpers.generate_image_helper import (
    parse_image_size,
    generate_unique_filename,
)
from GPTdiscord.utils.helpers.openai_message_format_helper import format_error_message
import openai

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_model = os.getenv("MODEL_CHAT")

client = OpenAI(api_key=openai_api_key)
openai.api_key = openai_api_key


async def generate_image(ctx, *, prompt: str):
    try:
        prompt, size = parse_image_size(prompt)
        async with ctx.typing():
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            image_data = requests.get(image_url).content
            image_file = BytesIO(image_data)
            image_file.seek(0)
            unique_filename = generate_unique_filename(prompt)
            image_discord = discord.File(fp=image_file, filename=unique_filename)

        await ctx.send(
            f"Generated Image -- every image you generate costs $0.04 so please keep that in mind\nPrompt: {prompt}",
            file=image_discord,
        )

    except openai.BadRequestError as e:
        error_message = str(e)

        if "content_policy_violation" in error_message:
            start = error_message.find("'message': '") + len("'message': '")
            end = error_message.find("', 'param'")
            important_message = error_message[start:end]
            await ctx.send(f"Error: {important_message}")

    except Exception as e:
        formatted_error = format_error_message(e)
        await ctx.send(f"An error occurred during image generation: {formatted_error}")
