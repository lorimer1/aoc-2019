from itertools import groupby
import aoc_download
YEAR = 2019
DAY = 4

puzzle_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY)
code_lowest, code_highest = map(int, puzzle_input.split('-'))


def is_code_valid(code, predicate):

    # get the counts of groups of digits ... where adjacent digits are the same
    # e.g. 599299 => keys = ('5', '9', '2', '9') ... counts = (1, 2, 1, 2)
    # *[] unpacks the list
    digits, counts = zip(*[(k, len(list(v))) for k, v in groupby(str(code))])

    # all() is an 'and' function i.e. if all items are true, the result is true
    # All consecutive digits must be equal or higher than previous digits
    # any() is an 'or' function i.e. if any items are true, the result is true
    # At least one item must match the passed in lamda function
    # Finally, return true if the all() and the any() were both true
    return all(b >= a for a, b in zip(digits, digits[1:])) and any(map(predicate, counts))


# sums all the 'True' results for is_code_valid()
# all digits need to be >= to previous, also one digit needs to be a repeat 
# of previous adjacent digits i.e. 2 or more adjacently the same
print("Part 1:", sum(is_code_valid(code, lambda x: x > 1)
                     for code in range(code_lowest, code_highest + 1)))

# same as part 1 but one of the adjacent repeats must be a pair only
print("Part 2:", sum(is_code_valid(code, lambda x: x == 2)
                     for code in range(code_lowest, code_highest + 1)))
