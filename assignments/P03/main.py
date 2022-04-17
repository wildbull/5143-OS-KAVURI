from asyncore import write
from datetime import datetime
from gettext import install
#from logging import Level
from multiprocessing import Lock
import sys
import getopt
from time import sleep
import threading
import json
from random import shuffle

import memory
import rwLock
#default number of writers
NUM_WRITERS = 5
NUM_INSTRUCTIONS_PER_FILE = 128
NUM_REGISTERS = 2
LOCK_ENTIRE_MEM = True

#GLOGAL LOCK
LOCK = rwLock.ReadWriteLock(withPromotion=True)
LOCK_A = rwLock.ReadWriteLock()
LOCK_B = rwLock.ReadWriteLock()
LOCK_C = rwLock.ReadWriteLock()


#reader threads
READER_THREADS = []
#writer threads
WRITER_THREADS = []
#output thread
OUTPUT_THREAD = None
#GLOBAL data
with open("memory.json") as fd:
    MEMORY = json.load(fd)

def generate_instruction_files():
    for i in range(NUM_WRITERS):
        instructions = []
        for j in range(NUM_INSTRUCTIONS_PER_FILE):
            instructions.append(memory.randInstruction())
        
        with open("Instructions_"+str(i)+".txt", "w") as fd:
            fd.write("\n".join(instructions))


def execute_instruction(instruction):
    registers = [0]*(NUM_REGISTERS + 1)
    result = 0
    for line in instruction:
        line = line.strip().split(" ")
        print(line)
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

def reader():
    while True:
        #acquire lock
        with rwLock.ReadRWLock(LOCK) as lock:
            #store the values in dummy variable
            sleep(0.5)
        
    pass

def writer(file_name):
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
        with rwLock.WriteRWLock(LOCK) as lock:
            execute_instruction(instruction)
            sleep(0.3)
            #run the instrutctions

def printer(lock):
    print("Number of readers up :: ", len(READER_THREADS))
    print("Number of writers up :: ", len(WRITER_THREADS))
    print("readers = " + str(lock._readers) + " , Writers = "+ str(lock._writers) )
    #print("readers = "+ "\n".join(lock._readerList))
    #print("readers = "+ "\n".join(lock._writerList))
    sleep(0.3)


def create_threads():
    num_readers = NUM_WRITERS * 5

    #create readers
    for i in range(num_readers):
        READER_THREADS.append(threading.Thread(target=reader))
    
    for i in range(NUM_WRITERS):
        WRITER_THREADS.append(threading.Thread(target=writer, args=("Instructions_"+str(i)+".txt",)))
    
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
        if LOCK_ENTIRE_MEM:
            printer(LOCK)
        else:
            printer(LOCK_A)
            printer(LOCK_B)
            printer(LOCK_C)


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
    printer_thread = threading.Thread(target=print_thread_handler)
    printer_thread.start()
    for tr in WRITER_THREADS:
        tr.join()
    end_time = datetime.now()
    #printer_thread.pause()

    print("time taken :: ", end_time - start_time)
    #writer("Instructions_4.txt")


    
    
             

