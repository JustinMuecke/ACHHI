from core.scheduler.command import Command
from core.scheduler.command_type import command_type as ct
import typing
import os
from core.user import Hunter
import pickle
from database.database import add_score

class Scheduler: 

    command_queue : list[Command]
    interrupt : bool

    def __init__(self):
        self.command_queue = []
        self.interrupt = False

    def queue_command(self, command : Command):
        self.command_queue.append(command)
        print(f"New Command Queued: {command.type} {command.steam_id}")

    def run(self):
        print("Scheduler active")
        while(not self.interrupt):
            if(len(self.command_queue) == 0):
                continue
            command = self.command_queue.pop(0)
            command_type = command.type

            discord_id = command.discord_id
            steam_id = command.steam_id
            print(f"Processing Command {command_type} {steam_id}")
            if(command_type is ct.REGISTER):
                _register_user(discord_id, steam_id)
                print(f"Executed Command: {command_type} {steam_id}")
            #if(command_type is ct.UPDATE):
            #    _update_user(entity)
            #    print(f"Execuded Command: {command_type} {entity}")


def _register_user(discord_id, steam_id):
    try:
        hunter = Hunter(steam_id)
        add_score(discord_id, hunter.score)
    except:
        add_score(discord_id, None)

### TODO Write more efficient update method
def _update_user(entity): 
    hunter = Hunter(entity)
    file = open("Hunters/" + entity.lower() + ".hunt", "wb")
    pickle.dump(hunter, file)

