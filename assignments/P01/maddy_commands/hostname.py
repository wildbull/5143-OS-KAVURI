from utilities import *
import socket
flags = []
help = '''
hostanme ::  prints the name of the device 
'''
def func(**kwargs):
    """ Concatenate files and send to std out
    """
    command = ["cat"]
    flags = []
    params = []

    if "input" in kwargs:
        return
    if 'flags' in kwargs:
        flags = kwargs["flags"]

    if 'params' in kwargs:
        params = kwargs['params']
    
    return socket.gethostname()
