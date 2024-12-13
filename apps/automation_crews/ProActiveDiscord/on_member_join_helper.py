import asyncio
import discord
from discord.ext import commands


def log_member_join(member, guild_invites, invite_user_data):
    print(f"\nMember joined: {member.name}")
    print(f"Current invite cache before join: {guild_invites.get(member.guild.id, {})}")
    print(f"Current invite_user_data: {invite_user_data}")


async def get_current_invites(guild):
    try:
        current_invites = await guild.invites()
        return {invite.code: invite.uses for invite in current_invites}
    except Exception as e:
        print(f"Error fetching current invites: {e}")
        return {}


def identify_used_invite(old_invite_dict, current_invite_dict, invite_user_data):
    # Check for single-use invite disappearance
    for old_code in old_invite_dict:
        if old_code not in current_invite_dict and old_code in invite_user_data:
            print(f"Found used single-use invite: {old_code}")
            return old_code

    # Check for multi-use invite with increased use count
    for invite_code, uses in current_invite_dict.items():
        old_uses = old_invite_dict.get(invite_code, 0)
        if uses > old_uses:
            print(f"Found used multi-use invite: {invite_code}")
            return invite_code

    print("Could not find the invite used.")
    return None


async def handle_used_invite(used_invite_code, member, invite_user_data):
    if used_invite_code:
        custom_data = invite_user_data.get(used_invite_code)
        if custom_data:
            await send_welcome_message(
                member, custom_data, used_invite_code, invite_user_data
            )
        else:
            print(f"No custom data found for invite code: {used_invite_code}")
    else:
        print(f"Could not find the invite used by {member.name}")
        print("Available invite codes in user data:", list(invite_user_data.keys()))


async def send_welcome_message(member, custom_data, used_invite_code, invite_user_data):
    welcome_channel = discord.utils.get(
        member.guild.text_channels, name="general"
    )  # Adjust channel name as needed
    if welcome_channel:
        welcome_message = (
            f"Welcome to {member.guild.name}, {member.mention}! \U0001F389\n"
            f"Custom Info: {custom_data}\n"
            f"We're thrilled to have you here!"
        )
        await welcome_channel.send(welcome_message)
        print(f"Sent welcome message for {member.name}")

        # Clean up used invite data
        del invite_user_data[used_invite_code]
        print(f"Cleaned up invite data for code: {used_invite_code}")


def update_invite_cache(guild_id, current_invite_dict, guild_invites):
    guild_invites[guild_id] = current_invite_dict
    print(f"Updated invite cache for guild ID {guild_id}")


def handle_exception(e):
    print(f"Error in on_member_join: {e}")
    import traceback

    traceback.print_exc()
