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

steam_id = "Niievex"

#cmd_sched.queue_command(command(ct.REGISTER, steam_id))
with open("Hunters/" + steam_id+".hunt", "rb") as file:
    hunter : Hunter = pickle.load(file)
    message = str(hunter.score)
print(message)

output = t2a(
    header=["Rank", "Hunter", "Score"],
    body = calculate_scoreboard_around_hunter(steam_id),
    style=PresetStyle.thin_compact
)
print(output)

if(steam_id.lower()+".hunt" not in os.listdir("Hunters")):
        message = "User not Registered. Use /register to register a new Achievement Hunter"
with open("Hunters/"+steam_id+".hunt", "rb") as file:
    hunter : Hunter = pickle.load(file)
    message = str(hunter.score)
print(message)