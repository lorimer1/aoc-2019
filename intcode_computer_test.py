import unittest
import aoc_download
from intcode_computer import IntCodeComputer, IntcodeComputerTestEventHandler
from custom_exceptions import IntCodeComputerEventHandlerException, IntCodeComputerInputQueueException, IntCodeComputerOpCodeException
from custom_enums import Opcode

class TestIntCodeComputer(unittest.TestCase):

    # def setUp(self):
    #     self.computer = IntCodeComputer()

    def test_intcode_load(self):
        self.computer = IntCodeComputer("2,3,0,3,99")
        self.assertListEqual(list(self.computer.memory.values()), [2,3,0,3,99])

    def test_intcode_opcode_exeption(self):
        self.computer = IntCodeComputer("0,0,99")
        self.assertRaises(IntCodeComputerOpCodeException,self.computer.run)

    def test_intcode_ADD(self):
        self.computer = IntCodeComputer("1,0,0,0,99")
        self.computer.run()
        self.assertListEqual(list(self.computer.memory.values()), [2,0,0,0,99])

    def test_intcode_MUL(self):
        self.computer = IntCodeComputer("2,3,0,3,99")
        self.computer.run()
        self.assertListEqual(list(self.computer.memory.values()), [2,3,0,6,99])

    def test_intcode_IN_input_queue(self):
        self.computer = IntCodeComputer("3,0,3,2,99")
        self.computer.input_queue.append(5)
        self.computer.input_queue.append(6)
        self.computer.run()
        self.assertListEqual(list(self.computer.memory.values()), [5,0,6,2,99])

    def test_intcode_IN_input_queue_empty_exception(self):
        self.computer = IntCodeComputer("3,0,99")
        self.assertRaises(IntCodeComputerInputQueueException,self.computer.run)

    def test_intcode_IN_event_handler_input(self):
        self.computer = IntCodeComputer("3,0,99", is_enable_events=True)
        self.event_handlers = IntcodeComputerTestEventHandler(self.computer)
        self.event_handlers.input = 88
        self.event_handlers.is_test_input_queue_exception = False
        self.computer.run()
        self.assertEqual(self.computer.input, self.event_handlers.input)

    def test_intcode_IN_event_handler_input_queue_empty_exception(self):
        self.computer = IntCodeComputer("3,0,99", is_enable_events=True)
        self.event_handlers = IntcodeComputerTestEventHandler(self.computer)
        self.event_handlers.is_test_input_queue_exception = True
        self.assertRaises(IntCodeComputerInputQueueException,self.computer.run)

    def test_intcode_IN_event_handler_missing_exeption(self):
        self.computer = IntCodeComputer("3,0,99", is_enable_events=True)
        self.assertRaises(IntCodeComputerEventHandlerException,self.computer.run)

    def test_intcode_OUT(self):
        self.computer = IntCodeComputer("104,88,99")
        self.assertEqual(self.computer.run(), 88)

    def test_intcode_OUT_event_handler(self):
        self.computer = IntCodeComputer("104,88,99", is_enable_events=True)
        self.event_handlers = IntcodeComputerTestEventHandler(self.computer)
        self.computer.run()
        self.assertEqual(self.event_handlers.output, 88)

    def test_intcode_OUT_event_handler_missing_exeption(self):
        self.computer = IntCodeComputer("104,88,99", is_enable_events=True)
        self.assertRaises(IntCodeComputerEventHandlerException, self.computer.run)

    def test_intcode_modes(self): # using day 5 diagnostic test
        self.computer = IntCodeComputer( aoc_download.aoc.puzzle_input_file(year=2019, day=5) )
        self.computer.input_queue.append(1)
        while not (self.computer.output or self.computer.opcode == Opcode.HALT):
            self.computer.run()
        self.assertEqual(self.computer.output,6069343)

    def test_intcode_EQ_true(self): 
        self.computer = IntCodeComputer("3,9,8,9,10,9,4,9,99,-1,8")
        self.assertEqual(self.computer.run(8),1)

    def test_intcode_EQ_false(self): 
        self.computer = IntCodeComputer("3,9,8,9,10,9,4,9,99,-1,8")
        self.assertEqual(self.computer.run(7),0)

    def test_intcode_LT_true(self): 
        self.computer = IntCodeComputer("3,3,1107,-1,8,3,4,3,99")
        self.assertEqual(self.computer.run(7),1)

    def test_intcode_LT_false(self): 
        self.computer = IntCodeComputer("3,3,1107,-1,8,3,4,3,99")
        self.assertEqual(self.computer.run(8),0)

    # def test_intcode_JZ_true(self): 
    #     self.computer = IntCodeComputer("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9")
    #     self.assertEqual(self.computer.run(0),0)

    def test_intcode_JZ_false(self): 
        self.computer = IntCodeComputer("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9")
        self.assertEqual(self.computer.run(10),1)

    def test_intcode_jumps_test1(self): 
        self.computer = IntCodeComputer("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99")
        self.assertEqual(self.computer.run(5),999)

    def test_intcode_jumps_test2(self): 
        self.computer = IntCodeComputer("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99")
        self.assertEqual(self.computer.run(8),1000)

    def test_intcode_jumps_test3(self): 
        self.computer = IntCodeComputer("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99")
        self.assertEqual(self.computer.run(10),1001)

    def test_intcode_relative_mode(self):
        self.computer = IntCodeComputer("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99", is_enable_events=True)
        self.event_handlers = IntcodeComputerTestEventHandler(self.computer)
        self.computer.run()
        self.assertEqual(self.event_handlers.output_cache, '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99')

    def test_intcode_large_numbers(self):
        self.computer = IntCodeComputer("104,1125899906842624,99")
        self.assertEqual(self.computer.run(),1125899906842624)

if __name__ == '__main__':
    unittest.main()
