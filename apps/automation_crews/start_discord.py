import os
import sys
import discord
import importlib
from dotenv import load_dotenv
from discord.ext import commands
from discord import Intents
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

assets_folder_path = "./financial_crew/assets"
os.makedirs(assets_folder_path, exist_ok=True)
# Import your modules here
import components.pyautogui.gmail as gmail
import financial_crew.run_crew as crew
import personal_assistant_crew.run_crew as assistant_crew

from dev_crew.app import WebsiteDevCrew
from dev_crew.crew_business import BusinessCrew
from dev_crew.crew_frontend import FrontendCrew
from components.discord.discord_helper_function import (
    send_message,
    run_finance_crew,
    train_finance_crew,
    run_assistant_crew,
    run_dev_crew,
)

# STEP 0: LOAD OUR DISCORD_TOKEN FROM .env FILE
load_dotenv()
upload_folder = "data"
os.makedirs(upload_folder, exist_ok=True)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())


# Function to reload modules when a change is detected
def reload_modules():
    module_names = ["components.pyautogui.gmail", "financial_crew.run_crew"]
    for module_name in module_names:
        if module_name in sys.modules:
            print(f"Reloading module: {module_name}")
            importlib.reload(sys.modules[module_name])


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(str(e))


@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user:
        return
    user_message = message.content
    if user_message.startswith("!crew"):
        username = str(message.author)
        channel = str(message.channel)
        print(f'[{channel}] {username}: "{user_message}"')
        await send_message(message, user_message[len("!crew") :].strip(), crew, gmail)
    elif user_message.startswith("!finance_crew"):
        username = str(message.author)
        channel = str(message.channel)
        print(f'[{channel}] {username}: "{user_message}"')
        await run_finance_crew(
            message, user_message[len("!finance_crew") :].strip(), crew, gmail
        )
    elif user_message.startswith("!assistant_crew"):
        username = str(message.author)
        channel = str(message.channel)
        print(f'[{channel}] {username}: "{user_message}"')
        await run_assistant_crew(
            message, user_message[len("!assistant_crew") :].strip(), assistant_crew
        )
    elif user_message.startswith("!dev_crew"):
        username = str(message.author)
        channel = str(message.channel)
        print(f'[{channel}] {username}: "{user_message}"')
        await run_dev_crew(
            message, user_message[len("!dev_crew") :].strip(), WebsiteDevCrew
        )

    elif user_message.startswith("!train"):
        username = str(message.author)
        channel = str(message.channel)
        print(f'[{channel}] {username}: "{user_message}"')
        await train_finance_crew(
            message, user_message[len("!train") :].strip(), crew, gmail
        )
    else:
        return


class ReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Detected change in {event.src_path}. Reloading modules...")
            reload_modules()


# Start the observer for watching file changes
def start_observer():
    event_handler = ReloadHandler()

    # Set path to current directory (assuming script is executed from 'src')
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
