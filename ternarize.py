import sys

replace_string = '!replace!'
variable_array = []

def load_arguments():
    arguments = sys.argv[1:]
    argc = len(arguments)
    return arguments, argc

def ternarized(line):
    global replace_string
    return f'true ? ({line}, {replace_string}) : 0'

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches


def process_keywords(line):
    variable_keywords = ["const", "let" , "var"]
    for keyword in variable_keywords:
        if line.find(keyword):
            variable_array.append(line)
            return True
    return False
            

def main():

    compiled = replace_string
    lines = []
    argv, argc = load_arguments()
    with open(argv[0], "r") as file:
        lines = file.readlines()

    linear_ternarize = []

    for line in lines:
        if "for" or "while" not in line:
            split_lines = line.split(';')
        else: split_lines = [line] 
        for expression in split_lines:
            if not process_keywords(expression):
                ter = ternarized(line.replace(";", ""))
                compiled = compiled.replace(replace_string, ter)

    compiled = compiled.replace(replace_string, '0')
    with open("ternarized.js", "w") as output:
        output.write(compiled)

if __name__ == "__main__":
    main()