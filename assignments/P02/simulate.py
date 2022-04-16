# Import Module
from tkinter import *
from ttkthemes import ThemedTk
import json

from main import Pcb,JobStateQueue,ReadyQueue,WaitQueue
NewQueue = JobStateQueue()

'''
def load_data():
    data = []
    with open("datafile.dat") as f:
        lines = f.read().splitlines()
        for line in lines:
            data.append(Pcb(line))
    return data
'''

def load_data():
    pcb_objs = []
    with open("datafile.json") as fd:
        data = json.load(fd)
    for i in data:
        pcb_objs.append(Pcb(i))
    
    return pcb_objs

# create root window
root = ThemedTk(theme = "yaru")
 
# root window title and dimension
root.title("CPU Scheduling Simulator")
# Set geometry (widthxheight)
root.geometry('700x700')



fcfs_frame = Frame(root)
sjf_frame = Frame(root)
rr_frame = Frame(root)
pb_frame = Frame(root)

fcfs_frame.grid(row = 0, column = 0)
sjf_frame.grid(row = 0, column = 1 )
rr_frame.grid(row = 1, column = 0)
pb_frame.grid(row = 1, column = 1)

fcfs_label = Label(fcfs_frame, text = "FCFS scheduler").pack()
sjf_label = Label(sjf_frame, text = "SJF scheduler").pack()
rr_label = Label(rr_frame, text = "RR scheduler").pack()
pb_label = Label(pb_frame, text = "PB scheduler").pack()

if __name__ == "__main__":
    root.mainloop()
