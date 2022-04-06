import os
from utilities import *
import shutil

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

    if not params:
        return("Please provide while file to open")
        

    os.system(" vim "+params[0] )

    return "done"
    
    


