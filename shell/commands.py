#!/usr/local/bin/python3
"""
This file gives and idea of how to parse commands from the command prompt and
the invoke the proper command function with parameters. 
The functions are examples only that call the built in commands, which is not
acceptable for your project. Again, this file is just an example of parsing a 
command and calling the correct function with params.
It may give you a little insight into organizing your shell code as well.
"""
import threading
import sys
from subprocess import call  # FOR DEMO PURPOSES ONLY!
from maddy_commands import Commands
from utilities import *


############### Decorator #############

def Command_parser(func):
    def inner():
        flags = []
        params = []
        pipes = []
        redirects = []

        if 'flags' in kwargs:
            flags = kwargs["flags"]

        if 'params' in kwargs:
            params = kwargs['params']
       
        if 'pipes' in kwargs:
            pipes = kwargs['pipe']

        if 'redirects' in kwargs:
            redirects = kwargs['redirects']

        func()

    return inner

class CommandHelper(object):
    def __init__(self):
        self.commands = {}
        self.cmd_files = []
        self.load_commands()

    ############ load context #############
    def load_commands(self):
        #read commands folder and fill commands_helper
        cmd_files = os.listdir("maddy_commands")
        #all python files in maddy_commands except Commands.py
        self.cmd_files = [ i for i in cmd_files if (i.endswith(".py") and i != "Commands.py")]

        for cmd_file in self.cmd_files:
            cmd_obj = Commands.Command(cmd_file)
            self.commands[cmd_obj.name] = cmd_obj

    def execute_command(self, **kwargs):
        if "raw_cmd" in kwargs:
            command = kwargs["raw_cmd"].split()
            cmd = command [0]
            if cmd[1].startswith("-"):
                flags = command[1]
                params = command [2:]
            else:
                params = command[1:]
        else:
            if 'cmd' in kwargs:
                cmd = kwargs['cmd']
            else:
                cmd = ''

            if 'params' in kwargs:
                params = kwargs['params']
            else:
                params = []

        if 'thread' in kwargs:
            thread = kwargs['thread']
        else:
            thread = False

        # One way to invoke using dictionary
        if not thread:
            print("running it is same thread")
            results = self.commands[cmd].func(params=params)
            print(results)
            #if not err == Error_codes.PROPER:
            #    print("ERROR : unable to execute command : Rerurn code - "+str(err))
        else:
            # Using a thread ****** broken right now *********
            if len(params) > 0:
                c = threading.Thread(target=self.commands[cmd], args=tuple(kwargs))
            else:
                c = threading.Thread(target=self.commands[cmd])

            c.start()
            c.join()
        
    def exists(self, cmd):
        print(self.commands)
        return cmd in self.commands


if __name__ == '__main__':

    ch = CommandHelper()

    while True:
        # get input from terminal (use input if raw_input doesn't work)
        command_input = input()

        #print(type(command_input))

        # remove command from params (very over simplified)
        command_input = command_input.split()

        # params are all but first position in list
        params = command_input[1:]

        # pull actual command from list
        cmd = command_input[0]

        

        # if command exists in our shell
        if ch.exists(cmd):
            ch.execute_command(cmd=cmd, params=params,thread=False)
        else:
            print("Error: command %s doesn't exist." % (cmd))


