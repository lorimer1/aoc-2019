# Advent of code Year 2019
# Author = Rob Lorimer
YEAR = 2019
DAY = 14

import aoc_download
import math

def get_recipes(recipe_data):
    formulas = [[[
        (int(quantity_of_element.split(' ')[
         0]), quantity_of_element.split(' ')[1])
        for quantity_of_element in equation_side.split(", ")]
        for equation_side in equation.split(' => ')]
        for equation in recipe_data.splitlines()]

    recipes = {}
    for formula in formulas:
        bill_of_materials = formula[0]
        finished_good = formula[1][0]
        material = finished_good[1]
        material_quantity = int(finished_good[0])
        recipes[material] = (material_quantity, bill_of_materials)
    return recipes


def ore_required(recipes, fuel_required=1):
    """ Calculates the amount of ORE required for a given amount of fuel """

    stock_required = {'FUEL': fuel_required}
    is_finished = False

    while not is_finished:
        sku, sku_quantity_required = next((sku, sku_quantity_required)
                                          for sku, sku_quantity_required in stock_required.items() if sku_quantity_required > 0 and sku != 'ORE')
        min_batch_size, bom = recipes[sku]
        batches_required = math.ceil(sku_quantity_required/min_batch_size)
        for quantity, ingredient in bom:
            stock_required[ingredient] = stock_required.get(
                ingredient, 0) + batches_required * quantity
        stock_required[sku] -= batches_required * min_batch_size
        is_finished = len([(sku, sku_quantity_required) for sku, sku_quantity_required in stock_required.items()
                           if sku_quantity_required > 0 and sku != 'ORE']) == 0

    return stock_required['ORE']


def fuel_made(recipes, ore_quantity):
    # For part 2 I originally used a brute force method.
    # Use interpolation to get cloes
    # Formula is: y = mx + c ... worked out m and c using two points (x1,y1) and (x2,y2)
    x1 = 1000
    y1 = ore_required(recipes, x1)
    x2 = 100000
    y2 = ore_required(recipes, x2)
    m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1
    
    fuel = math.ceil((ore_quantity - c) / m) # Now we have the full y = mx + c, work out x (ORE) for y = FUEL
    ore_for_fuel = ore_required(recipes, fuel)
    if ore_for_fuel == ore_quantity:
        return fuel

    # if not correct, move closer 1 fuel at a time until the higest ore for fuel below ore_quantity
    if ore_for_fuel < ore_quantity:
        while ore_for_fuel < ore_quantity:
            fuel += 1
            ore_for_fuel = ore_required(recipes, fuel)
        fuel -= 1
        return fuel
   
    if ore_for_fuel > ore_quantity:
        while ore_for_fuel > ore_quantity:
            fuel -= 1
            ore_for_fuel = ore_required(recipes, fuel)
        return fuel

if __name__ == '__main__':
    puzzle_input = aoc_download.aoc.puzzle_input_file(YEAR, DAY)
    recipes = get_recipes(puzzle_input)
    print("Part 1:", ore_required(recipes))
    print("Part 2:", fuel_made(recipes, ore_quantity=1000000000000))
