import os
from colorama import Fore, Style
import json
from dotenv import load_dotenv

load_dotenv()


def generate_message_id(channel_id, timestamp):
    formatted_timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")
    return f"{channel_id}_{formatted_timestamp}"


def save_message_to_json_and_index_solr(channel_id, username, content, timestamp):
    filename = f"chat_history/{channel_id}.json"
    message_id = generate_message_id(channel_id, timestamp)
    data = {
        "id": message_id,
        "username": username,
        "content": content,
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
