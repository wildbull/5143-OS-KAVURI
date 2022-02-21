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
import globals

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

def redirect_func(file_path, content, mode):
    try:
        with open(file_path, mode) as fd:
            fd.write("\n"+content)
    except Exception as e:
        print("UNABLE to WRITE to the file as -----------------")
        print(e)
    return

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
            raw_command =  kwargs["raw_cmd"]#.encode("ascii", "ignore").decode()
            redirect = None
            redirect_type = ""
            pipes = []
            if (">" in raw_command):
                temp = raw_command.split(">") 
                redirect = temp[1].strip()
                raw_command =  temp[0].strip()
                redirect_type = "w"
            if (">>" in raw_command):
                temp = raw_command.split(">>") 
                redirect = temp[1].strip()
                raw_command =  temp[0].strip()
                redirect_type = "a"

            if "|" in raw_command:
                temp = raw_command.split("|")
                pipes = [pipe.strip() for pipe in temp [1:]]
                raw_command =  temp[0].strip()

            command = raw_command.strip().split()
            cmd = command [0].strip()
            flags = []
            params = []
            if len(command) > 1:
                if command[1].startswith("-"):
                    flags = list(command[1][1:])
                    if len(command) > 2:
                        params = command [2:]
                else:
                    params = command[1:]
            
            #Load commands dynamically
            if cmd == "ldcmds":
                self.load_commands()
                return

            if cmd.startswith("!"):
                try:
                    pos = int(cmd[1:])
                    print()
                    print(globals.history_obj.get_nth_in_history(pos))
                    return
                except:
                    print("\nWe could not understand the command")
                    return
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
        if cmd not in self.commands:
            #check if the command is man
            if cmd == "man":
                pass
            else:
                print("\nOops !!! we dont understand the command "+cmd)
                return
        if not thread:
            #print("running it is same thread")
            try:
                if cmd == "man":
                    results = self.commands[params[0]].help
                else:
                    results = self.commands[cmd].func(params=params, flags = flags)
            except Exception as e:
                results = e
                print("###############")
                print(self.commands[cmd].help)
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
        
        if not (pipes or redirect):
            print("  ")
            print(results)
            return

        if pipes:
            for pipe in pipes:
                pipe_content = pipe.split()
                pipe_cmd = pipe_content[0]
                pipe_flags = []
                pipe_params = []
                if len(pipe_content) > 1:
                    if pipe_content[1].startswith("-"):
                        pipe_flags = list(pipe_content[1])[1:]
                        if len(pipe_content) > 2:
                            pipe_params = pipe_content[2:]
                    else:
                        pipe_params = pipe_content[1:]

                
                if pipe_cmd not in self.commands:
                    print("Oops !!! we dont understand the command "+pipe_cmd)
                    return
                results = self.commands[pipe_cmd].func(params = pipe_params, input = results, flags = pipe_flags )
        if redirect:
            redirect_func(redirect, results, redirect_type)
            return
        
        print(" ")
        print(results)
        return

        
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


