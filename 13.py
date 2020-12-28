# Advent of code Year 2019
# Author = Rob Lorimer
YEAR = 2019
DAY = 13

import aoc_download
puzzle_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY)

from arcade_game import ArcadeGame

game = ArcadeGame( puzzle_input )
game.run()
print("Part 1:", game.blocks_total )

game = ArcadeGame( puzzle_input, is_play_free=True, is_show_animation=True )
game.run()
print("Part 2:", game.score )


