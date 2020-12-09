import aoc_download
from intcode_computer import IntCodeComputer
from custom_enums import Opcode
YEAR = 2019
DAY = 5

puzzle_input = aoc_download.read_input_file(YEAR, DAY)

computer = IntCodeComputer(puzzle_input)
computer.input_queue.append(1)
while not (computer.output or computer.opcode == Opcode.HALT):
    computer.run()

print("Part 1:", computer.output)

computer.reset()
computer.input_queue.append(5)
computer.run()

print("Part 2:", computer.output)
