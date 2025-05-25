from core.scheduler.command_type import command_type

class Command:
    type = command_type
    discord_id : str
    steam_id : str

    def __init__(self, command : command_type, discord_id : str, steam_id: str):
        self.type = command
        self.discord_id = discord_id
        self.steam_id = steam_id