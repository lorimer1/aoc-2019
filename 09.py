import aoc_download
from intcode_computer import IntCodeComputer
YEAR = 2019
DAY = 9

puzzle_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY)

computer = IntCodeComputer(puzzle_input)
computer.input_queue.append(1)
computer.run()

print("part 1:", computer.output)

computer.reset()
computer.input_queue.append(2)
computer.run()

print("part 2:", computer.output)
