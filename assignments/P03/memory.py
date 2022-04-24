from rich import print
import json
import random
from random import shuffle

from globals import *

# READ A205 R1
# READ B240 R2
# ADD R1 R2
# WRITE R1 A205
def randInstruction():

    choices = ["ADD", "SUB", "MUL", "DIV"]
    registers = ["R1", "R2"]
    memblocks = ["A", "B", "C"]
    memaddress = [x for x in range(100, 255, 5)]

    shuffle(choices)
    shuffle(registers)
    shuffle(memblocks)
    shuffle(memaddress)

    itype = choices[0]
    r1, r2 = registers[:2]
    #TODO :: memblock should be one not two
    mb1, mb2 = memblocks[:2]
    madd1, madd2 = memaddress[:2]
    
    if not LOCK_ENTIRE_MEM:
        mb2 = mb1
    
    inst = ""
    inst += f"READ {mb1}{madd1} {r1}\n"
    inst += f"READ {mb2}{madd2} {r2}\n"
    inst += f"{itype} {r1} {r2}\n"
    inst += f"WRITE {r1} {mb1}{madd1}\n"
    return inst

def randreadonlyInstruction():

    registers = ["R1", "R2"]
    memblocks = ["A", "B", "C"]
    memaddress = [x for x in range(100, 255, 5)]

    shuffle(registers)
    shuffle(memblocks)
    shuffle(memaddress)

    r1, r2 = registers[:2]
    mb1, mb2 = memblocks[:2]
    madd1, madd2 = memaddress[:2]
    
    if not LOCK_ENTIRE_MEM:
        mb2 = mb1
    
    inst = ""
    inst += f"READ {mb1}{madd1} {r1}\n"
    inst += f"READ {mb2}{madd2} {r2}\n"
    return inst


if __name__ == "__main__":

    mem = {}
    for section in range(3):
        section = str(chr(section + 65))
        mem[section] = {}
        for i in range(100, 255, 5):
            mem[section][i] = None

    with open("memory.json", "w") as f:
        json.dump(mem, f, indent=2)

    for i in range(10):
        print(randInstruction())
