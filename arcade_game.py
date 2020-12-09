# Advent of code Year 2019
# Author = Rob Lorimer

from intcode_computer import IntCodeComputer
import turtle


class ArcadeGame:

    def __init__(self, program, is_play_free=False, is_show_animation=False):

        # indexes of tile types ... the intcode computer output uses these indexes
        self.EMPTY = 0
        self.WALL = 1
        self.BLOCK = 2
        self.PADDLE = 3
        self.BALL = 4

        # intitialize a few vars used later
        self.x = self.y = None
        self.blocks_total = self.score = 0
        self.ball_x = self.paddle_x = 0

        # init the intcode computer and setup event handlers
        self.computer = IntCodeComputer(program, is_enable_events=True)
        self.computer.input_event.listeners += [self.input_handler]
        self.computer.output_event.listeners += [self.output_handler]

        # if playing free (part 2) then set memory location 0 =2
        if is_play_free:
            self.computer.memory[0] = 2

        # if animating (part 2) then get the turtle graphics initialized
        if is_show_animation:
            self.init_window()
        self.is_show_animation = is_show_animation

    def run(self):
        """ Wrapper function to run the intcode computer """
        self.computer.run()

    def input_handler(self):
        """ whenever the intcode computer wants input we give a value to move the paddle to the same x position as the ball """
        # move the paddle toward the ball x value ... -1, 0, +1
        self.computer.input_queue.append(
            (self.ball_x > self.paddle_x) - (self.ball_x < self.paddle_x))

    def output_handler(self):
        """ whenever the intcode computer gives output, save x (1st output) and y (2nd output) and process the tile (3rd output) """
        output = self.computer.output
        if self.x == None:                  # process first output which will be x value
            self.x = output
        elif self.y == None:                # process second output which will be y value
            self.y = output
        # process the tile (or score) which will be the third output
        else:
            if self.x == -1 and self.y == 0:
                self.score = output
                if self.is_show_animation:  # write the score to the screen if animation requested
                    self.score_turtle.clear()
                    self.score_turtle.write(
                        f'Score: {self.score}', False, align='left', font=('Arial', 14, 'normal'))
            else:
                # increment the blocks total it the output is a block
                self.blocks_total += 1 if output == self.BLOCK else 0
                # save the ball x position if the outpult is the ball
                self.ball_x = self.x if output == self.BALL else self.ball_x
                # save the paddle x position if the output is the paddle
                self.paddle_x = self.x if output == self.PADDLE else self.paddle_x
                if self.is_show_animation:
                    # update the window if animation requested
                    self.update_window(output)

            self.x = self.y = None

    def init_window(self):

        # setup the turtle window
        window = turtle.Screen()
        window.bgcolor('black')
        window.title('Arcade Game')

        # make constants for gif filepaths (these gifs are used for turtle graphics shapes)
        EMPTY_GIF = r'.\\media\img_empty.gif'
        WALL_GIF = r'.\\media\img_wall.gif'
        BLOCK_GIF = r'.\\media\img_block.gif'
        PADDLE_GIF = r'.\\media\img_paddle.gif'
        BALL_GIF = r'.\\media\img_ball.gif'

        # register the gifs that will be used as shapes
        #pylint: disable=E1103
        turtle.register_shape(EMPTY_GIF)
        turtle.register_shape(WALL_GIF)
        turtle.register_shape(BLOCK_GIF)
        turtle.register_shape(PADDLE_GIF)
        turtle.register_shape(BALL_GIF)
        # pylint: enable=E1103

        # init the vars that help scale the turtle graphics screen to the co-ordinates we're using
        WIDTH, HEIGHT = 35, 25
        WINDOW_MULTIPLIER = 26
        WINDOW_X_OFFSET = 0 - (WIDTH * WINDOW_MULTIPLIER // 2)
        WINDOW_Y_OFFSET = 0 + (HEIGHT * WINDOW_MULTIPLIER // 2)

        def make_turtle(gif_path=None, is_score=False):
            """ Make a turtle for each tile type using gifs """
            new_turtle = turtle.Turtle()
            new_turtle.hideturtle()
            new_turtle.penup()
            new_turtle.speed(0)
            if is_score:    # score is a special case i.e. is text rather than a shape
                new_turtle.setpos(
                    WINDOW_X_OFFSET, WINDOW_Y_OFFSET + 1 * WINDOW_MULTIPLIER)
                new_turtle.color('white')
                new_turtle.write('Score: 0', False, align='left',
                                 font=('Arial', 14, 'normal'))
            else:           # set the intial positional to be outside the grid
                new_turtle.setpos(WINDOW_X_OFFSET - WINDOW_MULTIPLIER,
                                  WINDOW_Y_OFFSET + WINDOW_MULTIPLIER)
                new_turtle.shape(gif_path)
            return new_turtle

        # make the turtles (graphics) for each tile
        empty_turtle = make_turtle(EMPTY_GIF)
        wall_turtle = make_turtle(WALL_GIF)
        block_turtle = make_turtle(BLOCK_GIF)
        paddle_turtle = make_turtle(PADDLE_GIF)
        ball_turtle = make_turtle(BALL_GIF)
        self.turtles = [empty_turtle, wall_turtle,
                        block_turtle, paddle_turtle, ball_turtle]

        # make the score turtle (graphic)
        self.score_turtle = make_turtle(is_score=True)

        # init the dictionaries that will maintain graphics state
        self.grid_stamps = {}
        self.grid_turtles = {}

        # setup up functions for scaling position to screen position
        self.window_x = lambda x: WINDOW_X_OFFSET + (x * WINDOW_MULTIPLIER)
        self.window_y = lambda y: WINDOW_Y_OFFSET - (y * WINDOW_MULTIPLIER)

    def update_window(self, turtle_type):
        """ update the screen coordinate that represents a grid coordinate state """

        if turtle_type == self.EMPTY:
            # get the turtle for this coordinate if exists
            this_turtle = self.grid_turtles.get((self.x, self.y), None)
            if this_turtle:
                # remove the stamp from the window
                this_turtle.clearstamp(self.grid_stamps[(self.x, self.y)])
                # remove the stamp from the dictionary of stamped coordinates
                self.grid_stamps.pop((self.x, self.y), None)
                # remove the turtle that made the stamp
                self.grid_turtles.pop((self.x, self.y), None)
        else:
            # get a reference to the correct turtle
            this_turtle = self.turtles[turtle_type]
            # set the new postion for that turtle
            this_turtle.setpos(self.window_x(self.x), self.window_y(self.y))
            # stamp the window at that position and save the stamp id (required for later removal)
            self.grid_stamps[(self.x, self.y)] = this_turtle.stamp()
            # save a reference to the turtle that made the stamp at that position
            self.grid_turtles[(self.x, self.y)] = this_turtle
