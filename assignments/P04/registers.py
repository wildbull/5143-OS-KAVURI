from rich import print
from collections.abc import MutableMapping
from random import randint


class Register:
    """Represents a single `register` with a read and write method
    to change the registers values.
    """

    def __init__(self):
        """Constructor"""
        self.contents = -1 

    def write(self, x):
        """Change value of register"""
        self.contents = x

    def read(self):
        """Return value of register"""
        return self.contents

    def __str__(self):
        """Print out instance in readable format"""
        return f"[{self.contents}]"

    def __repr__(self):
        """Same as __str__"""
        return self.__str__()


class Registers(MutableMapping):
    """Represents a set of registers in an overloaded OOP fashion that
    allows for assignments to go like:

                r = Registers()
                r[0] = 44
                r[1] = 33
    """

    def __init__(self, num=2):
        """Constructor"""
        self.num = num
        self.registers = []
        for i in range(num):
            self.registers.append(Register())

    def __setitem__(self, k, v):
        """Assigns a value to a particular register as long as the key is
        integer, and within bounds.
        """
        if isinstance(k, int) and k < self.num:
            # setattr(self, self.registers[k], v)
            self.registers[k].write(v)

    def __getitem__(self, k):
        """Returns a value from a specific register indexed by `k`"""
        if isinstance(k, int) and k < self.num:
            # getattr(self, k)
            return self.registers[k].read()
        return None

    def __len__(self):
        """Len() of object instance. Must be here to overload class
        instance or python chokes.
        """
        return self.num

    def __delitem__(self, k):
        """Overloads the del keyword to delete something out of a
        list or dictionary.
        """
        if isinstance(k, int):
            self.registers[k] = None

    def __iter__(self):
        """Allows object iteration, or looping over this object"""
        yield self.registers

    def __str__(self):
        s = "[ "
        i = 0
        for r in self.registers:
            s += f"R{i}{str(r)} "
            i += 1
        return s + "]"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    reg = Registers(4)  # create 4 registers
    print(reg[1])
    for i in range(len(reg)):  # add random data to them
        reg[i] = randint(1, 100)
    
    print(reg[1])
    print(reg)  # print them out
