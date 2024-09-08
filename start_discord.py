import os
import sys
import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from discord import Intents
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import importlib

# STEP 0: LOAD OUR DISCORD_TOKEN FROM .env FILE
load_dotenv()
upload_folder = "data"
os.makedirs(upload_folder, exist_ok=True)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

# Import your modules here
import src.components.pyautogui.gmail as gmail
import src.financial_crew.run_crew as crew

# Function to reload modules when a change is detected
def reload_modules():
    module_names = [
        'src.components.pyautogui.gmail',
        'src.financial_crew.run_crew'
    ]
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

async def send_message(message: discord.Message, user_message: str) -> None:
    if not user_message:
        print("(Message was empty because intents were not enabled probably)")
        return
    is_private = user_message[0] == "?"
    if is_private:
        user_message = user_message[1:]
    try:
        async with message.channel.typing():
            response = await gmail.login_via_bitwarden()
            if "No unread emails" in response or "No Attachment" in response:
                chunks = [response[i: i + 2000] for i in range(0, len(response), 2000)]
                for chunk in chunks:
                    if is_private:
                        await message.author.send(chunk)
                    else:
                        await message.channel.send(chunk)
            elif "Something Went Wrong!" in response:
                chunks = [response[i: i + 2000] for i in range(0, len(response), 2000)]
                for chunk in chunks:
                    if is_private:
                        await message.author.send(chunk)
                    else:
                        await message.channel.send(chunk)
            else:
                crew_response = str(crew.run_crew())
                response = response + "\n\n" + "------------------------" + "\n" + crew_response
                chunks = [response[i: i + 2000] for i in range(0, len(response), 2000)]
                for chunk in chunks:
                    if is_private:
                        await message.author.send(chunk)
                    else:
                        await message.channel.send(chunk)
    except Exception as e:
        print(f"An error occurred while sending a message: {e}")

async def run_finance_crew(message: discord.Message, user_message: str) -> None:
    if not user_message:
        print("(Message was empty because intents were not enabled probably)")
        return
    is_private = user_message[0] == "?"
    if is_private:
        user_message = user_message[1:]
    try:
        crew_response = str(crew.run_crew())
        response = crew_response
        chunks = [response[i: i + 2000] for i in range(0, len(response), 2000)]
        for chunk in chunks:
            if is_private:
                await message.author.send(chunk)
            else:
                await message.channel.send(chunk)
    except Exception as e:
        print(f"An error occurred while sending a message: {e}")

async def train_finance_crew(message: discord.Message, user_message: str) -> None:
    if not user_message:
        print("(Message was empty because intents were not enabled probably)")
        return
    is_private = user_message[0] == "?"
    if is_private:
        user_message = user_message[1:]
    try:
        response = await crew.train_crew()
        await message.author.send(response)
    except Exception as e:
        print(f"An error occurred while sending a message: {e}")

@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user:
        return
    user_message = message.content
    if user_message.startswith("!crew"):
        username = str(message.author)
        channel = str(message.channel)
        print(f'[{channel}] {username}: "{user_message}"')
        await send_message(message, user_message[len("!crew"):].strip())
    elif user_message.startswith("!run"):
        username = str(message.author)
        channel = str(message.channel)
        print(f'[{channel}] {username}: "{user_message}"')
        await run_finance_crew(message, user_message[len("!run"):].strip())
    elif user_message.startswith("!train"):
        username = str(message.author)
        channel = str(message.channel)
        print(f'[{channel}] {username}: "{user_message}"')
        await train_finance_crew(message, user_message[len("!train"):].strip())
    else:
        return

# Watchdog event handler for detecting changes in .py files
class ReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Detected change in {event.src_path}. Reloading modules...")
            reload_modules()

# Start the observer for watching file changes
def start_observer():
    event_handler = ReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path="src", recursive=True)  # Adjust path as needed
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
