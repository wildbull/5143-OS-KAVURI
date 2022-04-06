from utilities import *
flags = []
help = '''

concatenates files and writes them to STDOUT
usage:
    cat <file_1> <file_2> ....
 
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
    
    if "h" in flags:
        return("this Program takes in files and concatenates their contents to STDOUT", Error_codes.PROPER)

    if params:
        content = ""
        for file_path in params:
            try:
                with open(file_path) as fd:
                    content += fd.read()
            except Exception as e:
                print(e)

        return(content)

