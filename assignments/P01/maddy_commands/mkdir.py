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
        os.mkdir(params[0])
    except IOError:
        return ("unable to create :: " + params[0])
    return ""

