import os
import time
from os import stat

flags = []
help = '''
'''
make_4digits = lambda x: '0'*(4-len(x)) + x

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

    case = 0
    arr = [0,0,0]


    if not params:
        params = ["."]
    
    for flag in flags:
        if flag == "a":
            arr [0] = 1
        if flag == "h":
            arr[1] = 1
        if flag == "l":
            arr[2] = 1
    for i in range(len(arr)):
        case = case + arr[i]*(2**i)
    
    permissions = {
            0: "---",
            1: "--x",
            2: "-w-",
            3: "-wx",
            4: "r--",
            5: "r-x",
            6: "rw-",
            7: "rwx",
            8: "-",
            9: "d---"
            }

    string_2_return = ""

    now = int(time.time())
    recent = now - (4*30*24*60*60) #4 months ago
    for dir_path in params:
        for file_path in os.listdir(dir_path):
            file_path = os.path.join(dir_path , file_path)
            if case == 0: # ls
                try:
                    stat_info = os.lstat(file_path)
                except:
                    string_2_return += "\n" + "File/Dir not found :: "+file_path

                if not file_path.startswith("."):
                    if os.path.isdir(file_path):
                        string_2_return += "\n"+ file_path + "/"
                    else:
                        string_2_return += "\n"+ file_path
            elif case == 1: # ls -a
                try:
                    stat_info = os.stat(file_path)
                except:
                    string_2_return += "\n" + "File/Dir not found :: "+file_path
                
                if os.path.isdir(file_path):
                    string_2_return += "\n"+ file_path + "/"
                else:
                    string_2_return += "\n"+ file_path
                
            elif case == 3: # ls -ha
                stat_info = os.stat(file_path)
                if os.path.isdir(file_path):
                    size = stat_info.st_size
                    for unit in ["B", "MB", "KB", "GB"]:
                        if size < 1024.0:
                            h_size = make_4digits(str(size)[:4]) + unit
                            break
                    string_2_return += "\n"+ h_size + "     " + file_path + "/"
                else:
                    if not os.path.basename(file_path).startswith("."):
                        size = stat_info.st_size
                        for unit in ["B", "MB", "KB", "GB"]:
                            if size < 1024.0:
                                h_size = make_4digits(str(size)[:4]) + unit
                                break
                            else:
                                size /= 1024.0
                    string_2_return += "\n"+ h_size + "     " + file_path
                        
            elif case == 4: # ls -l
                stat_info = os.stat(file_path)
                octalPrem = oct(stat_info.st_mode)[-3:] # permissions
                octalPrem = int(octalPrem)
                octalP = octalPrem // 10
                owner = octalP //10
                GroupP = octalP % 10
                Others = octalPrem %10

                ts = stat_info.st_mtime
                time_m = stat_info.st_mtime
                if(ts < recent) or (ts > now):
                    time_fmt = "%b %e %Y"
                else:
                    time_fmt = "%b %e %R"
                    time_str = time.strftime(time_fmt, time.gmtime(ts))
                    time_str2 = time.strftime(time_fmt,time.gmtime(time_m))

                    name = stat(file_path).st_uid  # User id of the owner                    
                    try:
                        name = "%-3s" % os.getcwd(stat_info.st_uid)[0]
                    except:
                        name = "%-3s" % (stat_info.st_uid)
                    try:
                        group = "%-3s" % os.getegid(stat_info.st_gid) [0]
                    except:
                        group = "%-3s" % stat_info.st_gid


                    nlink = "%4d" % stat_info.st_nlink
                    total = len([name for name in os.listdir(dir_path) if os.path.isfile(file_path)])

                if not os.path.basename(file_path).startswith("."):
                    string_2_return += "\n" + permissions[Others] + permissions[GroupP] + permissions[owner] + " "
                    string_2_return += nlink + " "

                    size = "%8d" % stat_info.st_size
                    string_2_return += name + " "
                    string_2_return += group + " "
                    string_2_return += size + " "
                    string_2_return += time_str + "  "
                    if os.path.isdir(file_path):
                        string_2_return += file_path + "/"
                    else:
                        string_2_return += file_path


            else:
                stat_info = os.stat(file_path)
                octalPrem = oct(stat_info.st_mode)[-3:] # permissions
                octalPrem = int(octalPrem)
                octalP = octalPrem // 10
                owner = octalP //10
                GroupP = octalP % 10
                Others = octalPrem %10

                ts = stat_info.st_mtime
                time_m = stat_info.st_mtime
                if(ts < recent) or (ts > now):
                    time_fmt = "%b %e %Y"
                else:
                    time_fmt = "%b %e %R"
                    time_str = time.strftime(time_fmt, time.gmtime(ts))
                    time_str2 = time.strftime(time_fmt,time.gmtime(time_m))

                    name = stat(file_path).st_uid  # User id of the owner                    
                    try:
                        name = "%-3s" % os.getcwd(stat_info.st_uid)[0]
                    except:
                        name = "%-3s" % (stat_info.st_uid)
                    try:
                        group = "%-3s" % os.getegid(stat_info.st_gid) [0]
                    except:
                        group = "%-3s" % stat_info.st_gid


                    nlink = "%4d" % stat_info.st_nlink
                    total = len([name for name in os.listdir(dir_path) if os.path.isfile(file_path)])

                if not os.path.basename(file_path).startswith("."):
                    string_2_return += "\n" + permissions[Others] + permissions[GroupP] + permissions[owner] + " "
                    string_2_return += nlink + " "

                    size = "%8d" % stat_info.st_size
                    string_2_return += name + " "
                    string_2_return += group + " "
                    string_2_return += size + " "
                    string_2_return += time_str + "  "
                    if os.path.isdir(file_path):
                        string_2_return += file_path + "/"
                    else:
                        string_2_return += file_path


                try:
                    stat_info = os.lstat(file_path)
                except:
                    string_2_return += "\n" + "no such file or dir :: " + file_path
                    continue

                if not flags:
                    if os.path.isdir(file_path):
                        string_2_return += "\n"+ file_path + "/"
                    else:
                        string_2_return += "\n" + file_path


    return string_2_return

if __name__ == "__main__":
    print(func(params = [], flags = ["l","a","h"]))
    print(func(params = ["test_dir"], flags = ["l", "a", "h"]))

