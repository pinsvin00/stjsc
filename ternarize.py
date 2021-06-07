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
    occuranes = []
    last = 0
    found_any = False
    for x in variable_keywords:
        if line.find(x):
            found_any = True
    if not found_any:
        return False
    

    # while True:
    #     local = {}
    #     for key in variable_keywords:
    #         if line.find(key) != -1:
    #             local[key] = line.find(key, last)
    #     minimum = 10**10
    #     for key in local:
    #         minimum = min(local[key], minimum)
    #     if minimum == 10*10:
    #         break
    #     else:
    #         last = minimum


        
        

def main():

    compiled = replace_string
    lines = []
    argv, argc = load_arguments()
    with open(argv[0], "r") as file:
        lines = file.readlines()

    linear_ternarize = []

    for line in lines:
        
        if not process_keywords(line):
            ter = ternarized(line.replace(";", ""))
            compiled = compiled.replace(replace_string, ter)

    compiled = compiled.replace(replace_string, '0')
    with open("ternarized.js", "w") as output:
        output.write(compiled)

if __name__ == "__main__":
    main()