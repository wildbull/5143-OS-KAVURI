import os
import globals
from utilities import *

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

    with open(globals.history_path) as fd:
        content = fd.readlines()
    
    for i in range(len(content)):
        content[i] = make_2digits(str(i+1)) + "    " + content[i]
    
    return "\n".join(content)
