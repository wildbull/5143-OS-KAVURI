
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
    
    #TODO :: implement wild cards
    if "input" in kwargs:
        content = kwargs["input"].split("\n")
    else:
        content = []
        for file_path in params:
            with open(file_path) as fd:
                content += fd.readlines()


    content.sort()

    return "\n".join(content)

if __name__ == "__main__":
    print(func(params = ["test_file"]))


