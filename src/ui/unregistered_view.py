import discord

from discord.ui import View
from database.database import add_user
from core.scheduler.command_scheduler import Scheduler
from core.scheduler.command_type import command_type as ct
from core.scheduler.command import Command


class Unregistered_View(View):
    def __init__(self, scheduler : Scheduler, registered_view):
        super().__init__()
        self.scheduler = scheduler
        self.registered_view = registered_view
    @discord.ui.button(label="Register", style=discord.ButtonStyle.primary)
    async def click_me_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(RegisterModal(self.scheduler, self.registered_view))

class RegisterModal(discord.ui.Modal):
    def __init__(self, scheduler : Scheduler, registered_view):
        super().__init__(title="Register")

        self.name_input = discord.ui.InputText(label="Enter your Steam ID")
        self.add_item(self.name_input)
        self.scheduler = scheduler
        self.registered_view = registered_view
        
    async def callback(self, interaction: discord.Interaction):
        steam_id = self.name_input.value
        discord_id = interaction.user.id
        add_user(discord_id, steam_id)
        self.scheduler.queue_command(Command(ct.REGISTER, discord_id, steam_id))
       # await interaction.response.send_message("Registered Successfully", ephemeral=True)
        await interaction.response.edit_message(content=f"Successfully Registered! It may take a few minutes until a score is Displayed!", view=self.registered_view)