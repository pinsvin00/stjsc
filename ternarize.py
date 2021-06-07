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
    compiled = '!replace!'
    lines = []
    bloat_type = "extreme"
    argv, argc = load_arguments()
    argv = ["123"]
    argv[0] = "test.js"
    with open(argv[0], "r") as file:
        lines = file.readlines()


    nest_count = 0
    for index, line in enumerate(lines, 0):
        split_lines = [line] 
        for expression in split_lines:
            expression = expression.replace('\n', '')
            expression = expression.strip()
            if len(expression) == 0:
                continue
            if expression.startswith("if"):
                start = expression.index('(')
                stack = 0
                last = -1
                #find inner conidtion in if ()
                for i in range(start, len(expression)):
                    if expression[i] == "(":
                        stack += 1
                    elif expression[i] == ")":
                        stack -= 1
                        if stack == 0:
                            last = i
                            break
                
                condition = expression[start+1:last]
                compiled = compiled.replace(replace_string, f'({condition} ?  (!replace!) : !alternative!), true ? (!next!) : 0') 
                #set current stream and two points of stream regulators
                nest_count += 1
                continue

            elif expression.startswith("else"):
                compiled = compiled.replace('!replace!', '!next!') #terminate all replaces
                compiled = rreplace(compiled, '!alternative!', '!replace!', 1) #setup next replace and alterantive path
                nest_count += 1
                continue


            if '}' in expression:
                compiled = compiled.replace('!replace!', '0') #terminate current streams
                compiled = rreplace(compiled, '!next!', '!replace!', nest_count) #set stream to nearest stream pointer 
                #RREPLACE DOESNT WORK!
                nest_count -= 1
                continue


            if expression.startswith("for"):
                last = expression.index('{')
                for_inner = expression[0:last]
                compiled = compiled.replace('!replace!', f'true ? ((() => {{ {for_inner} {{ !replace! }} }})(), !next!) : 0')
                nest_count += 1
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