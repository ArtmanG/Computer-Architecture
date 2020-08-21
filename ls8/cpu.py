"""
CPU functionality.
"""

import sys

# Branchtable variables
# weeks work
HLT = 0b00000001 
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
# #sprint mvp
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
# sprint stretch
AND = 0b10101000
OR = 0b10101010
XOR = 0b10101011
NOT = 0b01101001
SHL = 0b10101100
SHR = 0b10101101
MOD = 0b10100100

class CPU:
    """Main CPU class."""

    def __init__(self):
        # ram that holds 256 bytes (list of 0)
        self.ram = [0] * 256
        # 8 registers (list of 0)
        self.reg = [0] * 8
        # reg7 resets/defaults to 0xF4
        self.reg[7] = 0XF0
        # internal pc register = 0
        self.pc = 0
        # setup branch table
        self.is_running = False
        # use pattern 00000LGE for FL register
        self.FL = 0b11000000
        # use R5 for interrupt mask, R6 for interrupt status
        self.IM = self.reg[5]
        self.IS = self.reg[6]
        # Start branch table setup 
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET

        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[JMP] = self.handle_JMP
        self.branchtable[JEQ] = self.handle_JEQ
        self.branchtable[JNE] = self.handle_JNE

        self.branchtable[AND] = self.handle_ADD
        self.branchtable[OR] = self.handle_OR
        self.branchtable[XOR] = self.handle_XOR
        self.branchtable[NOT] = self.handle_NOT
        self.branchtable[SHL] = self.handle_SHL
        self.branchtable[SHR] = self.handle_SHR
        self.branchtable[MOD] = self.handle_MOD
        # End branch table setup

    # branch table methods
    def handle_HLT(self, *args):
        self.is_running = False

    def handle_LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def handle_PRN(self, operand_a, operand_b):
        print(self.reg[operand_a])

    def handle_PUSH(self, operand, *args):
        val = self.reg[operand]
        self.reg[7] -= 1
        self.ram[self.reg[7]] = val

    def handle_POP(self, operand, *args):
        val = self.ram[self.reg[7]]
        self.reg[operand] = val
        self.reg[7] += 1

    def handle_CALL(self, operand_a, operand_b):
        addr = self.reg[operand_a]
        rtn_addr = self.pc + 2
        self.reg[7] -= 1  
        sp = self.reg[7]  
        self.ram[sp] = rtn_addr 
        self.pc = addr

    def handle_RET(self, *args):
        rtn_addr = self.ram[self.reg[7]]
        self.reg[7] += 1
        self.pc = rtn_addr
    
    def handle_JMP(self, operand, *args):
        self.pc = self.reg[operand]

    def handle_JEQ(self, operand, *args):
        if self.FL & 0b00000001:
            self.pc = self.reg[operand]
        else:
            self.pc += 2

    def handle_JNE(self, operand, *args):
        if not self.FL & 0b00000001:
            self.pc = self.reg[operand]
        else: 
            self.pc += 2
    # end branch table methods


    # start alu branch table methods
    def handle_MUL(self, operand_a, operand_b):
        self.alu('MUL', operand_a, operand_b)

    def handle_ADD(self, operand_a, operand_b):
        self.alu('ADD', operand_a, operand_b)

    def handle_AND(self, operand_a, operand_b):
        self.alu('AND', operand_a, operand_b)

    def handle_CMP(self, operand_a, operand_b):
        self.alu('CMP', operand_a, operand_b)

    def handle_MOD(self, operand_a, operand_b):
        self.alu('MOD', operand_a, operand_b)

    def handle_NOT(self, operand_a, operand_b):
        self.alu('NOT', operand_a, operand_b)

    def handle_OR(self, operand_a, operand_b):
        self.alu('OR', operand_a, operand_b)

    def handle_SHL(self, operand_a, operand_b):
        self.alu('SHL', operand_a, operand_b)
    
    def handle_SHR(self, operand_a, operand_b):
        self.alu('SHR', operand_a, operand_b)

    def handle_XOR(self, operand_a, operand_b):
        self.alu('XOR', operand_a, operand_b)
    # end alu branch table methods

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
                    comment_split = line.split('#')
                    n = comment_split[0].strip()
                    if n:
                        value = int(n,2)
                        self.ram[address] = value
                        address += 1
        
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
        
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.reg[reg_a] &= 0xFF

        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
            self.reg[reg_a] &= 0xFF

        elif op == 'AND':
            self.reg[reg_a] &= self.reg[reg_b]
            self.reg[reg_a] &= 0xFF

        elif op == 'CMP':
            self.FL = self.FL & 0b11111000

            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = self.FL | 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.FL = self.FL | 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.FL = self.FL | 0b00000100

        elif op == 'MOD':
            if self.reg[reg_b]: 
                self.reg[reg_a] %= self.reg[reg_b]

            else:
                self.handle_HLT()
                raise Exception("Cannot divide by 0")

        elif op == 'NOT':
            self.reg[reg_a] = self.reg[reg_a] ^ 0b11111111

        elif op == 'OR':
            self.reg[reg_a] |= self.reg[reg_b]

        elif op == 'SHL':
            self.reg[reg_a] = (self.reg[reg_a] << self.reg[reg_b])

        elif op == 'SHR':
            self.reg[reg_a] = (self.reg[reg_a] >> self.reg[reg_b])

        elif op == 'SUB':
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == 'XOR':
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]

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
        self.is_running = True

        while self.is_running:
            # read the memory address stored in PC and store it in IR(instruction register local to this method)
            ir = self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            add_to_pc = (ir >> 6) + 1

            self.branchtable[ir](operand_a, operand_b)

            jumps = [CALL, RET, JEQ, JMP, JNE]

            # if ir != CALL and ir != RET:
            #     self.pc += add_to_pc

            if ir not in jumps:
                self.pc += add_to_pc