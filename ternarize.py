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

def rreplace(s, old, new, ocurrence):
    li = s.split(old, ocurrence)
    return new.join(li)

def get_lines_in_block(index, lines):
    string = ';'.join(lines[index:])
    start = string.index('{')
    stack = 0
    for i in range(start, len(string)):
        if string[i] == "{":
            stack += 1
        elif string[i] == "}":
            stack -= 1
        if stack == 0:
            last = i
            break
    return string[start+1:last]

def main():
    compiled = replace_string
    lines = []
    argv, argc = load_arguments()
    argv = ["123"]
    argv[0] = "test.js"
    with open(argv[0], "r") as file:
        lines = file.readlines()


    nest_count = 0
    for index, line in enumerate(lines, 0):
        if ("for" or "while" not in line) and line.count(';') > 1:
            split_lines = line.split(';')
        else:
            split_lines = [line] 

        for expression in split_lines:
            if expression.startswith("if"):
                start = expression.index('(')
                stack = 0
                last = -1

                for i in range(start, len(expression)):
                    if expression[i] == "(":
                        stack += 1
                    elif expression[i] == ")":
                        stack -= 1
                        if stack == 0:
                            last = i
                            break
                
                condition = line[start+1:last]
                compiled = compiled.replace(replace_string, f'({condition} ?  (!replace!) : !alternative!), true ? (!next!) : 0')
                nest_count += 1

                continue

            elif expression.startswith("else"):
                compiled = compiled.replace('!replace!', '!next!')
                compiled = rreplace(compiled, '!alternative!', '!replace!', 1)
                nest_count += 1
                continue
            
            if nest_count == 1 and '}' in expression:
                compiled = compiled.replace('!replace!', '0')
                compiled = rreplace(compiled, '!next!', '!replace!', 1) #this wont work with nested expressions
                nest_count = 0
                continue
                                
            variable_keywords = ["const", "let" , "var"]
            stop = False
            for keyword in variable_keywords:
                if keyword in line:
                    variable_array.append(line)
                    stop = True
                    break
            if stop:
                continue

            ter = ternarized(line.replace(";", ""))
            compiled = compiled.replace(replace_string, ter)

    placeholders = ['!replace!', '!alternative!', "!next!"]
    for placeholder in placeholders:
        compiled = compiled.replace(placeholder, '0')
    with open("ternarized.js", "w") as output:
        output.write(''.join(variable_array))
        output.write(compiled)

if __name__ == "__main__":
    main()