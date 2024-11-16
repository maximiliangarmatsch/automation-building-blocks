import os
import discord
import openai
import requests
from io import BytesIO
from openai import OpenAI
from colorama import init, Fore, Style
from discord.ext import commands
from dotenv import load_dotenv
from utils.helpers.image_analysis_helper import encode_discord_image, analyze_image
from utils.helpers.openai_message_format_helper import format_error_message
from utils.helpers.discord_helper import handle_gpt_command, handle_refresh_command
from utils.helpers.json_helper import save_channel_history_to_json, index_all_json_files
from utils.helpers.generate_image_helper import (
    parse_image_size,
    generate_unique_filename,
)

load_dotenv()

directory = "chat_history"
if not os.path.exists(directory):
    os.makedirs(directory)
init(autoreset=True)

openai_api_key = os.getenv("OPENAI_API_KEY")
discord_bot_token = os.getenv("DISCORD_TOKEN")
openai_model = os.getenv("MODEL_CHAT")

regsitered_channels_ids = registered_channels_ids = [
    int(id.strip())
    for id in os.getenv("REGISTERED_CHANNEL_IDS", "").strip("[]").split(",")
]

client = OpenAI(api_key=openai_api_key)
openai.api_key = openai_api_key
user_chat_history = {}
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

index_all_json_files("chat_history/")


@bot.event
async def on_ready():

    for guild_idx, guild in enumerate(bot.guilds, start=1):
        all_channels = guild.text_channels
        processed_channels = set()

        for channel in all_channels:
            if channel.id in regsitered_channels_ids:
                try:
                    await save_channel_history_to_json(channel)
                    processed_channels.add(channel.id)
                except Exception as e:
                    print(
                        Fore.RED
                        + f"Failed to save history for channel {channel.name} (ID: {channel.id}): {e}"
                        + Style.RESET_ALL
                    )
            else:
                continue


@bot.command(
    name="generate",
    help="Generates an image using DALL-E 3.\n\n"
    "Options:\n"
    "--wide: Generates a wide image (1920x1024).\n"
    "--tall: Generates a tall image (1024x1920).\n"
    "--seed <number>: Use a specific seed for image generation.\n\n"
    "Default size is 1024x1024. The prompt costs $0.04 per image.",
)
async def generate(ctx, *, prompt: str):

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
        print(Fore.RED + formatted_error + Fore.RESET)


@bot.command(
    name="analyze",
    help="Analyzes an attached image and provides a description.\n\n"
    "Attach an image (PNG, JPG, JPEG, WEBP) to the command, and the bot will\n"
    "analyze the image and provide a detailed description based on AI.",
)
async def analyze(ctx):

    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]

        if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            async with ctx.typing():

                try:
                    base64_image = await encode_discord_image(attachment.url)
                    instructions = "Please describe the image."
                    analysis_result = await analyze_image(base64_image, instructions)
                    response_text = (
                        analysis_result.get("choices", [{}])[0]
                        .get("message", {})
                        .get("content", "")
                    )

                    if response_text:
                        await ctx.send(response_text)
                    else:
                        await ctx.send("Sorry, I couldn't analyze the image.")

                except Exception as e:
                    error_details = str(e)
                    if hasattr(e, "response") and e.response is not None:
                        error_details += f" Response: {e.response.text}"
                    formatted_error = format_error_message(error_details)
                    await ctx.send(formatted_error)
                    print(Fore.RED + formatted_error + Fore.RESET)
    else:
        await ctx.send("Please attach an image to analyze.")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("!gpt"):
        await handle_gpt_command(message, bot)
        return

    if message.content.startswith("!refresh"):
        await handle_refresh_command(message)
        return

    await bot.process_commands(message)


if discord_bot_token is None:
    raise ValueError(
        "No Discord bot token found. Make sure to set the DISCORD_BOT_TOKEN environment variable."
    )
bot.run(discord_bot_token)
