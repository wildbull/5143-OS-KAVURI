from shutil import move
import os
from utilities import *

flags = ["r"]
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
    
    string_2_return = ""

    if flags:
        if flags[0] == '-r':
            shutil.rmtree(params[0])
            string_2_return += (params[0], "was deleted.\n")

    else:
        if not params:
            string_2_return += "Error: Please enter a file name after rm.\n"
        else:
            filename = params[0]
            basepath = os.getcwd()
            #NOTE :: only one * is allowed/supported in wild cards
            if "*" in filename:
                substrings = filename.split("*")
                if len(substrings) == 1:
                    if filename.startswith("*"):
                        substring = filename[1:]
                        for file in os.listdir(basepath):
                            if file.endswith(substring):
                                os.remove(os.path.join(basepath,file))
                                string_2_return += file + " :: is deleted\n" 
                    elif filename.endswith("*"):
                        substring = filename[:-1]
                        for file in os.listdir(basepath):
                            if file.startswith(substring):
                                os.remove(os.path.join(basepath,file))
                                string_2_return += file + " :: is deleted\n" 


            else:
                index = 0
                for p in params:
                    if os.path.exists(params[index]):
                        os.remove(params[index])
                    else:
                        string_2_return += params[index] + "  :: Error :: The file does not exist.\n"
                index += 1
    
    return string_2_return


