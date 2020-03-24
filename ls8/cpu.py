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
        self.ir = [0] * 256
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
        self.reg = [0] * 8
        """
        Branchtable
        """
        self.branchtable = {}
        # OTHERS
        self.branchtable[0b00000001] = self.HLT
        self.branchtable[0b10000010] = self.LDI
        self.branchtable[0b01000111] = self.PRN
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
        # "ADD"
        self.branchtable[0b10100000] = lambda reg_a, reg_b: self.alu("ADD", reg_a, reg_b)
        # "SUB"
        self.branchtable[0b10100001] = lambda reg_a, reg_b: self.alu("SUB", reg_a, reg_b)
        # "MUL"
        self.branchtable[0b10100010] = lambda reg_a, reg_b: self.alu("MUL", reg_a, reg_b)
        # "DIV"
        self.branchtable[0b10100011] = lambda reg_a, reg_b: self.alu("DIV", reg_a, reg_b)
        # "MOD"
        self.branchtable[0b10100100] = lambda reg_a, reg_b: self.alu("MOD", reg_a, reg_b)
        # "INC"
        self.branchtable[0b01100101] = lambda reg_a: self.alu("INC", reg_a)
        # "DEC"
        self.branchtable[0b01100110] = lambda reg_a: self.alu("DEC", reg_a)
        # "CMP"
        self.branchtable[0b10100111] = lambda reg_a, reg_b: self.alu("CMP", reg_a, reg_b)
        # "AND"
        self.branchtable[0b10101000] = lambda reg_a, reg_b: self.alu("AND", reg_a, reg_b)
        # "NOT"
        self.branchtable[0b01101001] = lambda reg_a: self.alu("NOT", reg_a)
        # "OR"
        self.branchtable[0b10101010] = lambda reg_a, reg_b: self.alu("OR", reg_a, reg_b)
        # "XOR"
        self.branchtable[0b10101011] = lambda reg_a, reg_b: self.alu("XOR", reg_a, reg_b)
        # "SHL"
        self.branchtable[0b10101100] = lambda reg_a, reg_b: self.alu("SHL", reg_a, reg_b)
        # "SHR"
        self.branchtable[0b10101101] = lambda reg_a, reg_b: self.alu("SHR", reg_a, reg_b)

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename, 'r') as file:
                allLines = file.readlines()
                for i in range(0, len(allLines)):
                    line = allLines[i].replace('\n','').strip()
                    if '#' in allLines[i]:
                        line = allLines[i].split('#')[0].strip()
                    if len(line) > 0:
                        self.ram[address] = int(line, 2)
                        address += 1
            self.canRun = True
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b = 0):
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b] # "ADD"
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b] # "SUB"
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b] # "MUL"
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b] # "DIV"
        elif op == "MOD":
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b] # "MOD"
        elif op == "INC":
            self.reg[reg_a] += 1 # "INC"
        elif op == "DEC":
            self.reg[reg_a] -= 1 # "DEC"
        elif op == "CMP":
            self.reg[reg_a] == self.reg[reg_b] # "CMP"
        elif op == "AND":
            self.reg[reg_a] = self.reg[reg_a] and self.reg[reg_b] # "AND"
        elif op == "NOT":
            self.reg[reg_a] = not self.reg[reg_a] # "NOT"
        elif op == "OR":
            self.reg[reg_a] = self.reg[reg_a] or self.reg[reg_b] # "OR"
        elif op == "XOR":
            pass
        elif op == "SHL":
            pass
        elif op == "SHR":
            pass
        else:
            raise Exception("Unsupported ALU operation")

    def getOperation(self, identifier):
        if identifier in self.branchtable:
            return self.branchtable[identifier]
        raise Exception("Unsupported operation")
    
    def HLT(self):
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
        # pcAlterCommands = ['CALL','INT','IRET','JMP','JNE','JEQ','JGT','JGE','JLT','JLE','RET']
        while self.canRun:
            # get instruction
            instruction = self.ram_read(self.pc)
            # save it in instruction register
            self.ir[self.pc] = instruction
            # get operation name
            operation = self.getOperation(instruction)
            print(f'run {instruction:08b} -> pc {self.pc}')
            # decode instruction
            instruct = "{0:8b}".format(instruction)
            # operands = int(instruct[:2].strip() or '00', 2)
            operands = instruction >> 6
            # alu = int(instruct[2].strip() or '0', 2)
            alu = instruction >> 5 & 0b001
            # setPC = int(instruct[3].strip() or '0', 2)
            setPC = instruction >> 4 & 0b0001
            
            # identifier = int(instruct[4:].strip() or '0000', 2)

            """
            print(
                f'\n\nram_read {int(instruct,2):08b}', 
                f'\noperands {operands:02b}', 
                f'ALU? {alu:01b}', 
                f'sets PC? {setPC:01b}', 
                #f'identifier {identifier:04b}'
            )
            """

            # get param 1
            instruct_a = self.ram_read(self.pc + 1)
            # get param 2
            instruct_b = self.ram_read(self.pc + 2)

            if operands == 1:
                operation(instruct_a)
            elif operands == 2:
                operation(instruct_a, instruct_b)
            else:
                operation()
            
            #if setPC is not 0b1:
                # pc is advanced to subsequent instruction
            #print('self.pc +=', int(operands), self.pc + int(operands))
            self.pc += int(operands) + 1

    def ram_read(self, mar):
        """
        Meanings of the bits in the first byte of each instruction: AABCDDDD
        AA Number of operands for this opcode, 0-2
        B 1 if this is an ALU operation
        C 1 if this instruction sets the PC
        DDDD Instruction identifier
        The number of operands AA is useful to know because 
        the total number of bytes in any instruction is the number of operands + 1 (for the opcode). 
        This allows you to know how far to advance the PC with each instruction.
        """
        if mar in self.ram:
            return self.ram[mar]
        return None

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
        return self.ram[mar]

    def LDI(self, register, value):
        """
        LDI register immediate
        Set the value of a register to an integer.
        Machine code:
            10000010 00000rrr iiiiiiii
            82 0r ii
        """
        self.reg[int(register)] = value
        return self.reg[int(register)]

    def PRN(self, register):
        """
        PRN register pseudo-instruction
        Print numeric value stored in the given register.
        Print to the console the decimal integer value that is stored in the given register.
        Machine code:
            01000111 00000rrr
            47 0r
        """
        numericValue = int(self.reg[int(register)])
        print(numericValue)
        return numericValue