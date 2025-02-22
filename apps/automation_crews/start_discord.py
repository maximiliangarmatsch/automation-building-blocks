import os
import sys
import discord
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
from utils.helper.module_watcher import start_observer
from GPTdiscord.utils.helpers.setup_bot_commands import setup_commands

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_model = os.getenv("MODEL_CHAT")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

registered_channels_ids = [
    int(id.strip())
    for id in os.getenv("REGISTERED_CHANNEL_IDS", "").strip("[]").split(",")
]

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

setup_commands(bot, registered_channels_ids)

def start_discord():
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    observer = start_observer()
    try:
        start_discord()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()