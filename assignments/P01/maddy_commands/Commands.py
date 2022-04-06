import os

class Command:
    def __init__(self,cmd_path):
        self.cmd_path = os.path.abspath(cmd_path)
        self.name = os.path.basename(self.cmd_path)[:-3]
        self.help = ""
        self.func = None
        self.flags = []
        self.load_command()

    def load_command(self):
        package = "maddy_commands"
        cmd_module = getattr(__import__(package, fromlist=[self.name]), self.name)
        self.help = cmd_module.help
        self.func = cmd_module.func
        self.flags = cmd_module.flags
