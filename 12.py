import aoc_download
from math import gcd
YEAR = 2019
DAY = 12

puzzle_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY)

# Read initial positions from file -> 
# [['x_axis=5', 'y_axis=13', 'z_axis=-3'], ['x_axis=18', 'y_axis=-7', 'z_axis=-13'], ... ]
raw_coordinates = [line[1:-1].split(', ')
                   for line in puzzle_input.splitlines()]


def gravity(this_axis_position, other_axis_position):
    """ returns the affect of gravity on an axis by the same axis of another moon """
    if this_axis_position > other_axis_position:
        return -1
    if this_axis_position < other_axis_position:
        return 1
    return 0


# returns true if all velocity values for given axis are 0
def is_axis_velocities_zero(axis): return all(
    [velocity[axis] == 0 for velocity in velocities])


def least_common_multiple(a, b): return a * \
    b // gcd(a, b)  # least common multiple


# Create initial positions as [[x_axis,y_axis,z_axis],[x_axis,y_axis,z_axis],...]
# Create initial velocities as [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
positions, velocities = [], []
for raw_coordinate in raw_coordinates:
    x_val, y_val, z_val = [int(item.split('=')[1]) for item in raw_coordinate]
    positions.append([x_val, y_val, z_val])
    velocities.append([0, 0, 0])

x_axis, y_axis, z_axis = 0, 1, 2  # indexes of x_axis, y_axis, z_axis
# will hold the number of cycles before each axis across all velocities becomes 0 again
x_repeat, y_repeat, z_repeat = 0, 0, 0

cycles = 1

# continue until all axis repeats have a value
while not all([x_repeat, y_repeat, z_repeat]):

    # apply gravity
    for this_index, (this_x, this_y, this_z) in enumerate(positions):
        # moon to get influence on gravity
        for other_index, (other_x, other_y, other_z) in enumerate(positions):
            if this_index == other_index:  # don't apply gravity from own position
                continue
            velocities[this_index][x_axis] += gravity(this_x, other_x)
            velocities[this_index][y_axis] += gravity(this_y, other_y)
            velocities[this_index][z_axis] += gravity(this_z, other_z)

    # apply velocity
    for position, velocity in zip(positions, velocities):
        position[x_axis] += velocity[x_axis]
        position[y_axis] += velocity[y_axis]
        position[z_axis] += velocity[z_axis]

    # determine the first cycle where all velocities of each axis become 0 again
    if not x_repeat:
        x_repeat = cycles if is_axis_velocities_zero(x_axis) else 0
    if not y_repeat:
        y_repeat = cycles if is_axis_velocities_zero(y_axis) else 0
    if not z_repeat:
        z_repeat = cycles if is_axis_velocities_zero(z_axis) else 0

    # Part 1 energy calcs
    if cycles == 1000:
        potential_energies = [abs(x_axis) + abs(y_axis) + abs(z_axis)
                              for x_axis, y_axis, z_axis in positions]
        kinetic_energies = [abs(x_axis) + abs(y_axis) + abs(z_axis)
                            for x_axis, y_axis, z_axis in velocities]
        total_energies = [pe * ke for pe,
                          ke in zip(potential_energies, kinetic_energies)]

        print("Part 1:", sum(total_energies))

    cycles += 1

# answer is least common multiple of all axis first repeat
print("Part 2:", 2 * least_common_multiple(x_repeat,
                                           least_common_multiple(y_repeat, z_repeat)))
