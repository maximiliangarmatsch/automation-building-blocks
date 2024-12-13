import discord


async def generate_user_invite(
    server_name, channel_name, user_data, invite_user_data, guild_invites, client
):
    for guild in client.guilds:
        if guild.name == server_name:
            channel = discord.utils.get(guild.text_channels, name=channel_name)
            if channel:
                try:
                    invite = await channel.create_invite(max_uses=1, unique=True)

                    invite_user_data[invite.code] = user_data

                    # Update our invite cache
                    if guild.id not in guild_invites:
                        guild_invites[guild.id] = {}
                    guild_invites[guild.id][invite.code] = 0

                    print(f"Invite created: {invite.url} with data: {user_data}")
                    print(f"Updated invite cache: {guild_invites[guild.id]}")
                    print(f"Current invite_user_data: {invite_user_data}")
                    return invite.url
                except Exception as e:
                    print(f"Error creating invite: {e}")
                    return None
    return None
