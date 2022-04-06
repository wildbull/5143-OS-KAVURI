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
        print("Please provide what to copy and where to write")
    
    source = params[0]
    dest = params [1]
    # Make sure the source file exists before doing anything
    if os.path.exists(source):
        if os.path.exists(dest):
            basepath = os.path.dirname(__file__)

            sourcepath = os.path.abspath(os.path.join(basepath, "..", source))
            destpath = os.path.abspath(os.path.join(basepath, "..", dest))
            if os.path.isdir(destpath):
                destpath = os.path.join(destpath,os.path.basename(sourcepath))

            shutil.copyfile(sourcepath, destpath)

        else:
            # Create the file for writing
            with open(dest, 'a') as f:
                pass

            basepath = os.path.dirname(__file__)

            sourcepath = os.path.abspath(os.path.join(basepath, "..", source))
            destpath = os.path.abspath(os.path.join(basepath, "..", dest))

            shutil.copyfile(source, dest)
        
        return ""

    else:
        print("Error: ", source, " does not exist.")



