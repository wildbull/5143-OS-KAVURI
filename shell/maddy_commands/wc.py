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
        print ("in if branch in wc")
        if not input_content:
            with open(params[0], "r") as f:
                file_content = f.read()
        else:
            file_content = input_content
        lines = len(file_content.split("\n"))
        chars = len(file_content)
        words = len(file_content.split(" "))

        srting_2_print = ""
        srting_2_print += "\nlines :: "+str(lines)
        srting_2_print += "\nwords :: "+str(words)
        srting_2_print += "\nchars :: "+str(chars)
        
        return srting_2_print
    else:
        print("flags found")

if __name__ == "__main__":
    print(func(params = ["cp.py"]))
    print(func(params = ["cp.py"], input = "hello world\nsilly felows"))

