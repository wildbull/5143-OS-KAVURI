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
import random
from uuid import RESERVED_FUTURE

import rwLock
import orealy_lock
from globals import *
import registers
import randInstructions
import cpu

#GLOGAL LOCK
LOCK = orealy_lock.ReadWriteLock()
PRIVILIGED_LOCK = orealy_lock.ReadWriteLock()
THREADS = []
OUTPUT_THREAD = None


#GLOBAL data
stop_readers = False

REGISTERS = registers.Registers(NUM_REGISTERS)
ALU = cpu.Alu(REGISTERS)

with open("memory.json") as fd:
    MEMORY = json.load(fd)

def generate_instruction_files():
    randInstructions.RandInstructions(privilegedRatio=0.05, sleepRatio=0.15, numProcesses=NUM_FILES)

def execute_instruction(instruction):
    result = 0
    for line in instruction:
        line = line.strip().split(" ")
        #print(line)
        if line[0] == "READ":
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
            MEMORY[(line[2].strip())[0]][int((line[2].strip())[1:])] = result
        if line[0] == "LOAD":
            print("Priviliged section update :: " , line)
            REGISTERS[int(line[2].strip()[1:])] = int(line[1])
        #if line[0] == "sleep":
        #    sleep()

def program(file_name):
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
            print("Priviliged instruction found")
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
                print(file_name + " :: waiting for priviliged sequence : " + str(priviliged_id-1) + " , current at : "+ str(REGISTERS[4]) + " last p :" + str(REGISTERS[3]))
                sleep(3)

        with rwLock.WriteRWLock(lock) as lck:
            execute_instruction(instruction)
            #run the instrutctions
            print(file_name + " :: done executing instruction")
            #sleep(0.2)
            sleep(random.randint(0,9)/10)
        sleep(random.randint(0,9)/10)

def printer(lock):
    #print("Number of threads :: ", len(THREADS))
    #print("readers = " + str(lock.num_r) + " , Writers = "+ str(lock.num_w) )
    print("readers = " + str(lock._readers) + " , Writers = "+ str(lock._writers) )
    sleep(0.3)

def create_threads():
    num_readers = NUM_FILES * 5
    for i in range(NUM_FILES):
        THREADS.append(threading.Thread(target=program, args=("program_"+str(i)+".exe",)))
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
    #printer_thread = threading.Thread(target=print_thread_handler)
    #printer_thread.start()
    for tr in THREADS:
        tr.join()
    #stop_readers = True
    #printer_thread.pause()

    mem_dump_file = "memory_after_run.json"
    with open( mem_dump_file ,"w") as fd:
        json.dump(MEMORY, fd, indent=4)

    #writer("Instructions_4.txt")


    
    
             

