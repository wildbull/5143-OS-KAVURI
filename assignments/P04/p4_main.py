import os
import sys
import json
import random
import getopt
import threading
from time import sleep
from random import shuffle
from asyncore import write
from gettext import install
from datetime import datetime
from collections import deque
from multiprocessing import Lock
from uuid import RESERVED_FUTURE

###########  local modules ################################
import rwLock
import orealy_lock
from globals import *
import registers
import randInstructions
import cpu

############## Visualisation imports ######################
from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
###########################################################

#GLOGAL LOCK
LOCK = orealy_lock.ReadWriteLock()
PRIVILIGED_LOCK = orealy_lock.ReadWriteLock()
THREADS = []
OUTPUT_THREAD = None


#GLOBAL data
stop_readers = False

REGISTERS = registers.Registers(NUM_REGISTERS)
ALU = cpu.Alu(REGISTERS)

###########################################################
#               visualisation Utilities                   #
console = Console()
live    = None
def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=7),
    )
    layout["main"].split_row(
        Layout(name="side", ratio = 1),
        Layout(name="body", ratio=2, minimum_size=60),
    )
    #layout["side"].split(Layout(name="box1"), Layout(name="box2"))
    return layout

class Header:
    """Display header with clock."""
    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]Reader Writer[/b] - 1 ",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white on blue")

width , height = os.get_terminal_size()
live_logs = deque(maxlen=int(height/2)-4)

live_logs_table = Table(expand = True, show_footer = True)



def generate_table(rows):
    layout = Layout()
    console = Console()

    table = Table(expand = True)
    rows = list(rows)

    # This would also get the height:
    # render_map = layout.render(console, console.options)
    # render_map[layout].region.height
    n_rows = (os.get_terminal_size()[1])/2 -4

    while n_rows >= 0:
        for row in rows:
            table.add_row(row)

        layout.update(table)

        render_map = layout.render(console, console.options)

        if len(render_map[layout].render[-1]) > 2:
            # The table is overflowing
            n_rows -= 1
        else:
            break

    return table

     

def print_live_logs():
    live_logs_table.add_column(style="green", justify="left")
    add_log("###############")
    message_panel = Panel(
        live_logs_table
    )
    
    return message_panel

job_progress = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
)
for i in range(NUM_FILES):
    job_progress.add_task("[green]Writer_"+str(i), total = NUM_INSTRUCTIONS_PER_FILE)

total = sum(task.total for task in job_progress.tasks)
overall_progress = Progress()
overall_task = overall_progress.add_task("All Jobs", total=int(total))

progress_table = Table.grid(expand=True)
progress_table.add_row(
    Panel(
        overall_progress,
        title="Overall Progress",
        border_style="green",
        padding=(2, 2),
    ),
    Panel(job_progress, title="[b]Jobs", border_style="red", padding=(1, 2)),
)

class Counts:
    """Renders the time in the center of the screen."""
    def __init__(self):
        #self.name = name
        pass

    def build_table(self):
        #table = Table(title = self.name)
            table_1 = Table(title = "LOCK")
            table_1.add_column("Writers", justify="center", style="cyan", no_wrap=True)
            table_1.add_column("Readers", justify="center", style="green", no_wrap=True)
            table_1.add_row(str(LOCK._writers),str(LOCK._readers))
           
            table_2 = Table(title = "PRITVILIGED_LOCK")
            table_2.add_column("Writers", justify="center", style="cyan", no_wrap=True)
            table_2.add_column("Readers", justify="center", style="green", no_wrap=True)
            table_2.add_row(str(PRIVILIGED_LOCK._writers),str(PRIVILIGED_LOCK._readers))

            return Panel(Group(table_1, table_2))
        

    def __rich__(self) -> Panel:
        return self.build_table()

locks_stats = Counts()

#body_table = print_live_logs()
body_table = generate_table(live_logs)
layout = make_layout()
layout["header"].update(Header())
layout["side"].update(locks_stats)
layout["body"].update(body_table)
#layout["box2"].update(Panel(make_syntax(), border_style="green"))
#layout["box1"].update(Panel(layout.tree, border_style="red"))
layout["footer"].update(progress_table)

#console.print(layout)
from rich.live import Live
from time import sleep

def visualisation_handler():
    with Live(layout, refresh_per_second=10, screen=True):
        while not overall_progress.finished:
            console.print("check this out")
            sleep(0.5)
    
def update_progress(job_id):
    job_progress.advance(job_progress.tasks[job_id].id)
    completed = sum(task.completed for task in job_progress.tasks)
    overall_progress.update(overall_task, completed=completed)


def add_log(msg):
    live_logs.append(msg)
    layout["body"].update(generate_table(live_logs))

###########################################################


with open("memory.json") as fd:
    MEMORY = json.load(fd)

def generate_instruction_files():
    randInstructions.RandInstructions(privilegedRatio=0.05, sleepRatio=0.15, numProcesses=NUM_FILES)

def execute_instruction(instruction, lock):
    result = 0
    for line in instruction:
        line = line.strip().split(" ")
        #print(line)
        if line[0] == "READ":
            with rwLock.ReadRWLock(lock) as lck:
                sleep(0.5)
                REGISTERS[int((line[-1].strip())[1:])] = MEMORY[line[1][0]][line[1][1:]]
        if line[0] in ["ADD", "SUB", "MUL", "DIV"]:
            if line[0] == "ADD":
                result = REGISTERS[int(line[1][1:])] + REGISTERS[int(line[2][1:])] 
            if line[0] == "MUL":
                result = REGISTERS[int(line[1][1:])] * REGISTERS[int(line[2][1:])] 
            if line[0] == "sub":
                result = REGISTERS[int(line[1][1:])] - REGISTERS[int(line[2][1:])] 
            if line[0] == "DIV":
                result = REGISTERS[int(line[1][1:])] / REGISTERS[int(line[2][1:])] 
        if line[0] == "WRITE":
            with rwLock.WriteRWLock(lock) as lck:
                sleep(0.5)
                MEMORY[(line[2].strip())[0]][int((line[2].strip())[1:])] = result
        if line[0] == "LOAD":
            with rwLock.WriteRWLock(lock) as lck:
                sleep(0.5)
                print("Priviliged section update :: " , line)
                REGISTERS[int(line[2].strip()[1:])] = int(line[1])
        if line[0] == "sleep":
            sleep(random.randint(0,9)/10)

def program(file_name, id):
    instructions = None
    with open(file_name) as fd:
        instructions = json.load(fd)
    
    #print(instructions[0])
    #execute_instruction(instructions[0])
    for instruction in instructions:
        is_priviliged = False
        if "LOAD" in json.dumps(instruction):
            is_priviliged = True
        #acquire lock
        if is_priviliged:
            add_log("Priviliged instruction found")
            lock = PRIVILIGED_LOCK
        else:
            lock = LOCK
        
        #if priviliged,
        #wait till the register 4 is set with previous previligied instruction
        if is_priviliged:
            line_2_consider = None
            for line in instruction:
                if line.startswith("LOAD") and line.endswith("R4"):
                    line_2_consider = line
                    break
            priviliged_id = int(line_2_consider.split(" ")[1])
            #sleep till all priviliged sections before this are completed
            #while REGISTERS[4] != (priviliged_id - 1) :
            while True:
                if REGISTERS[4] == (priviliged_id -1):
                    break
                add_log(file_name + " :: waiting for priviliged sequence : " + str(priviliged_id-1) + " , current at : "+ str(REGISTERS[4]) + " last p :" + str(REGISTERS[3]))
                sleep(3)

        execute_instruction(instruction, lock)
        #run the instrutctions
        add_log(file_name + " :: done executing instruction")
        #sleep(0.2)
        #sleep(random.randint(0,9)/10)
        update_progress(id)
        sleep(random.randint(0,9)/10)

def printer(lock):
    #print("Number of threads :: ", len(THREADS))
    #print("readers = " + str(lock.num_r) + " , Writers = "+ str(lock.num_w) )
    add_log("readers = " + str(lock._readers) + " , Writers = "+ str(lock._writers) )
    sleep(0.3)

def create_threads():
    num_readers = NUM_FILES * 5
    for i in range(NUM_FILES):
        THREADS.append(threading.Thread(target=program, args=("program_"+str(i)+".exe",i,)))
    return

def run_threads():
    #start randomly using shuffle
    shuffle(THREADS)
    for k in THREADS:
        k.start()
        sleep(random.randint(0,5)/10)
    return 


def print_thread_handler():
    while True:
        if stop_readers:
            break
        printer(LOCK)
        printer(PRIVILIGED_LOCK)
        add_log("*****")


if __name__ == "__main__":
    try:
        opts, orgs = getopt.getopt(sys.argv[1:], "-w:f", ["writers","full_lock"]) 
    except getopt.GetoptError as err:
        print(err)
        exit()
    
    for i, o in opts:
        if i == "-w" or i == "--writers":
            NUM_WRITERS = int(o.strip())
        if i == "-f" or i == "--full_lock":
            LOCK_ENTIRE_MEM = False
    
    #TODO :: collect start and end time here
    #generate_instruction_files()
    create_threads()
    run_threads()
    printer_thread = threading.Thread(target=print_thread_handler)
    printer_thread.start()
    #for tr in THREADS:
    #    tr.join()
    #stop_readers = True
    #printer_thread.pause()
    ##########
    with Live(layout, refresh_per_second=10, screen=True) as live:
        while not overall_progress.finished:
            #live.console.print("check this out")
            #add_log("check this out")
            sleep(0.5)
    ##########
    stop_readers = True

    mem_dump_file = "memory_after_run.json"
    with open( mem_dump_file ,"w") as fd:
        json.dump(MEMORY, fd, indent=4)

    #writer("Instructions_4.txt")


    
    
             

