import discord
import os
import asyncio
import threading

from core.scheduler.command_scheduler import Scheduler

from ui.unregistered_view import Unregistered_View
from ui.scoreboard_updater import hourly_scoreboard_update
from ui.registered_view import RegisteredView

from database.database_setup import setup_database
from database.database import user_registered


intents = discord.Intents.default()
intents.guilds = True

achhi = discord.Bot(intents=intents)
server_id = os.getenv("GUILD_ID")
setup_database()

@achhi.event
async def on_ready():
    print(f"Bot is ready as {achhi.user}")
    asyncio.create_task(hourly_scoreboard_update(achhi))

cmd_sched = Scheduler()
thread = threading.Thread(target=cmd_sched.run)
thread.start()

@achhi.slash_command(name="bot", description="Launch the ACHHI Bot", guild_ids=[server_id])
async def bot_command(context):
    steam_id = user_registered(context.author.id)
    registered_view = RegisteredView(cmd_sched, achhi)
    unregistered_view = Unregistered_View(cmd_sched, registered_view)
    if not steam_id:
        await context.respond("Welcome to the ACHHI! Feel free to register to participate!", view=unregistered_view, ephemeral=True)
    else:
        await context.respond(f"Welcome back {steam_id}", view=registered_view, ephemeral=True)

achhi.run(os.environ["DISCORD_TOKEN"])


