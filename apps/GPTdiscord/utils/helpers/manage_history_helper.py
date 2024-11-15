import os
import openai
import asyncio
import random
import json
from pathlib import Path
from datetime import datetime
import regex as re
from colorama import Style, Fore

# from utils.helpers.solr_helper import solr
from dotenv import load_dotenv
from utils.helpers.prompt_helper import read_prompt, read_and_construct_prompt

load_dotenv()
system_prompt = read_prompt("./components/prompts/GPTbot_system_prompt.txt")
openai_model = os.getenv("MODEL_CHAT")


async def fetch_recent_messages(channel, bot, history_length=5):
    file_name = f"chat_history/{channel.id}.json"
    file_path = Path(file_name)
    if not file_path.exists():
        return []
    with open(file_path, "r") as file:
        messages = json.load(file)
    parsed_messages = sorted(
        messages, key=lambda x: datetime.fromisoformat(x["timestamp"])
    )
    recent_messages = parsed_messages[-history_length:]
    formatted_history = []
    for message in recent_messages:
        role = "assistant" if message["username"] == bot.user.name else "user"
        formatted_history.append(
            {"role": role, "content": f'{message["username"]}: {message["content"]}'}
        )
    return formatted_history


def combine_and_rank_results(history, solr_results):
    combined_results = []
    preface = {
        "role": "system",
        "content": "Below are messages from the past that may be relevant to the current conversation:",
    }
    combined_results.append(preface)
    for tier, results in solr_results.items():
        for result in results:
            if isinstance(result.get("username"), list) and isinstance(
                result.get("content"), list
            ):
                username = result["username"][0]
                content = result["content"][0]
                combined_results.append(
                    {"role": "user", "content": f"{username}: {content}", "tier": tier}
                )
            else:
                print("Warning: Unexpected data structure in Solr result")
    combined_results.extend(history)
    return combined_results


async def async_chat_completion(*args, **kwargs):
    response = await asyncio.to_thread(openai.chat.completions.create, *args, **kwargs)
    return response


async def perform_tiered_solr_search(message_author, expanded_keywords):
    solr_queries = {
        "Tier 1": [f'content:"{keyword}"' for keyword in expanded_keywords[0]],
        "Tier 2": [
            f'content:"{related}"'
            for keyword_list in expanded_keywords[1:]
            for related in keyword_list
            if related.strip()
        ],
    }
    solr_results = {}
    for tier, queries in solr_queries.items():
        if queries:
            combined_query = (
                f'username:"{message_author}" AND ({ " OR ".join(queries) })'
            )
            try:
                solr_results = []
            except Exception as e:
                print(f"Error querying Solr for {tier}: {e}")
        else:
            print(f"No valid queries for {tier}. Skipping Solr query for this tier.")
    return solr_results


async def fetch_message_history(channel, message_author, bot):
    history = await fetch_recent_messages(channel, bot, history_length=15)
    return history


async def get_expanded_keywords(message):
    user_prompt = read_and_construct_prompt(
        message, "./components/prompts/GPTbot_user_prompt.txt"
    )
    try:
        response = await async_chat_completion(
            model=openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=100,
        )
        topic_keywords_str = response.choices[0].message.content.strip()
        topic_keywords_str = re.sub(r"Keywords:\n\d+\.\s", "", topic_keywords_str)
        expanded_keywords = [
            kw.strip().split(",") for kw in topic_keywords_str.split("\n") if kw.strip()
        ]
        return expanded_keywords
    except Exception as e:
        print(Fore.RED + f"Error in getting expanded keywords: {e}" + Style.RESET_ALL)
        return None


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
    channel_ids_str = os.getenv("CHANNEL_IDS")
    if not channel_ids_str:
        return False, False
    allowed_channel_ids = [int(cid) for cid in channel_ids_str.split(",")]
    if message.author == bot.user or "Generated Image" in message.content:
        return False, False
    is_random_response = random.random() < 0.015
    is_mentioned = bot.user in [mention for mention in message.mentions]
    if is_mentioned or is_random_response or message.channel.id in allowed_channel_ids:
        return True, is_random_response
    return False, False
