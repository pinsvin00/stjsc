# stjsc
STJSC stands for Stupid Ternary JavaScript Compiler (although it isn't compiler)
It takes a javascript code, and builds a big nested ternary expression out of it. Maybe useful for uglifying purposes.

Notice that stjsc doesn't handle well weird code formatting. Please use prettier before compiling, to prevent setbacks.

## Running the script
Download the script and do the following

```
python ternarize.py file_name
```

The script will output ternarized code into ternarized.js file.


## Things that work in stjsc
If statements

Else statements

For statements

Nesting the following lines into  

## Things that don't work in stjsc
Functions
Else if
