import os
import random
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from GPTdiscord.utils.helpers.prompt_helper import read_prompt

load_dotenv()
system_prompt = read_prompt("./GPTdiscord/components/prompts/GPTbot_system.txt")
openai_model = os.getenv("MODEL_CHAT")


async def fetch_recent_messages(channel, bot, history_length=5):
    file_name = f"./GPTdiscord/chat_history/{channel.id}.json"
    file_path = Path(file_name)
    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        messages = json.load(file)
    parsed_messages = sorted(
        messages, key=lambda x: datetime.fromisoformat(x["timestamp"])
    )
    recent_messages = parsed_messages[-history_length:]

    formatted_history = []
    for message in recent_messages:
        if message["username"] == bot.user.name:
            if "assistant" in message and message["assistant"]:
                role = "assistant"
                content = f'{message["assistant"][0]}: {message["assistant"][1]}'
            elif "user" in message and message["user"]:
                role = "user"
                content = f'{message["user"][0]}: {message["user"][1]}'
            else:
                continue
            formatted_history.append({"role": role, "content": content})
    return formatted_history


async def fetch_message_history(channel, message_author, bot):
    history = await fetch_recent_messages(channel, bot, history_length=15)
    return history


def split_message(message_content, min_length=1500):
    chunks = []
    remaining = message_content
    while len(remaining) > min_length:
        index = max(
            remaining.rfind(".", 0, min_length),
            remaining.rfind("!", 0, min_length),
            remaining.rfind("?", 0, min_length),
        )
        if index == -1:
            index = min_length
        chunks.append(remaining[: index + 1])
        remaining = remaining[index + 1 :]
    chunks.append(remaining)
    return chunks


def remove_redundant_messages(messages):
    filtered_messages = []
    last_message = None
    for message in messages:
        if message != last_message:
            filtered_messages.append(message)
        else:
            print(f"Redundant message detected and removed: {message}")
        last_message = message
    return filtered_messages


def should_bot_respond_to_message(message, bot):
    allowed_channel_ids = [
        int(id.strip())
        for id in os.getenv("REGISTERED_CHANNEL_IDS", "").strip("[]").split(",")
    ]
    if not allowed_channel_ids:
        return False, False
    if message.author == bot.user or "Generated Image" in message.content:
        return False, False
    is_random_response = random.random() < 0.015
    is_mentioned = bot.user in [mention for mention in message.mentions]
    if is_mentioned or is_random_response or message.channel.id in allowed_channel_ids:
        return True, is_random_response
    return False, False
