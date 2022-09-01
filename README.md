# stjsc
STJSC stands for Stupid Ternary JavaScript Compiler (although it isn't compiler)
It takes a javascript code, and builds a big nested ternary expression out of it. Maybe useful for uglifying purposes.

Notice that stjsc doesn't handle well weird code formatting. Please use prettier before compiling, to prevent setbacks.

## Running the script
Download the script and do the following

```
python ternarize.py input_file_name output_file_name
```

If output file name won't be provided, program will write code to file ternarized.js


## Things that work in stjsc
```
If statements
Else statements
For statements
Nesting the following lines into ternary expression  
```

## Things that don't currently work in stjsc
```
Function keyword
Else if
```

## Things that won't work in stjsc
```
Variable scoping, ternary expression prevents, creating variables inside a ternary expression. All variables in code are stored in global scope.
Specific keywords like [continue, break ... ], although there are some workarounds, like one shown in erastotenes_sieve.js in examples.
```

