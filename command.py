from command_type import command_type

class command:
    type = command_type
    entity : str

    def __init__(self, command, entity):
        self.type = command
        self.entity = entity