import os

flags = []
help = '''
filter for paging through text one screenful at a time
######## contorls :: 
    h     :: print help
    b,B   :: move up one line
    np,NP :: next page
    bp,BP :: Previous Page
    e,E   :: end of file
    s,S   :: starting of file
    <Enter>/<Return> :: move down by a line

########
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
    
    cols,rows =  os.get_terminal_size()
    print("rows :: ", rows)
    #case where num lines is given
    if flags:
        num_lines = int(params[-1])
    else:
        #num lines is 10 by default
        num_lines = 10
   
    if "input" in kwargs:
        content = kwargs["input"].split("\n")
    else:
        if not params:
            return "less :: no file input provided"
        with open(params[0]) as fd:
            content = fd.readlines()

     
    total_lines = len(content)
    
    start = 0
    end = rows
    curr_command = "s"

    while curr_command!= 'q' and curr_command != "Q":
        #print("\n".join(content[start:end]))
        for i in content[start:end]:
            print(i)

        curr_command = input().strip()

        if curr_command == "h" or curr_command == "H":
            print(help)
            curr_command = input().strip()

        elif curr_command == "b" or curr_command == "B":
            if start > 0:
                start = start -1
                end = end -1

        elif curr_command == "bp" or curr_command == "BP":
            if start >= rows:
                start -= rows
                end -= rows

        elif curr_command == "np" or curr_command == "NP":
            if end < total_lines - rows :
                start += rows
                end += rows

        elif curr_command == "e" or curr_command == "E":
            start = total_lines - rows
            end = total_lines

        elif curr_command == "s" or curr_command == "S":
            start = 0
            end = rows

        else:
            if end<total_lines:
                start += 1
                end += 1


if __name__ == "__main__":
    func(params = ["test_file"])

