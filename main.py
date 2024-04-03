# Simple Brainfuck interpreter written by justacoder


# BF INSTRUCTIONS:
#
# SYMBOL : MEANING
#    >   : Increment the data pointer by one
#    <   : Decrement the data pointer by one
#    +   : Increment the value at the data pointer by one
#    -   : Decrement the value at the data pointer by one
#    .   : Output the value at the data pointer (as an ASCII character)
#    ,   : Accept an input (as an ASCII decimal) and store it at the data pointer 
#    [   : If the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching ] command
#    ]   : If the byte at the data pointer is not zero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching [ command
#
# SPECIAL COMMANDS:
# 
# exit    : Exits the program
# reset   : Resets the data and the pointer
# data    : Shows the first few cells of the data. Amount can be configured below
DATA_PRINT_SIZE = 32 
# pointer : Shows the position of the pointer (starting at 0)


# MODES:
#
# Normal     : Execute one line of BF code and exit
# Continuous : Keep the program running and don't reset the data and pointer.
#              Good for debugging or playing around. Can be disabled below
CONTINUOUS_MODE = True

# DATA SIZE:
# The data array size is, usually, around 30000,
# although you probably don't need an array that big, but in case, you can configure it below.
DATA_SIZE = 128

# EXAMPLE CODE:
# 
# Hello World
# ++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
#
# Multiplication of two inputs (will print output as character, 
#        you can run "data" to see the result in cell #5 as an integer)
#
# ,>,[>>+<+<-]>>[<<+>>-]<<<[>[>>>+<<<-]>[<+>>+<-]>[<+>-]<<<-]>>>>.
#


#################################################################################
#################################################################################
#################################################################################


def reset():
    global data, pointer, inst_pointer
    data = [0] * DATA_SIZE; pointer = 0; inst_pointer = 0

code = ""; reset()

def find_match():
    c = code[inst_pointer]
    if c == "[":
        depth = 0
        i = inst_pointer
        while True:
            if (i >= len(code)): return len(code) - 1
            cc = code[i]
            if cc == "[": depth += 1
            if cc == "]": 
                depth -= 1
            if depth == 0: return i
            i += 1
    if c == "]":
        depth = 0
        i = inst_pointer
        while True:
            if (i < 0): return 0
            cc = code[i]
            if cc == "]": depth += 1
            if cc == "[": 
                depth -= 1
            if depth == 0: return i
            i -= 1

def run():
    global data, pointer, inst_pointer
    while True:
        if (inst_pointer >= len(code)): break

        c = code[inst_pointer]
        if not c in "><+-.,[]": inst_pointer += 1; continue
        
        if c == "<": pointer = max(pointer - 1, 0)
        if c == ">": pointer += 1
        if c == "+": data[pointer] += 1
        if c == "-": data[pointer] -= 1
        if c == ".": print(chr(data[pointer]), end=""); 
        if c == ",": data[pointer] = int(input("in (as int): "))
        if c == "[": 
            if data[pointer] == 0: inst_pointer = find_match()
        if c == "]": 
            if not data[pointer] == 0: inst_pointer = find_match()
        inst_pointer += 1

try:
    if CONTINUOUS_MODE: 
        while True:
            code = input("\nBF IN: ")
            if code == "exit": exit()
            if code == "reset": reset()
            if code == "pointer": print(pointer)
            if code == "data": print(data[:32])
            run(); inst_pointer = 0
    else:
        code = input("\nBF IN: "); run()
except KeyboardInterrupt: pass
