
flags = ["n"]
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
    
    #case where num lines is given
    if flags:
        num_lines = int(params[-1])
    else:
        #num lines is 10 by default
        num_lines = 10
   
    if "input" in kwargs:
        content = kwargs["input"].split("\n")
    else:
        with open(params[0]) as fd:
            content = fd.readlines()
    
    total_lines = len(content)
    string_2_return = "\n".join(content[total_lines-num_lines - 1:])

    return string_2_return

if __name__ == "__main__":
    print(func(params = ["test_file"]))


