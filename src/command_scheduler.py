from command import command
from command_type import command_type as ct
import typing
import os
from user import Hunter
import pickle

class scheduler: 

    command_queue : list[command]
    interrupt : bool

    def __init__(self):
        self.command_queue = []
        self.interrupt = False

    def queue_command(self, command : command):
        self.command_queue.append(command)
        print(f"New Command Queued: {command.type} {command.entity}")

    def run(self):
        print("Scheduler active")
        while(not self.interrupt):
            if(len(self.command_queue) == 0):
                continue
            command = self.command_queue.pop(0)
            command_type = command.type
            entity = command.entity
            print(f"Processing Command {command_type} {entity}")
            if(command_type is ct.REGISTER):
                if(entity in os.listdir("Hunters")):
                    continue
                _register_user(entity)
                print(f"Executed Command: {command_type} {entity}")
            if(command_type is ct.UPDATE):
                _update_user(entity)
                print(f"Execuded Command: {command_type} {entity}")


def _register_user(entity):
    hunter = Hunter(entity)
    file = open("Hunters/" + entity.lower() + ".hunt", "wb")
    pickle.dump(hunter, file)


### TODO Write more efficient update method
def _update_user(entity): 
    hunter = Hunter(entity)
    file = open("Hunters/" + entity.lower() + ".hunt", "wb")
    pickle.dump(hunter, file)

