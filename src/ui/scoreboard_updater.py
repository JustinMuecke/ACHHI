import asyncio
import discord
import os
from typing import List, Tuple
from database import get_steam_ids_sorted_by_points


async def hourly_scoreboard_update(bot: discord.Bot):
    await bot.wait_until_ready()

    guild_id = int(os.getenv("GUILD_ID"))
    channel_id = int(os.getenv("CHANNEL_ID"))

    channel = bot.get_channel(channel_id)
    if channel is None:
        try:
            channel = await bot.fetch_channel(channel_id)
        except Exception as e:
            print(f"❌ Failed to fetch channel: {e}")
            return

    print("✅ Scoreboard loop started")
    scoreboard_message: discord.Message = None  # To store the message reference

    while True:
        print("🔁 Updating scoreboard...")

        users: List[Tuple[str, int]] = get_steam_ids_sorted_by_points()
        bot.ranking = users

        # Build the markdown scoreboard
        header = "**🏆 ACHHI Scoreboard 🏆**\n"
        table_header = "```\nRank | Steam ID         | Score\n" + "-" * 32
        rows = [
            f"{i:>4} | {steam_id[:15]:<15} | {score:>5}"
            for i, (steam_id, score) in enumerate(users, start=1)
        ]
        table_footer = "```"
        message_content = header + table_header + "\n" + "\n".join(rows) + "\n" + table_footer

        if isinstance(channel, discord.TextChannel):
            if scoreboard_message is None:
                # Send the message the first time and store it
                scoreboard_message = await channel.send(message_content)
            else:
                # Edit the existing message
                try:
                    await scoreboard_message.edit(content=message_content)
                except discord.NotFound:
                    # Message was deleted — send a new one
                    scoreboard_message = await channel.send(message_content)
        else:
            print("⚠️ Channel is not a text channel")

        await asyncio.sleep(60)  # every hour