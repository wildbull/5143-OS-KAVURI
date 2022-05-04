import os
import sys
import json
import getopt
import threading
from time import sleep
from asyncore import write
from random import shuffle
from gettext import install
from datetime import datetime
from collections import deque
from multiprocessing import Lock

###########  local modules ################################
import memory
import rwLock
from readwritelock import RWLock
import orealy_lock
from globals import *

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

if not LOCK_ENTIRE_MEM:
    LOCK_A = orealy_lock.ReadWriteLock()
    LOCK_B = orealy_lock.ReadWriteLock()
    LOCK_C = orealy_lock.ReadWriteLock()


#reader threads
READER_THREADS = []
#writer threads
WRITER_THREADS = []
#output thread
OUTPUT_THREAD = None

#GLOBAL data
stop_readers = False


with open("memory.json") as fd:
    MEMORY = json.load(fd)

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
for i in range(NUM_WRITERS):
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
        if LOCK_ENTIRE_MEM:
            table = Table(title = "LOCK")
            table.add_column("Writers", justify="center", style="cyan", no_wrap=True)
            table.add_column("Readers", justify="center", style="green", no_wrap=True)
            table.add_row(str(LOCK._writers),str(LOCK._readers))
            return Panel(table)
        else:
            table_1 = Table(title = "LOCK_A")
            table_1.add_column("Writers", justify="center", style="cyan", no_wrap=True)
            table_1.add_column("Readers", justify="center", style="green", no_wrap=True)
            table_1.add_row(str(LOCK_A._writers),str(LOCK_A._readers))
           
            table_2 = Table(title = "LOCK_B")
            table_2.add_column("Writers", justify="center", style="cyan", no_wrap=True)
            table_2.add_column("Readers", justify="center", style="green", no_wrap=True)
            table_2.add_row(str(LOCK_B._writers),str(LOCK_B._readers))

            table_3 = Table(title = "LOCK_C")
            table_3.add_column("Writers", justify="center", style="cyan", no_wrap=True)
            table_3.add_column("Readers", justify="center", style="green", no_wrap=True)
            table_3.add_row(str(LOCK_C._writers),str(LOCK_C._readers))

            return Panel(Group(table_1, table_2, table_3))
        

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

def generate_instruction_files():
    for i in range(NUM_WRITERS):
        instructions = []
        for j in range(NUM_INSTRUCTIONS_PER_FILE):
            instructions.append(memory.randInstruction())
        
        with open("Instructions_"+str(i)+".txt", "w") as fd:
            fd.write("\n".join(instructions))
    
    for i in range(NUM_READERS):
        instructions = []
        for j in range(NUM_INSTRUCTIONS_PER_FILE):
            instructions.append(memory.randreadonlyInstruction())
        with open("Readonly_Instructions_"+str(i)+".txt", "w") as fd:
            fd.write("\n".join(instructions))
        


def execute_instruction(instruction):
    registers = [0]*(NUM_REGISTERS + 1)
    result = 0
    for line in instruction:
        add_log("processing : " + line)
        line = line.strip().split(" ")
        if line[0] == "READ":
           registers[int((line[-1].strip())[1:])] = MEMORY[line[1][0]][line[1][1:]]
        if line[0] in ["ADD", "SUB", "MUL", "DIV"]:
            if line[0] == "ADD":
                result = registers[int(line[1][1:])] + registers[int(line[2][1:])] 
            if line[0] == "MUL":
                result = registers[int(line[1][1:])] * registers[int(line[2][1:])] 
            if line[0] == "sub":
                result = registers[int(line[1][1:])] - registers[int(line[2][1:])] 
            if line[0] == "DIV":
                result = registers[int(line[1][1:])] / registers[int(line[2][1:])] 
        if line[0] == "WRITE":
            MEMORY[(line[2].strip())[0]][int((line[2].strip())[1:])] = result
    '''
    print("registers :: ", registers)
    print(result)
    print(MEMORY["A"]) 
    '''

def reader(file_name):
    content = []
    with open(file_name) as fd:
        fd.readlines()

    content = []
    with open(file_name) as fd:
        content = fd.readlines()
    idx_list = [idx+1 for idx, val in enumerate(content) if not val.strip()]
    size = len(content)
    instructions = [content[i: j] for i, j in
        zip([0] + idx_list, idx_list + 
        ([size] if idx_list[-1] != size else []))]



    for line in content:
        if not line.strip():
            continue
        line_content = line.split(" ")
        if stop_readers:
            break
        #acquire lock
        #with LOCK.r_locked():
        if LOCK_ENTIRE_MEM:
            lock = LOCK
        else:
            #figure out which lock
            mem_block = line_content[1][0] 
            if mem_block == "A":
                lock = LOCK_A
                #print("reader :: using LOCK_A")
            if mem_block == "B":
                lock = LOCK_B
                #print("reader :: using LOCK_B")
            if mem_block == "C":
                lock = LOCK_C
                #print("reader :: using LOCK_C")

        with rwLock.ReadRWLock(lock) as lck:
            #store the values in dummy variable
            execute_instruction([line])
            add_log("#################################")
            #sleep(0.7)
        sleep(0.3)
        

def writer(file_name, id):
    content = []
    with open(file_name) as fd:
        content = fd.readlines()
    idx_list = [idx+1 for idx, val in enumerate(content) if not val.strip()]
    size = len(content)
    instructions = [content[i: j] for i, j in
        zip([0] + idx_list, idx_list + 
        ([size] if idx_list[-1] != size else []))]

    #print(instructions[0])
    #print(instructions[-1])
    #execute_instruction(instructions[0])
    for instruction in instructions:
        #acquire lock
        #TODO add logic to identify memory location to use lock specific to the location
        #with LOCK.w_locked():
        if LOCK_ENTIRE_MEM:
            lock = LOCK
        else:
            #figure out which lock
            line_content = instruction[0].split(" ")
            mem_block = line_content[1][0] 
            if mem_block == "A":
                lock = LOCK_A
                #print("writer :: using LOCK_A")
                add_log(f"writer_{id} :: using LOCK_A")
            if mem_block == "B":
                lock = LOCK_B
                #print("writer :: using LOCK_B")
                add_log(f"writer_{id} :: using LOCK_B")
            if mem_block == "C":
                lock = LOCK_C
                add_log(f"writer_{id} :: using LOCK_C")

        with rwLock.WriteRWLock(lock) as lck:
            execute_instruction(instruction)
            #run the instrutctions
            sleep(0.2)
        update_progress(id)
        sleep(0.3)

def printer(lock):
    #print("Number of readers up :: ", len(READER_THREADS))
    #print("Number of writers up :: ", len(WRITER_THREADS))
    #print("readers = " + str(lock.num_r) + " , Writers = "+ str(lock.num_w) )
    add_log("readers = " + str(lock._readers) + " , Writers = "+ str(lock._writers) )
    '''
    print("readers = "+ "\n".join(map(str, lock._readerList)))
    print("writers = "+ "\n".join(map(str,lock._writerList)))
    '''
    sleep(0.3)

def create_threads():
    num_readers = NUM_WRITERS * 5

    #create readers
    for i in range(num_readers):
        READER_THREADS.append(threading.Thread(target=reader, args=("Readonly_Instructions_"+str(i)+".txt",)))
    
    for i in range(NUM_WRITERS):
        WRITER_THREADS.append(threading.Thread(target=writer, args=("Instructions_"+str(i)+".txt",i,)))
    
    #OUTPUT_THREAD = threading.Thread(target = printer)
    return

def run_threads():
    #start randomly using shuffle
    shuffle(READER_THREADS)
    shuffle(WRITER_THREADS)

    for k in WRITER_THREADS:
        k.start()
    for k in READER_THREADS:
        k.start()
    return 


def print_thread_handler():
    while True:
        if stop_readers:
            break
        if LOCK_ENTIRE_MEM:
            printer(LOCK)
        else:
            printer(LOCK_A)
            printer(LOCK_B)
            printer(LOCK_C)
        add_log("*****")
        sleep(0.3)


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
    start_time = datetime.now()
    create_threads()
    run_threads()
    #printer_thread = threading.Thread(target=print_thread_handler)
    #printer_thread = threading.Thread(target=visualisation_handler)
    #printer_thread.start()
    #for tr in WRITER_THREADS:
    #    tr.join()
    ##########
    with Live(layout, refresh_per_second=10, screen=True) as live:
        while not overall_progress.finished:
            #live.console.print("check this out")
            #add_log("check this out")
            sleep(0.5)
    ##########
    stop_readers = True
    end_time = datetime.now()
    #printer_thread.pause()

    print("time taken :: ", end_time - start_time)
    
    if LOCK_ENTIRE_MEM:  
        mem_dump_file = "memory_after_run_full_lock.json"
    else:
        mem_dump_file = "memory_after_run_section_lock.json"
    with open( mem_dump_file ,"w") as fd:
        json.dump(MEMORY, fd, indent=4)

    #writer("Instructions_4.txt")


    
    
             

