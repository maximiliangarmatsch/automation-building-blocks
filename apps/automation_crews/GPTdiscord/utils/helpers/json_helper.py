import os
import json
import glob
import datetime
from datetime import datetime, timedelta, timezone
from pathlib import Path


def generate_message_id(channel_id, timestamp):
    formatted_timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")
    return f"{channel_id}_{formatted_timestamp}"


def clear_user_history(channel, query):
    file_name = f"./GPTdiscord/chat_history/{channel.id}.json"
    file_path = Path(file_name)

    if file_path.exists():
        with open(file_name, "r", encoding="utf-8") as file:
            try:
                messages = json.load(file)
            except json.JSONDecodeError:
                print("Failed to decode JSON. Resetting file.")
                messages = []

        updated_messages = [
            message for message in messages if message["username"] != query.author.name
        ]

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(updated_messages, file, indent=4)

        return True
    else:
        return False


async def save_channel_history_to_json(channel):
    file_name = f"./GPTdiscord/chat_history/{channel.id}.json"
    days_to_look_back = 15 if os.path.exists(file_name) else 365

    try:
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        else:
            existing_data = []

    except (PermissionError, Exception) as e:
        print(f"Error handling file {file_name} for {channel.name}: {e}")
        return

    after_date = datetime.now(timezone.utc) - timedelta(days=days_to_look_back)
    new_messages = []

    async for message in channel.history(
        limit=None, oldest_first=True, after=after_date
    ):

        if message.content.startswith("!gpt"):
            message_id = generate_message_id(channel.id, message.created_at)

            if not any(msg["id"] == message_id for msg in existing_data):
                new_messages.append(
                    {
                        "id": message_id,
                        "username": str(message.author),
                        "user": [
                            "user",
                            message.content,
                        ],
                        "assistant": ["assistant", ""],
                        "timestamp": message.created_at.strftime(
                            "%Y-%m-%dT%H:%M:%S.%f"
                        )[:-3],
                    }
                )

    if new_messages:
        try:
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(
                    existing_data + new_messages, file, indent=4, ensure_ascii=False
                )
        except (PermissionError, Exception) as e:
            print(f"Error writing to file {file_name} for {channel.name}: {e}")


def index_all_json_files(directory):
    json_files = glob.glob(f"{directory}/*.json")

    for idx, json_file_path in enumerate(json_files, start=1):
        channel_id = os.path.splitext(os.path.basename(json_file_path))[0]

        with open(json_file_path, "r", encoding="utf-8") as file:
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
                    print(f"Failed to index entry from {json_file_path}. Error: {e}")


def save_message_to_json(channel_id, username, content, timestamp, airesponse):
    filename = f"./GPTdiscord/chat_history/{channel_id}.json"
    message_id = generate_message_id(channel_id, timestamp)
    data = {
        "id": message_id,
        "username": username,
        "user": ["user", content],
        "assistant": ["assistant", airesponse],
        "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f"),
    }

    if os.path.exists(filename):
        with open(filename, "r+", encoding="utf-8") as file:
            file_data = json.load(file)
            if not any(msg["id"] == message_id for msg in file_data):
                file_data.append(data)
                file.seek(0)
                file.truncate()
                json.dump(file_data, file, indent=4, ensure_ascii=False)

    else:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump([data], file, indent=4, ensure_ascii=False)
