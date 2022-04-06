import os
import sys
import getpass
import socket
from enum import Enum
from time import sleep

USER_INFO = "%s@%s::\033[2;37;40m maddy_sh\033[0;37;40m ::"%(getpass.getuser(),socket.gethostname())                      # set default prompt
def print_cmd(cmd):
    """ This function "cleans" off the command line, then prints
        whatever cmd that is passed to it to the bottom of the terminal.
    """
    padding = " " * 80
    sys.stdout.write("\r"+padding)
    sys.stdout.write("\r"+USER_INFO+cmd)
    sys.stdout.flush()

class Error_codes(Enum):
    PROPER = 0
    WRONG_PARAMS = 1
    ERROR = 2
    EXCEPTION = 3
    RESOURCE_LIMITATION = 4

make_2digits = lambda x: '0'*(2-len(x)) + x

