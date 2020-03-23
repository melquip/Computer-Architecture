"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.canRun = False
        """
        Internal Registers
        """
        # PC: Program Counter, address of the currently executing instruction
        self.pc = 0
        # IR: Instruction Register, contains a copy of the currently executing instruction
        self.ir = 0
        # MAR: Memory Address Register, holds the memory address we're reading or writing
        self.mar = 0
        # MDR: Memory Data Register, holds the value to write or the value just read
        self.mdr = 0
        # FL: Flags
        self.fl = 0
        # ram
        self.ram = dict()
        """
        8 general-purpose 8-bit numeric registers R0-R7.
            R5 is reserved as the interrupt mask (IM)
            R6 is reserved as the interrupt status (IS)
            R7 is reserved as the stack pointer (SP)
        These registers only hold values between 0-255. 
        After performing math on registers in the emulator, bitwise-AND the result with 0xFF (255) 
        to keep the register values in that range.
        """
        self.reg = dict()

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

        self.canRun = True


    def alu(self, op, reg_a, reg_b):
        """
        ALU operations.

        ADD  10100000 00000aaa 00000bbb
        SUB  10100001 00000aaa 00000bbb
        MUL  10100010 00000aaa 00000bbb
        DIV  10100011 00000aaa 00000bbb
        MOD  10100100 00000aaa 00000bbb

        INC  01100101 00000rrr
        DEC  01100110 00000rrr

        CMP  10100111 00000aaa 00000bbb

        AND  10101000 00000aaa 00000bbb
        NOT  01101001 00000rrr
        OR   10101010 00000aaa 00000bbb
        XOR  10101011 00000aaa 00000bbb
        SHL  10101100 00000aaa 00000bbb
        SHR  10101101 00000aaa 00000bbb
        """
        print(f'ALU [{op}] -> {reg_a}, {reg_b}')
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "MOD":
            # self.reg[reg_a] ?? self.reg[reg_b]
            pass
        elif op == "INC":
            # self.reg[reg_a] ?? reg_b
            pass
        elif op == "DEC":
            # self.reg[reg_a] ?? reg_b
            pass
        elif op == "CMP":
            return self.reg[reg_a] == self.reg[reg_b]
        elif op == "AND":
            # self.reg[reg_a] ?? self.reg[reg_b]
            pass
        elif op == "NOT":
            # self.reg[reg_a] ?? self.reg[reg_b]
            pass
        elif op == "OR":
            # self.reg[reg_a] ?? self.reg[reg_b]
            pass
        elif op == "XOR":
            # self.reg[reg_a] ?? self.reg[reg_b]
            pass
        elif op == "SHL":
            # self.reg[reg_a] ?? self.reg[reg_b]
            pass
        elif op == "SHR":
            # self.reg[reg_a] ?? self.reg[reg_b]
            pass
        else:
            raise Exception("Unsupported ALU operation")

    def hlt(self):
        """HLT operation"""
        self.canRun = False
        return False

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
        """
        Run the CPU.

        The instruction pointed to by the PC is fetched from RAM, decoded, and executed.
        If the instruction does not set the PC itself, the PC is advanced to point to the subsequent instruction.
        If the CPU is not halted by a HLT instruction, go to step 1.
        """
        # self.trace()
        pcAlterCommands = ['CALL','INT','IRET','JMP','JNE','JEQ','JGT','JGE','JLT','JLE','RET']
        while self.canRun:
            instruction = self.ram_read(self.pc)
            print(f'instruction {instruction:b}')
            
            if instruction not in pcAlterCommands and not :
                # pc is advanced to subsequent instruction
                self.pc += 1
            elif instruction is 'HLT':
                self.hlt()

    def ram_read(self, address):
        return self.ram[address]
    def ram_write(self, address, value):
        self.ram[address] = value
        return self.ram[address]
