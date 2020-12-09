import aoc_download

YEAR = 2019
DAY = 1

# each mass is on a separate line of the puzzle_input file
puzzle_input = aoc_download.read_input_file(YEAR, DAY)
masses = list(map(int, puzzle_input.splitlines()))


def fuel_calc(mass): return mass//3 - 2


print("Part 1:", sum(map(fuel_calc, masses)))


def fuel_recursive(mass):
    fuel = fuel_calc(mass)
    return fuel + fuel_recursive(fuel) if fuel > 0 else 0


print("Part 2:", sum(map(fuel_recursive, masses)))
