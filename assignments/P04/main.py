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
from readwritelock import RWLock
import orealy_lock
from globals import *

#GLOGAL LOCK
'''
LOCK = RWLock() 

#LOCK = rwLock.ReadWriteLock(withPromotion=True)
LOCK = rwLock.ReadWriteLock()
LOCK_A = rwLock.ReadWriteLock()
LOCK_B = rwLock.ReadWriteLock()
LOCK_C = rwLock.ReadWriteLock()
'''
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
        line = line.strip().split(" ")
        #print(line)
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
            sleep(0.5)
        sleep(0.5)
        

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
            if mem_block == "B":
                lock = LOCK_B
                #print("writer :: using LOCK_B")
            if mem_block == "C":
                lock = LOCK_C
                #print("writer :: using LOCK_C")

        with rwLock.WriteRWLock(lock) as lck:
            execute_instruction(instruction)
            #run the instrutctions
            sleep(0.2)
        sleep(0.3)

def printer(lock):
    print("Number of readers up :: ", len(READER_THREADS))
    print("Number of writers up :: ", len(WRITER_THREADS))
    #print("readers = " + str(lock.num_r) + " , Writers = "+ str(lock.num_w) )
    print("readers = " + str(lock._readers) + " , Writers = "+ str(lock._writers) )
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
        if stop_readers:
            break
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
    generate_instruction_files()
    start_time = datetime.now()
    create_threads()
    run_threads()
    printer_thread = threading.Thread(target=print_thread_handler)
    printer_thread.start()
    for tr in WRITER_THREADS:
        tr.join()
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


    
    
             

