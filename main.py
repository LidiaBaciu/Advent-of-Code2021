import numpy as np

from utils import read_file, parse_command


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

day2()
