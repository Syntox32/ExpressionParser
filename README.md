# Expression Solver
A small, self contained lexer and expression parser written in Python. Compatible with Python3 and 2. No pip requirements.

Example: `main.py`
```
from solver import Parser

def main():
    expr = "2 + sin(1/2) * 44.0"
    print("\"{}\"".format(expr))
    parser = Parser(expr)
    tokens = parser.parse()
    for t in tokens:
        print(t.token)

if __name__ == "__main__":
    main()

```
```
~# python ./main.py
"2 + sin(1/2) * 44.0"
Variable.Constant
Operator.Add
Function.Sin
Operator.LeftParen
Variable.Constant
Operator.Divide
Variable.Constant
Operator.RightParen
Operator.Multiply
Variable.Constant
```

Note that this is an expression *parser* and not a *solver*.

This is an upload of some old code from 2016. This code was used in my project
`LittleMan`.
