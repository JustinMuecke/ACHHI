import discord 

from discord.ext import commands
from discord.ui import View
from discord import option
from core.scheduler import Scheduler
from database import get_score
from database import get_steam_id
from database import add_user
from database import remove_user
from core import Command
from core import command_type as ct
from ui.team_view import TeamView
class RegisteredView(View):
    def __init__(self, scheduler : Scheduler, bot : discord.Bot):
        super().__init__()
        self.scheduler = scheduler
        self.bot = bot

    @discord.ui.button(label="Score", style=discord.ButtonStyle.primary)
    async def score_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        score = get_score(interaction.user.id)
        if score:
            await interaction.response.send_message(f"Your Current Score is {score}!", ephemeral=True)
        else: 
            await interaction.response.send_message("You currently have no score. If you just registered it might take a few minutes to calculate your score!", ephemeral=True)


    @discord.ui.button(label="Update", style = discord.ButtonStyle.blurple)
    async def update_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        discord_id = interaction.user.id
        steam_id = get_steam_id(discord_id)
        self.scheduler.queue_command(Command(ct.UPDATE, discord_id, steam_id))
        await interaction.response.send_message("Your Point Update is Queued!", ephemeral=True)

    @discord.ui.button(label="Rank", style=discord.ButtonStyle.primary)
    async def rank_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        ranking = self.bot.ranking
        steam_id = get_steam_id(interaction.user.id)

        index = next((i for i, (id, _) in enumerate(ranking) if id == steam_id), None)
        if index:
            await interaction.response.send_message(f"Your current rank is: {index}", ephemeral=True)
        else: 
            await interaction.response.send_message(f"You do not have a rank, as no Points are registered", ephemeral=True)
    
    @discord.ui.button(label="Update Steam ID", style=discord.ButtonStyle.red)
    async def update_steam_id(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(ChangeSteamIDModal(self.scheduler))

    @discord.ui.button(label="Team Menu", style=discord.ButtonStyle.primary)
    async def team_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content="🧑‍💻👥 Welcome to the Team View! 🏗️ Under Construction... Please stand by. ⚙️🛠️", view=TeamView(self.scheduler, self.bot, self))


class ChangeSteamIDModal(discord.ui.Modal):
    def __init__(self, scheduler : Scheduler):
        super().__init__(title="Are you sure?")

        self.name_input = discord.ui.InputText(
            label="If you want to continue, input your new ID!"
        )
        self.add_item(self.name_input)
        self.scheduler = scheduler

    async def callback(self, interaction: discord.Interaction):
        steam_id = self.name_input.value
        discord_id = interaction.user.id
        remove_user(discord_id)
        add_user(discord_id, steam_id)
        self.scheduler.queue_command(Command(ct.REGISTER, discord_id, steam_id))
        await interaction.response.send_message("Your new ID is being processed.", ephemeral=True)






