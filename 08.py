import aoc_download
YEAR = 2019
DAY = 8

puzzle_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY)

width, height = 25, 6
layer_size = width * height

# convert all input chars to a single list of integers
data = list(map(int, list(puzzle_input)))

# break the large list into a list of lists i.e. list of layers
layers = [data[i:i+layer_size] for i in range(0, len(data), layer_size)]

# determine layer with minimum count of 0's
layer_min_0 = min(layers, key=lambda x: x.count(0))

# multiple count of 1's by count of 2's for that layer
print("Part 1:", layer_min_0.count(1) * layer_min_0.count(2))

# start with blank image
image = [' '] * layer_size
for layer in reversed(layers):
    for pixel, value in enumerate(layer):
        if value == 0:
            image[pixel] = ' '
        if value == 1:
            image[pixel] = 'X'

print("Part 2: see image below\n")
for i in range(0, len(image), width):
    print(''.join(image[i:i+width]))
