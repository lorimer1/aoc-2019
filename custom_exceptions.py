
class IntCodeComputerEventHandlerException(Exception):
    """ Fires when no Input or Output event handler is configured (when event handlers are enabled) """
    pass

class IntCodeComputerInputQueueException(Exception):
    """ Fires when Input is required and none is available in the input queue """
    pass

class IntCodeComputerOpCodeException(Exception):
    """ Fires when an invalid opcode is found at the instruction pointer memory address """
    pass
