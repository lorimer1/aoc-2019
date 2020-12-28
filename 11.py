import aoc_download
from intcode_computer import IntCodeComputer
from custom_enums import Opcode
YEAR = 2019
DAY = 11

puzzle_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY)

BLACK, WHITE = 0, 1
X_INCREMENT_INDEX, Y_INCREMENT_INDEX = 0, 1

# headings with x and y increments
N, S, E, W = (0, -1), (0, 1), (1, 0), (-1, 0)
L = {N: W, E: N, S: E, W: S}  # heading when turning left
R = {N: E, E: S, S: W, W: N}  # heading when turning right


def turtle(start_panel_colour):

    x, y, heading = 0, 0, N  # turtle start state
    grid = {}  # grid coordinates with colour values

    computer = IntCodeComputer(puzzle_input)
    # add current colour to computer input queue
    computer.input_queue.append(start_panel_colour)
    paint_colour = computer.run()  # get new paint brush colour

    while not computer.opcode == Opcode.HALT:

        grid[(x, y)] = paint_colour

        turn_direction = computer.run()
        # turn direction = 0 is left, turn direction = 1  is right
        heading = [L, R][turn_direction][heading]
        x, y = x + heading[X_INCREMENT_INDEX], y + heading[Y_INCREMENT_INDEX]

        # get current colour, if not already seen it will be black
        current_colour = grid.get((x, y), BLACK)
        
        # add current colour to computer input queue
        computer.input_queue.append(current_colour)
        paint_colour = computer.run()  # current paint brush colour

    return grid


def render(grid):

    xs, ys = zip(*grid)
    x_min, x_max, y_min, y_max = min(xs), max(xs), min(ys), max(ys)

    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):

            panel_colour = '*' if grid.get((x, y)) == WHITE else ' '
            print(panel_colour, end='')

        print()


grid = turtle(start_panel_colour=BLACK)
print("Part 1:", len(grid))

grid = turtle(start_panel_colour=WHITE)
print("Part 2: see below \n")
render(grid)
