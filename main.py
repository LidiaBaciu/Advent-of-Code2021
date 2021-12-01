import numpy as np

from utils import read_file


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
    
day1()
