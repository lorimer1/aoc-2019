import aoc_download
YEAR = 2019
DAY = 6

puzzle_input = aoc_download.read_input_file(YEAR, DAY)
input_lines = list(puzzle_input.splitlines())

# Parents orbit the children ... lowest level is COM
# Parents are not repeated in the input and orbit a single child
parents_and_child = dict(reversed(line.strip().split(')'))
                         for line in input_lines)

# List of parents
parents_todo = list(set(parents_and_child))

# Start the path at COM which is not orbiting anything
paths = {'COM': []}

# Process each 'todo' parent
while parents_todo:
    for parent in parents_todo:
        child = parents_and_child[parent]
        if child in paths:
            paths[parent] = [child] + paths[child]
            parents_todo.remove(parent)

# Sum of all path lengths
print("Part 1:", sum(map(len, paths.values())))

# The sum of distinct orbits between YOU and SAN
set_paths_you = set(paths['YOU'])
set_paths_san = set(paths['SAN'])
set_distinct = set_paths_you.symmetric_difference(set_paths_san)

# What is left on each path is all the hops between YOU and SAN
print("Part 2:", len(set_distinct))
