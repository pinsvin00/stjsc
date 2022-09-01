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

def replace_nth(s, sub, repl, n):
    find = s.rfind(sub)
    i = 1 if find != -1 else 0 
    while find != -1 and i != n:
        find = s.rfind(sub, 0 ,find + 1)
        i += 1
    if i == n:
        a = s[:find]
        b = s[find+len(sub):]
        return a + repl + b
    return s

def replace_last_occurance(s, sub, replace):
    find = s.rfind(sub)
    if find == -1:
        print("PANIK!!!")

    last_find = find

    while True:
        find = s.rfind(sub, 0, find + 1)
        if find != -1:
            last_find = find
        else:
            break
        
    find = last_find

    a = s[:find]
    b = s[find+len(sub):]

    return a + replace + b


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
    argv, argc = load_arguments()
    with open(argv[0], "r") as file:
        lines = file.readlines()


    nest_count = 0
    skip = 0
    for index, line in enumerate(lines, 0):

        if skip != 0:
            skip -=1
            continue


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

                #find if condition expression
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
                compiled = replace_last_occurance(compiled, '!alternative!', '!replace!') #setup next replace and alterantive path
                nest_count += 1
                continue


            if '}' in expression:
                compiled = compiled.replace('!replace!', '0') #terminate current streams
                compiled = replace_nth(compiled, '!next!', '!replace!', nest_count) #set stream to nearest stream pointer
                nest_count -= 1
                continue


            if expression.startswith("for"):
                last = expression.index('{')
                for_inner = expression[0:last]
                compiled = compiled.replace('!replace!', f'true ? ((() => {{ {for_inner} {{ !replace! }} }})(), !next!) : 0')
                nest_count += 1
                continue



            # we should consider that it may be multiline variable                                     
            variable_keywords = ["const", "let" , "var"]
            stop = False

            for keyword in variable_keywords:
                if keyword in line:

                    if '{' in line:
                        for index, greedy_line in enumerate(lines[index+1:]):
                            line += greedy_line
                            skip += 1
                            if '}' in greedy_line:
                                break

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
    
    if argc >= 2:
        name = argv[1]
    else:
        name = "ternarized.js"

    with open(name, "w") as output:
        output.write(''.join(variable_array))
        output.write(compiled)

if __name__ == "__main__":
    main()