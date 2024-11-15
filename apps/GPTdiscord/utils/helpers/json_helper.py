import os
import json
import glob
import datetime
from datetime import datetime, timedelta, timezone
from colorama import Fore, Style
from utils.helpers.solr_helper import generate_message_id
from pathlib import Path


def clear_channel_history(channel):
    file_name = f"chat_history/{channel.id}.json"
    file_path = Path(file_name)
    if file_path.exists():
        with open(file_path, "w") as file:
            file.write("[]")
        print(f"Cleared JSON data for channel ID: {channel.id}")
        return True
    else:
        return False


async def save_channel_history_to_json(channel):
    file_name = f"chat_history/{channel.id}.json"
    existing_data = []
    new_message_count = 0
    file_exists_for_channel = os.path.exists(file_name)
    days_to_look_back = 15 if file_exists_for_channel else 365
    try:
        if file_exists_for_channel:
            with open(file_name, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        else:
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(existing_data, file)
    except PermissionError as e:
        print(
            Fore.RED
            + f"PermissionError: Unable to create or read file {file_name} for channel {channel.name}. Error: {e}"
            + Style.RESET_ALL
        )
        return
    except Exception as e:
        print(
            Fore.RED
            + f"Error: Unable to create or read file {file_name} for channel {channel.name}. Error: {e}"
            + Style.RESET_ALL
        )
        return

    processed_messages = 0
    after_date = datetime.now(timezone.utc) - timedelta(days=days_to_look_back)

    async for message in channel.history(
        limit=None, oldest_first=True, after=after_date
    ):
        if message.content.startswith("!gpt"):
            message_id = generate_message_id(channel.id, message.created_at)
            if not any(msg["id"] == message_id for msg in existing_data):
                new_message = {
                    "id": message_id,
                    "username": str(message.author),
                    "content": message.content,
                    "timestamp": message.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")[
                        :-3
                    ],
                }
                existing_data.append(new_message)
                new_message_count += 1
                processed_messages += 1
    if new_message_count > 0:
        try:
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(existing_data, file, indent=4, ensure_ascii=False)
        except PermissionError as e:
            print(
                Fore.RED
                + f"PermissionError: Unable to write to file {file_name} for channel {channel.name}. Error: {e}"
                + Style.RESET_ALL
            )
        except Exception as e:
            print(
                Fore.RED
                + f"Error: Unable to write to file {file_name} for channel {channel.name}. Error: {e}"
                + Style.RESET_ALL
            )


def index_all_json_files(directory):
    json_files = glob.glob(f"{directory}/*.json")
    for idx, json_file_path in enumerate(json_files, start=1):
        channel_id = os.path.splitext(os.path.basename(json_file_path))[0]
        with open(json_file_path, "r") as file:
            data = json.load(file)
            if not data:
                continue
            new_entries = 0
            for entry in data:
                timestamp = datetime.strptime(
                    entry["timestamp"], "%Y-%m-%dT%H:%M:%S.%f"
                )
                entry["id"] = generate_message_id(channel_id, timestamp)
                try:
                    new_entries += 1
                except Exception as e:
                    print(
                        Fore.RED
                        + f"Failed to index entry from {json_file_path}. Error: {e}"
                        + Style.RESET_ALL
                    )
