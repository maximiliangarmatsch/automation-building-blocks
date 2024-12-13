import os
import discord
import asyncio
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from asgiref.wsgi import WsgiToAsgi
from quart import Quart, request, jsonify
from discord.ext import commands
from quart_cors import cors
from on_member_join_helper import (
    log_member_join,
    get_current_invites,
    identify_used_invite,
    handle_exception,
    handle_used_invite,
    update_invite_cache,
)
from generate_invite import generate_user_invite

load_dotenv()
app = Quart(__name__)
app = cors(app, allow_origin="*")

intents = discord.Intents.default()
intents.members = True  # Enable member events
intents.guilds = True  # Enable guild events
intents.invites = True  # Enable invite tracking
client = commands.Bot(command_prefix="!", intents=intents)
asgi_app = WsgiToAsgi(app)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Run the Discord bot in a background thread
loop = asyncio.get_event_loop()
invite_user_data = {}
invite_counts = {}
guild_invites = {}


@client.event
async def on_ready():
    print(f"Bot is ready. Logged in as {client.user}")
    for guild in client.guilds:
        try:
            invites = await guild.invites()
            guild_invites[guild.id] = {invite.code: invite.uses for invite in invites}
            print(f"Cached invites for guild: {guild.name}")
            print(f"Current invite cache: {guild_invites[guild.id]}")
        except Exception as e:
            print(f"Error caching invites for {guild.name}: {e}")


@client.event
async def on_member_join(member):
    global invite_user_data, guild_invites

    try:
        log_member_join(member, guild_invites, invite_user_data)

        # Delay to ensure invite data is updated
        await asyncio.sleep(1)

        # Retrieve invite data
        old_invite_dict = guild_invites.get(member.guild.id, {})
        current_invite_dict = await get_current_invites(member.guild)

        # Identify the used invite
        used_invite_code = identify_used_invite(
            old_invite_dict, current_invite_dict, invite_user_data
        )

        # Handle the used invite
        await handle_used_invite(used_invite_code, member, invite_user_data)

        # Update invite cache
        update_invite_cache(member.guild.id, current_invite_dict, guild_invites)

    except Exception as e:
        handle_exception(e)


@app.route("/join-discord", methods=["POST"])
async def join_discord():
    global invite_user_data, guild_invites
    data = await request.json
    username = data.get("username")
    server_name = data.get("server_name")
    channel_name = data.get("channel_name")
    user_id = data.get("user_id")

    if not all([username, server_name, channel_name, user_id]):
        return jsonify({"error": "Missing data"}), 400

    user_data = {"name": username, "preferences": "Loves coding", "role": "Developer"}
    invite_url = await generate_user_invite(
        server_name, channel_name, user_data, invite_user_data, guild_invites, client
    )
    if invite_url:
        return jsonify({"message": "Invite created", "invite_url": invite_url}), 200
    return jsonify({"error": "Failed to create invite"}), 500


async def main():
    try:
        bot_task = asyncio.create_task(client.start(DISCORD_TOKEN))
        app_task = asyncio.create_task(app.run_task(host="127.0.0.1", port=5000))
        await asyncio.gather(bot_task, app_task)
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        if not client.is_closed():
            await client.close()


if __name__ == "__main__":
    asyncio.run(main())
