from utilities import *


class Commands:
    def __init__(self):
        self.commands_dict = {} # key :: tool_name , value :: tool function implementation
        pass
    
    def execute_command(self, cmd):
        cmd =  cmd.split(" ")
        tool = cmd[0]
        redirect = []
        piping = []
        #NOTE :: we assume that the second entry in cmd are flags
        #TODO :: add logic to identify and handle redirections and piping
        if cmd[1].startswith("-"):
            flags = cmd[1]
            params = cmd[2:]
        else:
            flags = None
            params = cmd[1:]
        
        if tool in self.commands_dict:
            #execute 
            self.commands_dict[tool](flags, params)
        else:
            print("\nwe do not support the tool yet :: %s" %(tool,))
            return


def ls():
    print("ls invoked, dont worry")
