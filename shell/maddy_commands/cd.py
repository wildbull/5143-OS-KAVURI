import os
from utilities import *
import globals

flags = []
help = '''
'''
def func(**kwargs):
    """ Concatenate files and send to std out
    """
    command = ["ls"]
    flags = []
    params = []

    if 'flags' in kwargs:
        flags = kwargs["flags"]

    if 'params' in kwargs:
        params = kwargs['params']

    if flags:
        if flags[0] == "~":
            os.chdir(os.path.expanduser("~"))

    elif params:
        dirPath = params[0]
        if len(params) ==1:
            if os.path.isdir(dirPath):
                os.chdir(dirPath)
                globals.dir_files_context = os.listdir(dirPath)
            else:
                print ("Path doesn't exist")
                return
        else:
            print("Pleae provide just one path!")
            return
    else:
        os.chdir(os.path.expanduser("~"))

