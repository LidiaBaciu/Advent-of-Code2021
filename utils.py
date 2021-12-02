
def read_file(file):
    with open(file, 'r', encoding='utf8') as f:
        return [line.rstrip('\n') for line in f]
    
def parse_command(line: str) -> tuple[str, int]:
    command, amount = line.split()
    return command, int(amount)