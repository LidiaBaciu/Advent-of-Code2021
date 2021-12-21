from enum import Enum
import numpy as np

def read_file(file):
    with open(file, 'r', encoding='utf8') as f:
        return [line.rstrip('\n') for line in f]
    
def parse_command(line: str) -> tuple[str, int]:
    command, amount = line.split()
    return command, int(amount)

def read_bingo_inputs(file):
    with open(file, 'r', encoding='utf8') as f:
        drawn = list(map(int, f.readline().split(",")))
        boards = [np.mat(board.replace("\n", ";")) for board in f.read()[1:-1].split("\n\n")]
        return (drawn, boards)
    
def get_range(start, stop):
    if stop >= start:
        # Make range inclusive
        return range(start, stop+1)
    # Make range run backwards properly
    return range(start, stop-1, -1)
        
class TankFishes:
    def __init__(self, internal_timers):
        self.internal_timers = internal_timers
            
    def total_fish(self, timer, days):
        if days <= 0:
            return 1
        elif timer == 0:
            return self.total_fish(6, days-1) + self.total_fish(8, days-1)
        else:
            return self.total_fish(timer-1, days-1)
        
    def get_fishes(self, days):
        sum_fishes = 0
        for timer in self.internal_timers:
            sum_fishes += self.total_fish(timer, days)
        return sum_fishes
    
def calculateFuel(rrange):
    return sum([i for i in range(1, rrange+1)])

def get_cell_value(row, column, matrix):
    if row < 0 or column < 0 or row >= len(matrix) or column >= len(matrix):
        return 9
    return matrix[row, column]

def is_low_point(row, column, matrix):
    value = get_cell_value(row, column, matrix)
    
    if value < get_cell_value(row-1, column, matrix) \
                and value < get_cell_value(row, column-1, matrix) \
                and value < get_cell_value(row, column+1, matrix) \
                and value < get_cell_value(row+1, column, matrix):
        return True
    return False

def get_adjacents(row, column, matrix):
    adjacents = []
    rows = len(matrix)
    columns = len(matrix[0])
    if row + 1 < rows:
        adjacents.append(matrix[row+1][column])
    if row - 1 >= 0:
        adjacents.append(matrix[row-1][column])
    if column + 1 < columns:
        adjacents.append(matrix[row][column+1])
    if column - 1 >= 0:
        adjacents.append(matrix[row][column-1])
    return adjacents
                
def count_groups(row, column, matrix, groups):
    rows = len(matrix)
    columns = len(matrix[0])
    if row < 0 or row >= rows or column < 0 or column >= columns \
        or matrix[row][column] == 9 or matrix[row][column] == -1:
            return
    matrix[row][column] = -1
    groups[len(groups)-1] += 1
    count_groups(row+1, column, matrix, groups)
    count_groups(row-1, column, matrix, groups)
    count_groups(row, column+1, matrix, groups)
    count_groups(row, column-1, matrix, groups)
    
  
    
class ParanthesisMatcher:
    def __init__(self, lines):
        self.lines = lines
        self.opening = ["(", "[", "{", "<"]
        self.closing = [")", "]", "}", ">"]
        self.matches = { 
            "(": ")",
            "[": "]",
            "{": "}",
            "<": ">"
        }
        self.scores = {
            ")": 3,
            "]": 57,
            "}": 1197,
            ">": 25137
        }
        self.autocomplete_scores = {
            ")": 1,
            "]": 2,
            "}": 3,
            ">": 4
        }
        
    def get_match(self, character):
        return self.matches[character]
        
    def get_score(self, character):
        return self.scores[character]
    
    def find_illegal_character(self, line):
        stack = []
        for character in line:
            if character in self.opening:
                stack.append(character)
            elif len(stack):
                prev = stack.pop()
                if character != self.get_match(prev):
                    return character
        return None
    
    def get_stack(self, line):
        stack = []
        for character in line:
            if character in self.opening:
                stack.append(character)
            elif len(stack):
                prev = stack[-1]
                if character == self.get_match(prev):
                    stack.pop()
        return stack
    
    def find_score(self):
        score = 0
        
        for line in self.lines:
            illegal_character = self.find_illegal_character(line)
            if illegal_character:
                score += self.get_score(illegal_character)
        return score
    
    def find_scores(self):
        scores = []
        for line in self.lines:
            score = 0
            illegal_character = self.find_illegal_character(line)
            if illegal_character:
                continue
            stack = self.get_stack(line)
            stack.reverse()
            
            for char in stack:
                match = self.get_match(char)
                score = score * 5 + self.autocomplete_scores[match]
            scores.append(score)
            
        scores.sort()
        return scores[len(scores) //2]
    
class OctopusGrid:
    def __init__(self, grid):
        self.grid = grid
        self.steps = 100
    
    def get_adjacents(self, row, column):
        adjacents = []
        rows = len(self.grid)
        columns = len(self.grid[0])
        
        if row + 1 < rows:
            adjacents.append((row+1, column))
        if row - 1 >= 0:
            adjacents.append((row-1, column))
        if column + 1 < columns:
            adjacents.append((row, column+1))
        if column - 1 >= 0:
            adjacents.append((row, column-1))
        
        if (row + 1, column) in adjacents and (row, column + 1) in adjacents:
            adjacents.append((row + 1, column + 1))
        if (row + 1, column) in adjacents and (row, column - 1) in adjacents:
            adjacents.append((row+1, column-1))
        if (row-1, column) in adjacents and (row, column-1) in adjacents:
            adjacents.append((row-1, column-1))
        if (row-1, column) in adjacents and (row, column+1) in adjacents:
            adjacents.append((row-1, column+1))
        
        return adjacents
    
    def flash(self, row, column, flashes):
        flashes.append((row, column))
        
        for (x, y) in self.get_adjacents(row, column):
            if (x, y) not in flashes:
                self.grid[x, y] += 1
                
                if self.grid[x, y] > 9:
                    self.flash(x, y, flashes)
    
    def count_flashes(self):
        count = 0
        for _ in range(self.steps):
            flashes = []
            self.grid += 1
            
            for row, line in enumerate(self.grid):
                for column, n in enumerate(line):
                    if self.grid[row, column] > 9 and (row, column) not in flashes:
                        self.flash(row, column, flashes)
                        
            for (x, y) in flashes:
                self.grid[x, y] = 0
                
            count += len(flashes)
        return count
    
    def get_step(self):
        step = 0
        
        while True:
            flashes = []
            self.grid += 1
            step += 1
            
            for row, line in enumerate(self.grid):
                for column, n in enumerate(line):
                    if self.grid[row, column] > 9 and (row, column) not in flashes:
                        self.flash(row, column, flashes)
                        
            for (x, y) in flashes:
                self.grid[x, y] = 0
            
            if len(flashes) == len(self.grid) * len(self.grid[0]):
                break
        
        return step
    
class Cave:
    def __init__(self, inputs):
        self.lines = inputs
        self.edges = self.get_edges()
            

    def get_edges(self):
        edges = {}
        for line in self.lines:
            src, dest = line.split("-")
            if not dest == 'start' and not src == 'end':
                edges[src] = edges.get(src, []) + [dest]
            if not src == 'start' and not dest == 'end':
                edges[dest] = edges.get(dest, []) + [src]
        return edges
    
    
    def count(self, node, prior_visited, allow_repeat) -> int:
        visited = prior_visited | {node}
        if node == "end":
            return 1
        counter = 0
        for next in self.edges[node]:
            if next == "start":
                continue
            elif next[0].isupper():
                counter += self.count(next, visited, allow_repeat)
            elif next not in visited:
                counter += self.count(next, visited, allow_repeat)
            elif allow_repeat:
                counter += self.count(next, visited, False)
        return counter
    
    