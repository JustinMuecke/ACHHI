import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from user import Hunter
from scoreboard_calculator import calculate_scoreboard
from scoreboard_calculator import calculate_scoreboard_around_hunter
import threading
import pickle
from table2ascii import table2ascii as t2a, PresetStyle
from command_scheduler import scheduler
from command_type import command_type as ct
from command import command

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
TOKEN = str(os.getenv("BOT_TOKEN"))
SERVERID = int(os.getenv("SERVER_ID"))



error_counter = 0
directory = os.fsencode("Hunters")
cmd_sched = scheduler()
thread = threading.Thread(target=cmd_sched.run)
thread.start()
print("Starting Bot")

@tree.command(
    name="register",
    description="Registers a new Achievement Hunter. It may take a few minutes.",
    guild = discord.Object(id=SERVERID)
)
async def register(interaction, steam_id : str):
    message : str
    try:
        if(steam_id.lower()+".hunt" in os.listdir("Hunters")):
            message="SteamID already Registered. Use /score to see the recorded score."
        else:
            cmd_sched.queue_command(command(ct.REGISTER, steam_id))
            message="Achievement Hunter is being registered. This may take a while."

    except Exception as e:
        message="Registration failed. Please Verify the SteamID is written correctly. Alternatively, send us a ticket using /error."
        e.with_traceback()

    await interaction.response.send_message(message)


@tree.command(
        name="update",
        description="Update Single Hunter",
        guild=discord.Object(id=SERVERID)
)
async def update(interaction, steam_id : str):
    try:
        if(steam_id+".hunt" not in os.listdir("Hunters")):
            message = "User not Registered. Use /register to register a new Achievement Hunter"
        else:
            print("Scheduling Update")
            cmd_sched.queue_command(command(ct.UPDATE, steam_id))
            message="Achievement Hunter is being updated. This may take a while."

    except Exception as e:
        message="Registration failed. Please Verify the SteamID is written correctly. Alternatively, send us a ticket using /error."
        e.with_traceback()

    await interaction.response.send_message(message)




@tree.command(
    name="scoreboard",
    description="Shows the Scoreboard",
    guild = discord.Object(id=SERVERID)
)
async def scoreboard(interaction):
    output = t2a(
        header=["Rank","Hunter", "Score"],
        body=calculate_scoreboard(),
        style=PresetStyle.thin_compact
)
    await interaction.response.send_message(f"```\n{output}\n```")


@tree.command(
    name="scoreboard_hunter",
    description="Shows the Scoreboard around an individual",
    guild = discord.Object(id=SERVERID)
)
async def scoreboard_hunter(interaction, steam_id : str):
    output = t2a(
        header=["Rank","Hunter", "Score"],
        body=calculate_scoreboard_around_hunter(steam_id),
        style=PresetStyle.thin_compact
)
    await interaction.response.send_message(f"```\n{output}\n```")

@tree.command(
    name = "score",
    description="Shows the score of a given SteamID",
    guild = discord.Object(id=SERVERID)
)
async def score(interaction, steam_id : str):
    print("Scoring")
    message : str
    if(steam_id.lower()+".hunt" not in os.listdir("Hunters")):
        print("Hunter not Registered")
        message = "User not Registered. Use /register to register a new Achievement Hunter"
    else:
        with open("Hunters/"+steam_id.lower()+".hunt", "rb") as file:
            hunter : Hunter = pickle.load(file)
            message = str(hunter.score)
    await interaction.response.send_message(message)

@tree.command(
    name = "error",
    description = "Send us information about a error you encountered",
    guild = discord.Object(id=SERVERID)
)
async def error(interaction, error_message : str, error_counter : int = error_counter):
    with open("Errors/error-" + str(error_counter), "w") as file:
        file.write(error_message)
    error_counter += 1
    await interaction.response.send_message("Error has been reported")

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=SERVERID))
    print('We have logged in as {0.user}'.format(client))

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return

#    if message.content.startswith('$hello'):
#        await message.channel.send('Hello!')

client.run(TOKEN)
