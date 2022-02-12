#!/usr/bin/env python3
"""
This file is about using getch to capture input and handle certain keys 
when the are pushed. The 'command_helper.py' was about parsing and calling functions.
This file is about capturing the user input so that you can mimic shell behavior.
I'll discuss more in class.
"""
import os
import sys
import getpass
import socket
from time import sleep

from utilities import *
import globals
from commands import CommandHelper 
from history import Maddy_History

##################################################################################
##################################################################################
class Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): 
        return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


############################## context building ##################################
getch = Getch()                             
history = Maddy_History()                   
commands = CommandHelper()

#for auto-completion
globals.dir_files_context = os.listdir()  #updated everytime cd command is run


##################################################################################



if __name__ == '__main__':
    cmd = ""                                # empty cmd variable
    cmd_after_cursor = ""

    print_cmd(cmd)                          # print to terminal
    
    while True:                             # loop forever
        char = getch()                      # read a character (but don't print)

        if char == '\x03' or cmd == 'exit': # ctrl-c
            del(history)
            raise SystemExit("\nBye.\n")
        
        elif char == '\x7f':                # back space pressed
            cmd = cmd[:-1]
            print_cmd(cmd)
            
        elif char in '\x1b':                # arrow key pressed
            null = getch()                  # waste a character
            direction = getch()             # grab the direction
            
            if direction in 'A':            # up arrow pressed
                # get the PREVIOUS command from your history (if there is one)
                # prints out 'up' then erases it (just to show something)
                #cmd += u"\u2191"
                cmd = history.prev_cmd(cmd)
                print_cmd(cmd)
                sleep(0.3)
                #cmd = cmd[:-1]
                
            if direction in 'B':            # down arrow pressed
                # get the NEXT command from history (if there is one)
                # prints out 'down' then erases it (just to show something)
                #cmd += u"\u2193"
                cmd = history.next_cmd()
                print_cmd(cmd)
                sleep(0.3)
                #cmd = cmd[:-1]
            
            if direction in 'C':            # right arrow pressed    
                # move the cursor to the right on your command prompt line
                # prints out 'right' then erases it (just to show something)
                cmd += u"\u2192"
                print_cmd(cmd)
                sleep(0.3)
                #cmd = cmd[:-1]

            if direction in 'D':            # left arrow pressed
                # moves the cursor to the left on your command prompt line
                # prints out 'left' then erases it (just to show something)
                cmd += u"\u2190"
                print_cmd(cmd)
                sleep(0.3)
                #cmd = cmd[:-1]
            
            print_cmd(cmd)                  # print the command (again)

        elif char in '\r':                  # return pressed 
            if cmd.strip():
                history.add(cmd)
            # This 'elif' simulates something "happening" after pressing return
            #cmd = "Executing command...."   #
            cmd = cmd.strip()
            if cmd:
                commands.execute_command(raw_cmd = cmd)
                '''
                try:
                    commands.execute_command(raw_cmd = cmd)
                    #print_cmd(cmd)                  
                    #sleep(1)    
                except Exception as e:
                    print("-------------------------")
                    print(e)
                    print("-------------------------")
                '''
                cmd = ""                        # reset command to nothing (since we just executed it)
            else:
                cmd = "  "

            print_cmd(cmd)                  # now print empty cmd prompt
        else:
            cmd += char                     # add typed character to our "cmd"
            print_cmd(cmd)                  # print the cmd out
