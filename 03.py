import aoc_download
import turtle
YEAR = 2019
DAY = 3

# setup screen
window = turtle.Screen()
window.bgcolor('black')
window.title('AOC Day 3')
window.setup(width=1.0, height=1.0)  # make full screen


def make_turtle(colour):
    new_turtle = turtle.Turtle()
    new_turtle.color(colour)
    new_turtle.speed(0)
    return new_turtle


wire_a_turtle = make_turtle('white')
wire_b_turtle = make_turtle('yellow')

# two lines of text each with comma separated input
puzzle_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY)
input_lines = list(puzzle_input.splitlines())
moves_a = list(input_lines[0].split(','))
moves_b = list(input_lines[1].split(','))

# dictionary of movements for each step in a direction
MOVE_DELTAS = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0)
}

ANGLES = {
    'U': 0,
    'D': 180,
    'L': 270,
    'R': 90
}


def get_path(moves, wire_turtle):
    result = {}
    x = y = total_steps = 0
    for move in moves:

        direction = move[0]  # first character in string

        # Obtain the delta x,y for each step for this direction
        (dx, dy) = MOVE_DELTAS[direction]
        wire_turtle.setheading(ANGLES[direction])

        # steps is the number remaining after single char representing direction is stripped
        steps = int(move[1:])
        wire_turtle.forward(steps // 20)

        # Ensure every (x,y) that is touched is captured during a move
        # 0 to (steps-1) ... still causes an iteration for every step as '0' based
        for _ in range(steps):

            # take a step
            x, y, total_steps = x + dx, y + dy, total_steps + 1

            # .setdefault ensures duplicate (x,y) does not overwrite the first time (x,y) was reached
            # This way, the least total_steps to any point is in the dictionary
            result.setdefault((x, y), total_steps)

    return result


# get each paths points with number of steps to each point
# For duplicate points, the first time to the point is kept (others are discarded)
path_a = get_path(moves_a, wire_a_turtle)
path_b = get_path(moves_b, wire_b_turtle)

# creates a sets of the points ('keys' of the paths which are dictionaries)
points_a = set(path_a)
points_b = set(path_b)

# & results in the intersection of two sets
intersections = points_a & points_b

# manhattan distance is abs(x) + abs(y)
manhattan_distances = [sum(map(abs, point)) for point in intersections]

# Part 1 answer is the minimum manhattan distance
print("Part 1:", min(manhattan_distances))

# sum of steps for both path_a and path_b to each intersection
step_distances = [path_a[point] + path_b[point] for point in intersections]

# Part 2 answer is minimum sum of steps to an intersection
print("Part 2:", min(step_distances))

delay = input("press enter to finish")
