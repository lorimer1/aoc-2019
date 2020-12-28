import unittest
import aoc_download
from day_14 import YEAR, DAY, get_recipes, ore_required, fuel_made

class TestDay14(unittest.TestCase):

    def test_part1_test1(self):
        test_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY, extra='_part1_test1')
        test_recipes = get_recipes(test_input)
        self.assertEqual(ore_required(test_recipes), 31)

    def test_part1_test2(self):
        test_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY, extra='_part1_test2')
        test_recipes = get_recipes(test_input)
        self.assertEqual(ore_required(test_recipes), 165)

    def test_part1_test3(self):
        test_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY, extra='_part1_test3')
        test_recipes = get_recipes(test_input)
        self.assertEqual(ore_required(test_recipes), 13312)

    def test_part1_test4(self):
        test_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY, extra='_part1_test4')
        test_recipes = get_recipes(test_input)
        self.assertEqual(ore_required(test_recipes), 180697)

    def test_part1_test5(self):
        test_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY, extra='_part1_test5')
        test_recipes = get_recipes(test_input)
        self.assertEqual(ore_required(test_recipes), 2210736)

    def test_part1_actual(self):
        test_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY, extra='')
        test_recipes = get_recipes(test_input)
        self.assertEqual(ore_required(test_recipes), 2556890)

    def test_part2_test1(self):
        test_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY, extra='_part1_test3')
        test_recipes = get_recipes(test_input)
        self.assertEqual(fuel_made(test_recipes, ore_quantity=1000000000000), 82892753)

    def test_part2_test2(self):
        test_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY, extra='_part1_test4')
        test_recipes = get_recipes(test_input)
        self.assertEqual(fuel_made(test_recipes, ore_quantity=1000000000000), 5586022)

    def test_part2_test3(self):
        test_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY, extra='_part1_test5')
        test_recipes = get_recipes(test_input)
        self.assertEqual(fuel_made(test_recipes, ore_quantity=1000000000000), 460664)

    def test_part2_actual(self):
        test_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY, extra='')
        test_recipes = get_recipes(test_input)
        self.assertEqual(fuel_made(test_recipes, ore_quantity=1000000000000), 1120408)

if __name__ == '__main__':
    unittest.main()
