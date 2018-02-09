
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
