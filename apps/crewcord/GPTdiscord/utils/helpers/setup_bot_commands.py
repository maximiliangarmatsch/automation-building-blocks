import discord
from components.pyautogui import gmail
from GPTdiscord.utils.helpers.discord_helper_function import (
    send_message,
    run_finance_crew,
    train_finance_crew,
    run_invoice_crew,
    run_dev_crew,
)
from dev_crew.app import WebsiteDevCrew
import finance_crew.execute_finance_crew as crew
import invoice_crew.execute_invoice_crew as invoice_crew
from GPTdiscord.utils.helpers.handle_gpt_response_helper import (
    handle_gpt_command,
    handle_refresh_command,
)
from GPTdiscord.utils.helpers.json_helper import (
    save_channel_history_to_json,
)
from GPTdiscord.utils.helpers.image_generator import generate_image
from GPTdiscord.utils.helpers.image_analyzer import image_analyzer


def setup_commands(bot, registered_channels_ids):
    @bot.event
    async def on_ready():
        await bot.tree.sync()
        for guild in bot.guilds:
            for channel in guild.text_channels:
                if channel.id in registered_channels_ids:
                    try:
                        await save_channel_history_to_json(channel)
                    except Exception as e:
                        print(f"Failed to save history for channel {channel.name} (ID: {channel.id}): {e}")

    @bot.command(name="generate")
    async def generate(ctx, *, prompt: str):
        try:
            await generate_image(ctx, prompt)
        except Exception as e:
            print(f"Debug: Error in generate command: {e}")  # Debug logging
            await ctx.send(f"An error occurred while generating the image: {e}")

    @bot.command(name="analyze")
    async def analyze(ctx):
        try:
            await image_analyzer(ctx)
        except Exception as e:
            print(f"Debug: Error in analyze command: {e}")  # Debug logging
            await ctx.send(f"An error occurred while analyzing the image: {e}")

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
        elif user_message.startswith("!invoice_crew"):
            await run_invoice_crew(
                message, user_message[len("!invoice_crew") :].strip(), invoice_crew
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

        elif message.content.startswith("!refresh"):
            await handle_refresh_command(message, bot)

        await bot.process_commands(message)
