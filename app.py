"""
DBS main module
"""
import os
import discord
import requests
from typing import Final
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from discord import Intents, Client, Message
from pyautogui_gmail import login_via_bitwarden

# STEP 0: LOAD OUR TOKEN FROM .env FILE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = "/", intents = discord.Intents.all())

@bot.event
async def on_ready():
    """
    This function is called automatically when the bot has successfully logged in
    and is ready to start interacting with the Discord API.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    print("Bot is ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(str(e))

@bot.tree.command(name="email")
@app_commands.describe(query="Type email description here")
async def email(interaction: discord.Interaction, query: str):
    """
    This command takes an email query, processes it, and sends a response back to the user..

    Parameters
    ----------
    interaction : discord.Interaction
        The interaction object that represents the command invocation context.
    query : str
        user input or query.

    Returns
    -------
    None
    """
    await interaction.response.defer()
    try:
        response = "Hello Email"
        await interaction.followup.send(f"{response}")
    except discord.errors.NotFound as e:
        print(f"Interaction error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

@bot.tree.command(name = "linkedin")
@app_commands.describe(query="Type essay description here")
async def essay(interaction: discord.Interaction, query: str):
    """
    This command takes an essay query, processes it, and sends a response back to the user.

    Parameters
    ----------
    interaction : discord.Interaction
        The interaction object that represents the command invocation context.
    query : str
        user query or input.

    Returns
    -------
    None
    """
    await interaction.response.defer()
    try:
        response = "Hello Linkedin"
        await interaction.followup.send(f"{response}")
    except discord.errors.NotFound as e:
        print(f"Interaction error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# STEP 2: MESSAGE FUNCTIONALITY
async def send_message(message: discord.Message, user_message: str) -> None:
    """
    doc string
    """
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    is_private = user_message[0] == '?'
    if is_private:
        user_message = user_message[1:]

    try:
        # Use the typing context manager to show typing indicator
        async with message.channel.typing():
            response: str = await login_via_bitwarden()
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# STEP 4: HANDLING INCOMING MESSAGES
@bot.event
async def on_message(message: discord.Message) -> None:
    """
    doc string
    """
    if message.author == bot.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    print(f'[{channel}] {username}: "{user_message}"')

    await send_message(message, user_message)


# STEP 5: MAIN ENTRY POINT
def main() -> None:
    """
    This function initializes and runs the Discord bot using the provided token.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    bot.run(token=TOKEN)


if __name__ == '__main__':
    main()
