import numpy as np
import re
from itertools import product
import math

from utils import read_file, parse_command, read_bingo_inputs, get_range, calculateFuel
from utils import TankFishes, ParanthesisMatcher, OctopusGrid, Cave
from utils import get_adjacents, count_groups


def day1():
    measurements = np.array(read_file('input.txt'), 'i4')

    results = lambda res: sum(
        current < right for current, right in zip(res, res[1:])
    )
    
    # Part 1
    print(results(measurements))
    
    # Part 2
    print(results(tuple(
        sum(window) for window in zip(measurements, measurements[1:], measurements[2:])
    )))
   
    
def day2():
    commands = tuple(map(parse_command, read_file('input.txt')))
    
    horizontal = 0
    depth = 0
    
    for command, amount in commands:
        match command:
            case "forward": horizontal += amount
            case "down": depth += amount
            case "up": depth -= amount
            case _:
                raise AssertionError
            
    print(horizontal * depth)
    
    # Part 2
    horizontal = depth = aim = 0
    
    for command, amount in commands:
        match command:
            case "forward": 
                horizontal += amount
                depth += amount * aim
            case "down": aim += amount
            case "up": aim -= amount
            case _:
                raise AssertionError
            
    print(horizontal * depth)


def day3():
    lines = np.loadtxt("input.txt", "U")
    bits = int(len(lines[0]))
    data = lines.view('U1').astype(int).reshape(lines.shape[0], bits)
    pow2 = 1 << np.arange(bits)[::-1]
    
    print(pow2[1:5])
    
    nb_ones = (data == 1).sum(axis=0)
    nb_zeros = (data == 0).sum(axis=0)
    gamma_rate = pow2.dot(nb_ones > nb_zeros)
    epsilon_rate = pow2.dot(nb_ones < nb_zeros)
    result = gamma_rate * epsilon_rate
    
    print(result)
    
    a = b = data
    for i in range(bits):
        a_col = a[:, i]
        b_col = b[:, i]
        a = a[a_col == (a_col.sum()*2 >= a_col.size)] if len(a) > 1 else a
        b = b[b_col == (b_col.sum()*2 < b_col.size)] if len(b) > 1 else b
        
    result = pow2.dot(a[0]) * pow2.dot(b[0])
    
    print(result)
    
    
def day4():
    (drawn, boards) = read_bingo_inputs("input.txt")
    masked_boards = [np.ma.masked_array(board) for board in boards]
    
    result = 0
    for draw, board in product(drawn, masked_boards):
        board.mask |= board.data == draw
        line_sum = board.mask.sum(0)
        column_sum = board.mask.sum(1)
        if np.any(line_sum == 5) or np.any(column_sum == 5):
            result = board.sum() * draw
            break
    print(result)
    
    winning_boards = set()
    for draw, (index, board) in product(drawn, enumerate(masked_boards)):
        board.mask |= board.data == draw
        line_sum = board.mask.sum(0)
        column_sum = board.mask.sum(1)
        if np.any(line_sum == 5) or np.any(column_sum == 5):
            if index not in winning_boards and len(winning_boards) == len(boards) - 1:
                result = board.sum() * draw
                break
            winning_boards.add(index)
    print(result)
    
    
def day5():
    lines = read_file("input.txt")
    coordinates = np.array([re.match('(\d+),(\d+) -> (\d+),(\d+)', line).groups() for line in lines]).astype(int)
    size = np.max(coordinates) + 1
    
    grid = np.zeros((size, size))
    
    x_same_indexes = coordinates[:, 0] == coordinates[:, 2]
    y_same_indexes = coordinates[:, 1] == coordinates[:, 3]
    hv_indexes = x_same_indexes | y_same_indexes
    vh_lines = coordinates[hv_indexes]
    
    for x1, y1, x2, y2 in vh_lines:
        y_range = get_range(y1, y2)
        x_range = get_range(x1, x2)
        grid[y_range, x_range] += 1
        
    result = (grid >= 2).sum()
    print(result)
    
    grid = np.zeros((size, size))
    for x1, y1, x2, y2 in coordinates:
        y_range = get_range(y1, y2)
        x_range = get_range(x1, x2)
        grid[y_range, x_range] += 1
        
    result = (grid >= 2).sum()
    print(result)
    
    
def day6():
    lines = np.loadtxt("input.txt", delimiter=",")
    fish_tank = TankFishes(lines)
    print(fish_tank.get_fishes(80))
    # too slow
    print(fish_tank.get_fishes(256))
  
    
def day6_np():
    days = 256
    lines = np.loadtxt("input.txt", delimiter=",", dtype="uint32")
    fish = np.zeros(9)
    age, count = np.unique(lines, return_counts=True)
    fish[age] = count
    
    gen = np.copy(fish)
    for _ in range(days):
        gen[7] += gen[0]
        gen = np.roll(gen, -1)
    result = sum(gen)
    print(result)


def day7():
    lines = np.loadtxt("input.txt", delimiter=",", dtype="int32")
    
    median = round(np.median(lines))
    result = sum([abs(median - nb) for nb in lines])
    print(result)
    
    mean = np.mean(lines)
    meanFloor = math.floor(mean)
    meanCeil = math.ceil(mean)
    
    meanSubFloor = sum([calculateFuel(i) for i in abs(lines - meanFloor)])
    meanSubCeil = sum([calculateFuel(i) for i in abs(lines - meanCeil)])
    
    result = min(meanSubCeil, meanSubFloor)
    print(result)


def day8():
    pass


def day9():
    lines = read_file("input.txt")
    data = np.array([list(map(int, [c for c in line])) for line in lines])
    
    len_rows = len(data)
    len_cols = len(data[0])
    rows = range(len_rows)
    columns = range(len_cols)
    
    result = 0
    for row in rows:
        for column in columns:
            if data[row][column] < min(get_adjacents(row, column, data)):
                result += 1 + data[row][column]
         
    groups = []
    for row in rows:
        for column in columns:
            groups.append(0)
            count_groups(row, column, data, groups)
        
    gr = sorted(groups, reverse=True)[:3]
    print(math.prod(gr))
    
    
def day10():
    lines = read_file("input.txt")
    matcher = ParanthesisMatcher(lines)
    print(matcher.find_score())
    print(matcher.find_scores())
    
    
def day11():
    lines = np.loadtxt("input.txt", "U")
    bits = int(len(lines[0]))
    data = lines.view('U1').astype(int).reshape(lines.shape[0], bits)

    octopuses = OctopusGrid(data)
    # print(octopuses.count_flashes())
    print(octopuses.get_step())
                
def day12():
    lines = read_file("input.txt")
    cave = Cave(lines)
    print(cave.count('start', set(), False))
    print(cave.count('start', set(), True))

day12()
