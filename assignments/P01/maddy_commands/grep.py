
flags = ["l"]
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
    
    search_string = params [0]

    #TODO :: implement wild cards
    if "input" in kwargs:
        content = kwargs["input"].split("\n")
    else:
        with open(params[1]) as fd:
            content = fd.readlines()

    results = [ i.replace(search_string , '\033[34m' + search_string + '\033[0m') for i in content if search_string in i ]

    return "\n".join(results)

if __name__ == "__main__":
    print(func(params = [ "func" , "test_file"]))


