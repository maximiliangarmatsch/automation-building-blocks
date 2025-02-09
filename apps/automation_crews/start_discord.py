import os
import sys
import importlib
import openai
import discord
from openai import OpenAI
from discord.ext import commands
from discord import Intents
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
from components.pyautogui import gmail
from components.discord.discord_helper_function import (
    send_message,
    run_finance_crew,
    train_finance_crew,
    run_assistant_crew,
    run_dev_crew,
)

import financial_crew.execute_financial_crew as crew
import personal_assistant_crew.execute_assistant_crew as assistant_crew
from dev_crew.app import WebsiteDevCrew
from GPTdiscord.utils.helpers.discord_helper import (
    handle_gpt_command,
    handle_refresh_command,
)
from GPTdiscord.utils.helpers.json_helper import (
    save_channel_history_to_json,
    index_all_json_files,
)
from GPTdiscord.utils.helpers.image_generator import generate_image
from GPTdiscord.utils.helpers.image_analyzer import image_analyzer

load_dotenv()

assets_folder_path = "./financial_crew/assets"
os.makedirs(assets_folder_path, exist_ok=True)

directory = "./GPTdiscord/chat_history"
if not os.path.exists(directory):
    os.makedirs(directory)

upload_folder = "data"
os.makedirs(upload_folder, exist_ok=True)

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_model = os.getenv("MODEL_CHAT")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

registered_channels_ids = [
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

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())


# Function to reload modules when a change is detected
def reload_modules():
    module_names = ["components.pyautogui.gmail", "financial_crew.execute_financial_crew", "personal_assistant_crew.execute_assistant_crew"]
    for module_name in module_names:
        if module_name in sys.modules:
            print(f"Reloading module: {module_name}")
            importlib.reload(sys.modules[module_name])


@bot.event
async def on_ready():
    await bot.tree.sync()
    for _guild_idx, guild in enumerate(bot.guilds, start=1):
        all_channels = guild.text_channels
        processed_channels = set()
        for channel in all_channels:
            if channel.id in registered_channels_ids:
                try:
                    await save_channel_history_to_json(channel)
                    processed_channels.add(channel.id)
                except Exception as e:
                    print(
                        f"Failed to save history for channel {channel.name} (ID: {channel.id}): {e}"
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
    await generate_image(ctx, client, prompt)


@bot.command(
    name="analyze",
    help="Analyzes an attached image and provides a description.\n\n"
    "Attach an image (PNG, JPG, JPEG, WEBP) to the command, and the bot will\n"
    "analyze the image and provide a detailed description based on AI.",
)
async def analyze(ctx):
    await image_analyzer(ctx)


@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user:
        return
    user_message = message.content
    if user_message.startswith("!crew"):
        await send_message(message, user_message[len("!crew") :].strip(), crew, gmail)
    elif user_message.startswith("!finance_crew"):
        await run_finance_crew(
            message, user_message[len("!finance_crew") :].strip(), crew, gmail
        )
    elif user_message.startswith("!assistant_crew"):
        await run_assistant_crew(
            message, user_message[len("!assistant_crew") :].strip(), assistant_crew
        )
    elif user_message.startswith("!dev_crew"):
        await run_dev_crew(
            message, user_message[len("!dev_crew") :].strip(), WebsiteDevCrew
        )

    elif user_message.startswith("!train"):
        await train_finance_crew(
            message, user_message[len("!train") :].strip(), crew, gmail
        )
    elif message.content.startswith("!gpt"):
        await handle_gpt_command(message, bot)
        return
    elif message.content.startswith("!refresh"):
        await handle_refresh_command(message, bot)
        return
    else:
        return
    await bot.process_commands(message)


class ReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            reload_modules()


# Start the observer for watching file changes
def start_observer():
    event_handler = ReloadHandler()
    watch_path = os.path.abspath(".")
    observer = Observer()
    observer.schedule(event_handler, path=watch_path, recursive=True)
    observer.start()
    return observer


def start_discord():
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    observer = start_observer()
    try:
        start_discord()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
