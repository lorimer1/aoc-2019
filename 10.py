import aoc_download
from intcode_computer import IntCodeComputer
import math
YEAR = 2019
DAY = 10

puzzle_input = aoc_download.read_input_file(YEAR, DAY)
lines = list(puzzle_input.splitlines())
asteroids = [(x, y) for y in range(len(lines)) for x in range(
    len(lines[0])) if lines[y][x] == '#']  # co-ordinates of all asteroids

x, y = 0, 1  # index of x and y axis in a point


def angle(p1, p2): 
    """ angle clockwise from vertical """
    return math.atan2(p2[x] - p1[x], p1[y] - p2[y]) % (2 * math.pi)

def visible_asteroids(asteroids, asteroid):
    return len(set(angle(asteroid, test_asteroid) 
            for test_asteroid in asteroids if asteroid != test_asteroid))


print("Part 1:", max(visible_asteroids(asteroids, asteroid)
                     for asteroid in asteroids))  # most asteroids visible from any other asteroid

# find and remove our base from the list of asteroids (but keep our base position in 'our_base')
our_base = max(
    asteroids, key=lambda asteroid: visible_asteroids(asteroids, asteroid))
asteroids.remove(our_base)

# sort each asteroid by it's length form our base
# sort asteroids by distance from our base
asteroids.sort(key=lambda asteroid: math.hypot(
    asteroid[x] - our_base[x], asteroid[y] - our_base[y]))

# rank each asteroid based on the number of asteroids on the same angle. 0 for closest, 1 for next closest
ranks = {asteroid: sum(angle(our_base, asteroid) == angle(our_base, other_asteroid)
            for other_asteroid in asteroids[:i]) for i, asteroid in enumerate(asteroids)}

# sort by closet asteroids on each angle ... get 199th asteroid in this list
x1, y1 = sorted(asteroids, key=lambda asteroid: (
    ranks[asteroid], angle(our_base, asteroid)))[199]

print("Part 2:", x1 * 100 + y1)
