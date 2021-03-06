from shutil import move
import os
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

    if "input" in kwargs:
        return
    if 'flags' in kwargs:
        flags = kwargs["flags"]

    if 'params' in kwargs:
        params = kwargs['params']

    try:
        if os.path.isdir(params[1]):
            params[1] = os.path.join(params[1], os.path.basename(params[0]))
        move(params[0],params[1])
    except IOError:
        return("unable to write to :: " + params[1])
    return ""

