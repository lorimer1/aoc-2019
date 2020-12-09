from enum import IntEnum

class Opcode(IntEnum):
    """ mnemonic for each opcode number """
    ADD     = 1  # Addition
    MUL     = 2  # Multiplication
    IN      = 3  # Input
    OUT     = 4  # Output
    JNZ     = 5  # Jump if Not Zero
    JZ      = 6  # Jump if Zero
    LT      = 7  # Less Than
    EQ      = 8  # Equal
    RB      = 9  # Relative Base
    HALT    = 99 # Halt

class Operand(IntEnum):
    """ name for each operand index """
    One     = 0  # 1st operand
    Two     = 1  # 2nd operand
    Three   = 2  # 3rd operand

