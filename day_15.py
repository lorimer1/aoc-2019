# Advent of code Year 2019
# Author = Rob LorimerYEAR = 2019
YEAR = 2019
DAY = 15

import aoc_download
from repair_droid import RepairDroid

def part1(x,y):
    droid.window.onscreenclick(None)
    droid.solve_for_system(0,0)
    print("Part 1:", droid.step_count)
    droid.window.onscreenclick(part2)

def part2(x,y):
    droid.window.onscreenclick(None)
    print("Part 2:", "")
    droid.window.exitonclick()

if __name__ == '__main__':
    puzzle_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY)
    droid = RepairDroid( puzzle_input )
    droid.map_out_maze(0,0)
    droid.maze[(0,0)] = RepairDroid.START_CHAR
    droid.maze[droid.system] = RepairDroid.SYSTEM_CHAR

    droid.window.onscreenclick(part1)
    droid.window.mainloop()




