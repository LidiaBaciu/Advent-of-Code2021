
def read_file(file):
    with open(file, 'r', encoding='utf8') as f:
        return [line.rstrip('\n') for line in f]