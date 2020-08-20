import sys

# the index into a memory array, AKA location, address, pointer

PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3  # store a value in a register
PRINT_REG = 4  # print the register value in decimal
PUSH = 5
POP = 6
CALL = 7
RET = 8

# think of a big array of bytes, 8-bits per byte
memory = [0] * 256

# registers[4] = 37
registers = [0] * 8

SP = 7
registers[SP] = 0xF4  # Stack pointer

# load the program file
address = 0

if len(sys.argv) != 2:
    print("usage: comp.py progname")
    sys.exit(1)

try:
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.strip()
            temp = line.split()
            if len(temp) == 0:
                continue
            if temp[0][0] == "#":
                continue
            try:
                memory[address] = int(temp[0])
            except ValueError:
                print(f"Invalid num: {temp[0]}")
                sys.exit(1)
            address += 1


except FileNotFoundError:
    print(f"Couldn't open {sys.argv[1]}")
    sys.exit(2)

if address == 0:
    print("Program was empty")
    sys.exit(3)
# print(memory[:10])

# sys.exit(0)

running = True

pc = 0  # program counter, the index into memory of the currently_executing instruction

while running:
    ir = memory[pc]  # instruction register

    if ir == PRINT_BEEJ:
        print("Beej!")
        pc += 1

    elif ir == HALT:
        running = False
        pc += 1

    elif ir == SAVE_REG:  # SAVE_REG
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        registers[reg_num] = value
        pc += 3  # increment by the # of operands

    elif ir == PRINT_REG:  # PRINT_REG
        reg_num = memory[pc + 1]
        print(registers[reg_num])
        pc += 2

    elif ir == PUSH:  # PUSH
        # decrement stack pointer
        registers[SP] -= 1

        # get val from register
        reg_num = memory[pc + 1]
        value = registers[reg_num]  # this is the value we want to push

        # store it on the stack
        top_of_stack_addr = registers[SP]
        memory[top_of_stack_addr] = value

        pc += 2

        print(f"stack: {memory[0xE4:0xF4]}")

    elif ir == POP:
        value_addr = registers[SP]
        value = memory[value_addr]
        reg_num = memory[pc + 1]
        registers[reg_num] = value
        registers[SP] += 1
        pc += 2

    elif ir == CALL:
        # push return address
        return_address = pc + 2
        registers[SP] -= 1
        memory[registers[SP]] = return_address

        # call subroutine
        reg_num = memory[pc + 1]
        pc = registers[reg_num]

    elif ir == RET:
        # pop return addr off the stack
        return_address = memory[registers[SP]]
        registers[SP] += 1

        # set the pc to it
        pc = return_address

    else:
        print(f"Invalid instruction {ir} at address {pc}")
        sys.exit(1)

    # This if tests to see if the instruction set the PC to some arbitrary place or not
    # like CALL and RET do

    # if ir & 0b00010000 == 0:
    #     pc += (ir >> 6) + 1

