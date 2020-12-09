import os
from collections import namedtuple

Dir = namedtuple("Dir", ["char", "dy", "dx"])

class Maze:
    START = "S"
    END   = "E"
    WALL  = "#"
    PATH  = " "
    OPEN  = {PATH, END}  # map locations you can move to (not WALL or already explored)

    RIGHT = Dir(">",  0,  1)
    DOWN  = Dir("v",  1,  0)
    LEFT  = Dir("<",  0, -1)
    UP    = Dir("^", -1,  0)
    DIRS  = [RIGHT, DOWN, LEFT, UP]

    @classmethod
    def load_maze(cls, fname):
        with open(os.path.dirname(__file__) + "\\" + fname) as inf:
            lines = (line.rstrip("\r\n") for line in inf)
            maze  = [list(line) for line in lines]
        return cls(maze)

    def __init__(self, maze):
        self.maze = maze

    def __str__(self):
        return "\n".join(''.join(line) for line in self.maze)

    def find_start(self):
        for y,line in enumerate(self.maze):
            try:
                x = line.index("S")
                return y, x
            except ValueError:
                pass

        # not found!
        raise ValueError("Start location not found")

    def solve(self, y, x):
        if self.maze[y][x] == Maze.END:
            # base case - endpoint has been found
            return True
        else:
            # search recursively in each direction from here
            for dir in Maze.DIRS:
                ny, nx = y + dir.dy, x + dir.dx
                if self.maze[ny][nx] in Maze.OPEN:  # can I go this way?
                    if self.maze[y][x] != Maze.START: # don't overwrite Maze.START
                        self.maze[y][x] = dir.char  # mark direction chosen
                    if self.solve(ny, nx):          # recurse...
                        return True                 # solution found!

            # no solution found from this location
            if self.maze[y][x] != Maze.START:       # don't overwrite Maze.START
                self.maze[y][x] = Maze.PATH         # clear failed search from map
            return False

def main():
    maze = Maze.load_maze("somemaze.txt")

    print("Maze loaded:")
    print(maze)

    try:
        sy, sx = maze.find_start()
        print("solving...")
        if maze.solve(sy, sx):
            print(maze)
        else:
            print("    no solution found")
    except ValueError:
        print("No start point found.")

if __name__=="__main__":
    main()
