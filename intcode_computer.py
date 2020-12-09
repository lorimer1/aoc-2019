from collections import defaultdict, deque
from custom_events import Event
from custom_enums import Opcode, Operand
from custom_exceptions import IntCodeComputerEventHandlerException, IntCodeComputerInputQueueException, IntCodeComputerOpCodeException

class IntCodeComputer:
    
    # Valid opcodes for testing instructions against
    valid_opcodes = set(item.value for item in Opcode)

    # Each opcode has a size in memory i.e. the opcode and it's operands
    # e.g. ADD op1, op2, op3 ... uses 4 memory locations (size=4) 
    # Created as class variable (instead of instance variable) as remains the same no matter what instance is created
    op_sizes = { 
        Opcode.ADD  :   4,  # opcode, operand1, operand2, operand3
        Opcode.MUL  :   4,  # opcode, operand1, operand2, operand3
        Opcode.IN   :   2,  # opcode, operand1
        Opcode.OUT  :   2,  # opcode, operand1
        Opcode.JNZ  :   3,  # opcode, operand1, operand2
        Opcode.JZ   :   3,  # opcode, operand1, operand2
        Opcode.LT   :   4,  # opcode, operand1, operand2, operand3
        Opcode.EQ   :   4,  # opcode, operand1, operand2, operand3
        Opcode.RB   :   2,  # opcode, operand1
        Opcode.HALT :   1,  # opcode
    }
 
    # If stream is given, then load it as a program 
    def __init__(self, stream, is_enable_events=False):
        self.prog = list(map(int, stream.split(',')))
        self.reset()
        self.input_event  = Event() # allows for input events to be handled external to the class
        self.output_event = Event() # allows for output events to be handled external to the class
        self.is_events_enabled = is_enable_events # set to true when wanting to use with events

    # Copy the program into memory. Using a defaultdict for memory because the IntCode computer needs to be addressable
    # beyond the program size (defaultdict is ideal for this as it returns values for keys not explicityly set)
    def reset(self):
        self.memory = defaultdict(int, enumerate(self.prog)) # read program into memory
        self.ip = 0 # instruction pointer
        self.base = 0 # relative base
        self.input_queue = deque() # used to allow input to be received in bulk via the run() function
        self.input = None
        self.output = None
        self.opcode = None

    def run(self, input=None):
        if input:
            self.input_queue.append(input)
        instruction = self.memory[self.ip] # obtain the instruction in memory at index pointed to by the curent instruction pointer value
        self.opcode = instruction % 100 # opcode is right-most two digits of the instruction
        
        while self.opcode!=Opcode.HALT: # do until a halt opcode is read

            # only accept valid opcodes
            if self.opcode not in type(self).valid_opcodes: raise IntCodeComputerOpCodeException("Invalid OpCode " + str(self.opcode)) 

            # size is the number of memory addresses used by this instruction i.e opcode and its operands
            # use of type(self) to access class variable (rather than 'self' for instance variable)
            size = type(self).op_sizes[self.opcode] 

            # create list of operands for this instruction. Operands are in postions ip+1 through to ip+(size-1) 
            operands = [self.memory[self.ip+pos] for pos in range(1, size)]

            # modes are in the 100's, 1,000's and 10,000's digits of the instruction code for operands 1, 2, and 3 respectively i.e.
            # 100's digit (pos=2) is operand 1 mode, 1000's digit (pos=3) is operand 2 mode, 10,000's digit (pos=4) is operand 3 mode. 
            # if a mode digit is missing, it's mode is 0.
            # The approach taken here is similar to bit shifting and masking when working in binary i.e. in binary, divide by 2 to shift all bits to the right.
            # This can be done in decimal using base 10 rather than base 2. Masking for the right-most base 10 digit can be done using modulus 10.
            # Process: integer divide (//) the instruction by each digit power 10 to shift all digits right (each divide by 10 shifts all digits right by one place).
            # Truncate the fractional part of the result (// does this at the same time as dividing). Thus the mode digits are progressively shifted right.
            # Doing a modulus 10 after each shift 'masks' off the right most digit.
            modes = [(instruction // (10 ** power)) % 10 for power in range(2, 5)] # create list of operand modes ... index is operand position.

            # Addresses are determined by applying the modes to the operands i.e. mode=0 is direct, mode=1 is immediate, mode=2 is relative.
            # For mode=0 (direct) the operand is the address,
            # For mode=1 (immediate) there is no address, 
            # For mode=2 (relative) the address is relative to the current base value.
            # Process: Iterate the operands and modes and apply the operand formula for each respective mode ... produces a list of addresses implied by the operands    
            addresses = [(operand if operand >= 0 else None, None, (self.base + operand)  if (self.base + operand) >= 0 else None)[mode] \
                    for operand, mode in zip(operands, modes)]

            # Values are determined by applying the modes to the operands i.e. mode=0 is direct, mode=1 is immediate, mode=2 is relative.
            # For mode=0 (direct) the operand is the address in memory that contains the value
            # For mode=1 (immediate) the operand is the value
            # For mode=2 (relative) the operand is added to the current base value to obtain the address of the memory that contains the value
            # Process: Iterate the operands and modes and apply the operand formula for each respective mode ... produces a list of values implied by the operands 
            # Use 'if ... >= 0 else None' to ensure negative memory addresses are not accessed
            values = [( self.memory[operand] if operand >= 0 else None, operand, self.memory[self.base + operand] if (self.base + operand) >= 0 else None )[mode] \
                    for operand, mode in zip(operands, modes)]

            # Move instruction pointer to next instruction. Note that instruction JZ and JNZ may change this again below
            self.ip += size

            # Process Instruction using opcode, addresses and values
            # Addition
            if self.opcode == Opcode.ADD:
                self.memory[addresses[Operand.Three]] = values[Operand.One] + values[Operand.Two]

            # Multiplication
            elif self.opcode == Opcode.MUL:
                self.memory[addresses[Operand.Three]] = values[Operand.One] * values[Operand.Two]

            # Input
            elif self.opcode == Opcode.IN:
                # if the input queue is empty, raise an event to get input from an external event handler
                if not self.input_queue and self.is_events_enabled:
                    # if an event handler is configured, notify it else raise an exception
                    if self.input_event.listeners: 
                        self.input_event.notify()
                    else:
                        raise IntCodeComputerEventHandlerException('No Input Event Listener Found')
                # if the input queue is still empty after the event handler ran, raise an exception
                if not self.input_queue: 
                    raise IntCodeComputerInputQueueException("Input Queue is Empty")
                # process the next value on the input queue            
                self.input = int(self.input_queue.popleft())
                self.memory[addresses[Operand.One]] = self.input

            # Output
            elif self.opcode == Opcode.OUT:
                # Make the output available to external readers
                self.output = values[Operand.One]
                # Notify external event handlers if enabled and configured, raise exception if not
                if self.is_events_enabled:
                    if self.output_event.listeners: 
                        self.output_event.notify()
                    else:
                        raise IntCodeComputerEventHandlerException('No Output Event Listener Found')
                else:
                    return self.output

            # Jump if non-zero
            elif self.opcode == Opcode.JNZ:
                if values[Operand.One]!=0: self.ip = values[Operand.Two]

            # Jump if zero
            elif self.opcode == Opcode.JZ: 
                if values[Operand.One]==0: self.ip = values[Operand.Two]

            # Less Than
            elif self.opcode == Opcode.LT:
                self.memory[addresses[Operand.Three]] = 1 if values[Operand.One] < values[Operand.Two] else 0

            # Equals
            elif self.opcode == Opcode.EQ:
                self.memory[addresses[Operand.Three]] = 1 if values[Operand.One] == values[Operand.Two] else 0

            # Relative Base
            elif self.opcode == Opcode.RB:
                self.base += values[Operand.One]

            # Should never be hit ... but ... just in case :)
            else:
               raise IntCodeComputerOpCodeException("Invalid OpCode " + str(self.opcode)) 

            # setup for next instruction
            instruction = self.memory[self.ip] # obtain the instruction in memory at index pointed to by the curent instruction pointer value
            self.opcode = instruction % 100 # opcode is right-most two digits of the instruction

class IntcodeComputerTestEventHandler:
    """ Used for testing the event handlers during unit tests """

    def __init__(self, computer):
        self.computer = computer
        self.computer.input_event.listeners += [self.computer_input_event]
        self.computer.output_event.listeners += [self.computer_output_event]
        self.is_test_input_queue_exception = False
        self.input = 0
        self.output = 0
        self.output_cache = ""

    # self.is_add_to_queue is set to true during a unit test to assert that an empty queue exception is raised
    def computer_input_event(self):
        if not self.is_test_input_queue_exception:
            self.computer.input_queue.append(self.input)

    def computer_output_event(self):
        self.output = self.computer.output
        self.output_cache += f",{self.output}" if self.output_cache else str(self.output)