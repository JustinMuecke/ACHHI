import discord
from core.scheduler import Scheduler

from discord.ui import View
from database import get_steam_id
class TeamView(View):
    def __init__(self, scheduler : Scheduler, bot : discord.Bot, user_view : View):
        super().__init__()
        self.scheduler = scheduler
        self.bot = bot
        self.user_view = user_view
    
    @discord.ui.button(label="User Menu", style=discord.ButtonStyle.primary)
    async def team_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        steam_id = get_steam_id(interaction.user.id)
        await interaction.response.edit_message(content=f"Welcome back {steam_id}", view=self.user_view)

    
