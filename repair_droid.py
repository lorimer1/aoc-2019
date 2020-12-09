# Advent of code Year 2019
# Author = Rob Lorimer

from intcode_computer import IntCodeComputer
from collections import namedtuple
import turtle
from time import sleep


class RepairDroid:

    Dir = namedtuple('Dir', ['Forward', 'dy', 'dx', 'Reverse'])

    NORTH, SOUTH, WEST, EAST = 1, 2, 3, 4
    NORTH_DIR = Dir(NORTH, -1,  0, SOUTH)
    SOUTH_DIR = Dir(SOUTH, 1,  0, NORTH)
    WEST_DIR = Dir(WEST, 0, -1, EAST)
    EAST_DIR = Dir(EAST, 0,  1, WEST)
    DIRS = [NORTH_DIR, EAST_DIR, SOUTH_DIR, WEST_DIR]

    START_CHAR = "D"
    PATH_CHAR = " "
    SYSTEM_CHAR = "S"
    WALL_CHAR = "#"
    VISITED_CHAR = "."

    # map locations you can move to (not WALL or already explored)
    OPEN_CHARS = {PATH_CHAR, SYSTEM_CHAR}    # usually PATH, END when solving a maze

    # IntCode Computer responses
    RESPONSE_IS_WALL = 0
    RESPONSE_IS_MOVED = 1
    RESPONSE_IS_SYSTEM = 2

    IS_VISITED = 3   # to use ball for visited path

    def __init__(self, program):
        self.computer = IntCodeComputer(program)
        self.maze = {(0, 0): RepairDroid.START_CHAR}
        self.system = None
        self.init_window()
        self.update_window(2, 0, 0)  #display start
        self.step_count = 0

    def solve_for_system(self, y, x):
        if self.maze[(y, x)] == RepairDroid.SYSTEM_CHAR:
            # base case - endpoint has been found
            return True
        else:
            # search recursively in each direction from here
            for dir in RepairDroid.DIRS:
                ny, nx = y + dir.dy, x + dir.dx
                if self.maze[(ny, nx)] in RepairDroid.OPEN_CHARS:  # can I go this way?
                    if self.maze[(ny, nx)] != RepairDroid.START_CHAR and self.maze[(ny, nx)] != RepairDroid.SYSTEM_CHAR:  # don't overwrite start or end
                        # mark direction chosen
                        self.maze[(y, x)] = RepairDroid.VISITED_CHAR
                        self.update_window(RepairDroid.IS_VISITED, ny, nx)
                    if self.solve_for_system(ny, nx):          # recurse...
                        self.step_count += 1
                        return True                 # solution found!

        # no solution found from this location
        if self.maze[(y, x)] != RepairDroid.START_CHAR and self.maze[(y, x)] != RepairDroid.SYSTEM_CHAR:  # don't overwrite
            # clear failed search from map
            self.maze[(y, x)] = RepairDroid.PATH_CHAR
            self.update_window(RepairDroid.RESPONSE_IS_MOVED, y, x)
        return False

    def map_out_maze(self, y, x):
        """ uses recursion to map out the maze by supplying input to the intcode computer and reading responses """
        for dir in RepairDroid.DIRS:
            ny, nx = y + dir.dy, x + dir.dx
            response = self.computer.run(dir.Forward)
            if response == RepairDroid.RESPONSE_IS_WALL:
                self.maze[(ny, nx)] = RepairDroid.WALL_CHAR
                self.update_window(response, ny, nx)
            elif ((ny, nx) in self.maze) and self.maze[(ny, nx)] == RepairDroid.VISITED_CHAR:
                self.computer.run(dir.Reverse)
            else:
                if response == RepairDroid.RESPONSE_IS_SYSTEM:
                    self.system = (ny, nx)
                    self.update_window(response, ny, nx)
                self.maze[(ny, nx)] = RepairDroid.VISITED_CHAR
                self.update_window(RepairDroid.IS_VISITED, ny, nx)
                self.map_out_maze(ny, nx)          # recurse...
                self.computer.run(dir.Reverse)  # after all directions tested for location, step back

        # no solution found from this location
        if self.maze[(y, x)] != RepairDroid.START_CHAR and self.maze[(y, x)] != RepairDroid.SYSTEM_CHAR:  # don't overwrite
            # clear failed search from map
            self.maze[(y, x)] = RepairDroid.PATH_CHAR
            self.update_window(RepairDroid.RESPONSE_IS_MOVED, y, x)
        return False

    def init_window(self):

        # setup the turtle window
        self.window = turtle.Screen()
        self.window.bgcolor('black')
        self.window.title('Repair Droid Maze')
        self.window.setup(width = 1.0, height = 1.0) # maximize screen
        
        # make constants for gif filepaths (these gifs are used for turtle graphics shapes)
        EMPTY_GIF = r'.\\media\img_empty.gif'
        WALL_GIF = r'.\\media\img_wall.gif'
        BLOCK_GIF = r'.\\media\img_block.gif'
        BALL_GIF = r'.\\media\img_ball.gif'

        # register the gifs that will be used as shapes
        #pylint: disable=E1103
        turtle.register_shape(EMPTY_GIF)
        turtle.register_shape(WALL_GIF)
        turtle.register_shape(BLOCK_GIF)
        turtle.register_shape(BALL_GIF)
        # pylint: enable=E1103

        # init the vars that help scale the turtle graphics screen to the co-ordinates we're using
        WINDOW_MULTIPLIER = 24
        # setup up functions for scaling position to screen position
        self.window_x = lambda x: x * WINDOW_MULTIPLIER
        self.window_y = lambda y: -1 * y * WINDOW_MULTIPLIER

        def make_turtle(gif_path=None, is_score=False):
            """ Make a turtle for each tile type using gifs """
            new_turtle = turtle.Turtle()
            new_turtle.hideturtle()
            new_turtle.penup()
            new_turtle.speed(0)
            new_turtle.setpos(0, 0)
            new_turtle.shape(gif_path)
            return new_turtle

        # make the turtles (graphics) for each tile
        empty_turtle = make_turtle(EMPTY_GIF)
        wall_turtle = make_turtle(WALL_GIF)
        block_turtle = make_turtle(BLOCK_GIF)
        ball_turtle = make_turtle(BALL_GIF)
        self.turtles = [wall_turtle, empty_turtle, block_turtle, ball_turtle]

        # init the dictionaries that will maintain graphics state
        self.grid_stamps = {}
        self.grid_turtles = {}


    def update_window(self, turtle_type, y, x):
        """ update the screen coordinate that represents a grid coordinate state """

        if turtle_type == RepairDroid.RESPONSE_IS_MOVED:
            # get the turtle for this coordinate if exists
            this_turtle = self.grid_turtles.get((x, y), None)
            if this_turtle:
                # remove the stamp from the window
                this_turtle.clearstamp(self.grid_stamps[(x, y)])
                # remove the stamp from the dictionary of stamped coordinates
                self.grid_stamps.pop((x, y), None)
                # remove the turtle that made the stamp
                self.grid_turtles.pop((x, y), None)
        else:
            # get a reference to the correct turtle
            this_turtle = self.turtles[turtle_type]
            # set the new postion for that turtle
            this_turtle.setpos(self.window_x(x), self.window_y(y))
            # stamp the window at that position and save the stamp id (required for later removal)
            self.grid_stamps[(x, y)] = this_turtle.stamp()
            # save a reference to the turtle that made the stamp at that position
            self.grid_turtles[(x, y)] = this_turtle
        # sleep(0.1)
