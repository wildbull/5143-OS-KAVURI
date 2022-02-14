import os, sys, stat

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
        return help

    value = params[0]
    if value[0] == "u":
        if value[1] == "+":
            if value[2] == "r":
                os.chmod(params[1], stat.S_IREAD)
            if value[2] == "w":
                os.chmod(params[1], stat.IWRITE)
            if value[2] == "x":
                os.chmod(params[1], stat.IEXEC)
            if value[2] == "a":
                os.chmod(params[1], stat.S_IRWXU)
            else:
                return("in-proper input")
    if value[0] == "g":
        if value[1] == "+":
            if value[2] == "r":
                os.chmod(params[1], stat.S_IRGRP)
            if value[2] == "w":
                os.chmod(params[1], stat.IWGRP)
            if value[2] == "x":
                os.chmod(params[1], stat.IXGRP)
            if value[2] == "a":
                os.chmod(params[1], stat.S_IRWXG)
            else:
                return("in-proper input")
    if value[0] == "o":
        if value[1] == "+":
            if value[2] == "r":
                os.chmod(params[1], stat.S_IROTH)
            if value[2] == "w":
                os.chmod(params[1], stat.IWOTH)
            if value[2] == "x":
                os.chmod(params[1], stat.IXOTH)
            if value[2] == "a":
                os.chmod(params[1], stat.S_IRWXO)
            else:
                return("in-proper input")

    else:
        num = params[0].strip()
        num = int(num , 8)

        os.chmod(params[1],num)

        return 

if __name__=="__main__":
    func(params = ["555", "test.txt"])
