import os

flags = ["l","w", "c"]
help = '''
'''
def func(**kwargs):
    """ Concatenate files and send to std out
    """
    command = ["ls"]
    flags = []
    params = []
    input_content = ""
    if 'flags' in kwargs:
        flags = kwargs["flags"]

    if 'params' in kwargs:
        params = kwargs['params']
    
    if "input" in kwargs:
        input_content = kwargs['input']
    # If no flags were passed in, do all three
    if not flags:
        flags = ["l","w", "c"]
    
    if not input_content:
        with open(params[0], "r") as f:
            file_content = f.read()
    else:
        file_content = input_content
    lines = 0
    chars = 0
    words = 0
    
    srting_2_print = ""
    
    if "l" in flags: 
        lines = len(file_content.split("\n"))
        srting_2_print += "\nlines :: "+str(lines)
    if "c" in flags:
        chars = len(file_content)
        srting_2_print += "\nchars :: "+str(chars)
    if "w" in flags:
        words = len(file_content.split(" "))
        srting_2_print += "\nwords :: "+str(words)
    
    return srting_2_print

if __name__ == "__main__":
    print(func(params = ["cp.py"]))
    print(func(params = ["cp.py"], input = "hello world\nsilly felows"))
    print(func(params = ["cp.py"], flags = ["l","c"]))

