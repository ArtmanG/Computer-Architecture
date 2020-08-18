"""
CPU functionality.
"""

import sys

HLT = 0b00000001 
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        # ram that holds 256 bytes (list of 0)
        self.ram = [0] * 256
        # 8 registers (list of 0)
        self.reg = [0] * 8
        # internal pc register = 0
        self.pc = 0
        # setup branch table
        self.running = True
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL


    # branch table methods
    def handle_HLT(self, *args):
        self.running = False

    def handle_LDI(self, op_a, op_b):
        self.reg[op_a] = op_b

    def handle_PRN(self, op_a, op_b):
        print(self.reg[op_a])

    def handle_MUL(self, op_a, op_b):
        self.alu('MUL', op_a, op_b)

    # end branch table methods

    def ram_read(self, MAR): # MAR = Memory address register
        # uses an address to read and returns the value stored at that address
        return self.ram[MAR]

    def ram_write(self, MAR, MDR): # MDR = Memory data register
        self.ram[MAR] = MDR


    def load(self, filename):
        """Load a program into memory."""

        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    line = line.split('#')
                    temp = line[0].strip()
                    if temp:
                        value = int(temp, 2)
                        self.ram[address] = value
                        address += 1
        
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
        

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while self.running:
            ir = self.ram_read(self.pc)

            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)

            add_to_pc = (ir >> 6) + 1

            self.branchtable[ir](op_a, op_b)

            self.pc += add_to_pc