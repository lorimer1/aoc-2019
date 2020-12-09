import aoc_download
from intcode_computer import IntCodeComputer
YEAR = 2019
DAY = 2

puzzle_input = aoc_download.read_input_file(YEAR, DAY)
computer = IntCodeComputer(puzzle_input)
computer.memory[1] = 12
computer.memory[2] = 2
computer.run()

print("Part 1:", computer.memory[0])


def find_noun_verb(computer):
    for noun in range(100):
        for verb in range(100):
            computer.reset()
            computer.memory[1] = noun
            computer.memory[2] = verb
            computer.run()
            if computer.memory[0] == 19690720:
                return (noun, verb)


noun, verb = find_noun_verb(computer)

print("Part 2:", 100 * noun + verb)
