import os
import asyncio
import re
import openai
from dotenv import load_dotenv
from GPTdiscord.utils.helpers.manage_history_helper import (
    fetch_message_history,
    remove_redundant_messages,
    split_message,
    should_bot_respond_to_message,
)
from GPTdiscord.utils.helpers.json_helper import (
    save_message_to_json,
    clear_user_history,
)
from GPTdiscord.utils.helpers.image_analysis_helper import handle_image_attachments
from GPTdiscord.utils.helpers.prompt_helper import read_prompt

load_dotenv()

system_prompt = read_prompt("./GPTdiscord/components/prompts/GPTbot_system.txt")
RATE_LIMIT = 0.25


async def chat_completion(*args, **kwargs):
    response = await asyncio.to_thread(openai.chat.completions.create, *args, **kwargs)
    return response


async def handle_response_chunks(message, airesponse, user_message):
    airesponse_chunks = split_message(airesponse)
    final_response = ""
    for chunk in airesponse_chunks:
        chunk = re.sub(r"^([^\s:]+(\s+[^\s:]+)?):\s*", "", chunk)
        final_response = final_response + chunk
        sent_message = await message.channel.send(chunk)
        await asyncio.sleep(RATE_LIMIT)
    save_message_to_json(
        message.channel.id,
        message.author.name,
        user_message,
        message.created_at,
        final_response,
    )


async def handle_chat_response(message, user_message, is_random_response, bot):
    messages_with_solr = await fetch_message_history(
        message.channel, message.author.name, bot
    )

    system_message = {"role": "system", "content": system_prompt}
    current_user_message = {
        "role": "user",
        "content": f"{message.author.name}: {user_message}",
    }

    assistant_prompt = {
        "role": "assistant",
        "content": "Keep the current conversation going",
    }

    messages_for_openai = (
        [system_message] + messages_with_solr + [current_user_message, assistant_prompt]
    )

    try:
        async with message.channel.typing():
            filtered_messages = remove_redundant_messages(messages_for_openai)
            max_tokens = (
                int(os.getenv("MAX_TOKENS_RANDOM"))
                if is_random_response
                else int(os.getenv("MAX_TOKENS"))
            )
            response = await chat_completion(
                model=os.getenv("MODEL_CHAT"),
                messages=filtered_messages,
                temperature=1.5,
                top_p=0.9,
                max_tokens=max_tokens,
            )
            airesponse = response.choices[0].message.content
            await handle_response_chunks(message, airesponse, user_message)

    except openai.OpenAIError as e:
        await message.channel.send(
            f"An error has occurred with your request. Please try again. Error details: {e}"
        )

    except Exception:
        await message.channel.send("An unexpected error has occurred.")


async def handle_gpt_command(message, bot):
    user_message = message.content[len("!gpt") :].strip()
    should_respond, is_random_response = should_bot_respond_to_message(message, bot)
    is_mentioned = bot.user in message.mentions

    if message.attachments:
        await handle_image_attachments(message, is_mentioned)
        return

    if should_respond:
        await handle_chat_response(message, user_message, is_random_response, bot)


async def handle_refresh_command(message, bot):
    clear_user_history(message.channel, message)
    await message.channel.send("Cleared Previous Chat")
