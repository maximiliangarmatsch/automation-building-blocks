import openai
import asyncio
from utils.helpers.solr_helper import solr


async def fetch_recent_messages(channel, bot, history_length=15):
    message_history = []
    async for message in channel.history(limit=history_length, oldest_first=False):
        user_mention = f"{message.author.name}: " if message.author != bot.user else ""
        role = "assistant" if message.author == bot.user else "user"
        message_history.append(
            {"role": role, "content": f"{user_mention}{message.content}"}
        )
    return message_history


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
                results = solr.search(combined_query, **{"rows": 10})
                solr_results[tier] = results.docs
            except Exception as e:
                print(f"Error querying Solr for {tier}: {e}")
        else:
            print(f"No valid queries for {tier}. Skipping Solr query for this tier.")
    return solr_results


async def fetch_message_history(channel, message_author, expanded_keywords, bot):
    history = await fetch_recent_messages(channel, bot, history_length=15)
    solr_results = await perform_tiered_solr_search(message_author, expanded_keywords)
    combined_results = combine_and_rank_results(history, solr_results)
    return combined_results
