
import math
from enum import Enum, IntEnum

class TokenType(IntEnum):
    Value    = 0
    Operator = 1
    Function = 2
    Constant = 3

class Operator(IntEnum):
    Add        = 0
    Subtract   = 1
    Multiply   = 2
    Divide     = 3
    LeftParen  = 4
    RightParen = 5
    Power      = 6
    Equals     = 7
    LessThan   = 8
    MoreThan   = 9

    @property
    def type(self):
        return TokenType.Operator

class Function(IntEnum):
    Sin = 0
    Cos = 1
    Tan = 2
    Log = 3
    Ln  = 4

    @property
    def type(self):
        return TokenType.Function

class Constant(Enum):
    # Value = 0 # can be any constant value in an expression
    E = math.e
    Pi = math.pi
    Inf = math.inf

    @property
    def type(self):
        return TokenType.Constant

class Variable(IntEnum):
    Constant = 0 # numeric constant
    Alpha    = 1 # letter variable

    @property
    def type(self):
        return TokenType.Value

class Prefix(Enum):
    Positive = 1
    Negative = -1

SYMBOLS = {
    "+": Operator.Add,
    "-": Operator.Subtract,
    "*": Operator.Multiply,
    "/": Operator.Divide,
    "(": Operator.LeftParen,
    ")": Operator.RightParen,
    "^": Operator.Power,
    "=": Operator.Equals,
    "<": Operator.LessThan,
    ">": Operator.MoreThan,

    "sin": Function.Sin,
    "cos": Function.Cos,
    "tan": Function.Tan,
    "log": Function.Log,
    "ln":  Function.Ln,

    "e":   Constant.E,
    "pi":  Constant.Pi,
    "inf": Constant.Inf
}

class Token:

    def __init__(self, token_value, symbol_type):
        self._token_value = token_value
        self._symbol_type = symbol_type

    @property
    def symbol(self):
        return self._token_value

    @property
    def token(self):
        return self._symbol_type

    @property
    def foo(self):
        return self._foo
    
    def type(self):
        return self._symbol_type.type

class Expression:
    def __init__(self, tokens):
        self.tokens = tokens
        self.experssions = []

    def evaluate(self):
        output = 0
        for expr in self.expressions:
            output += expr.evaluate()
        return output

class Parser:

    def __init__(self, expr_string):
        self.tokens = Lexer(expr_string).get_tokens()
        self.experssions = []
        self.token_idx = 0
        self.stack = []

    def next(self):
        if not self.can_read():
            raise IndexError("Token index out of range.")
        token = self.tokens[self.token_idx]
        self.token_idx += 1
        return token

    def peak(self):
        if not self.can_read():
            raise IndexError("Token index out of range.")
        return self.tokens[self.token_idx]

    def can_read(self):
        return self.token_idx + 1 < len(self.tokens)

    def expect(self, token_type):
        token = self.peak()
        if token.token == token_type:
            self.next()
            return True
        raise ParseError("Expected token '{0}' at index: {1}, got {2}"
            .format(str(token_type), str(self.token_idx - 1), str(token.token)))

    def parse(self):
        """Turn tokens into expressions"""

        while self.can_read():
            token = self.next()


        return self.tokens

    def evaluate(self):
        """Evaluate expressions into output"""
        pass

class ParseError(Exception):
    pass

class TokenError(Exception):
    pass

class Lexer:

    def __init__(self, expr_string):
        self.reader = StringReader(expr_string)
        self.tokens = []

    def get_tokens(self):

        # to the end of the string, do something
        while self.reader.pos != self.reader.length:
            # if there are whitespace, skip it
            if self.reader.peak() == " ":
                self.reader.skip_whitespace()
            char = self.reader.next()

            # if the character is in the symbols dictionary
            # we add the it to the list of tokens
            if char in SYMBOLS:
                token = Token(char, SYMBOLS[char])
                self.tokens.append(token)
                continue
            else:
                match = False
                # test for function symbols with a length of 3
                if self.reader.pos + 2 <= self.reader.length:
                    symbol = char + self.reader.peak(2)
                    if symbol in SYMBOLS:
                        token = Token(symbol, SYMBOLS[symbol])
                        self.tokens.append(token)
                        self.reader.read(2)
                        match = True
                # if there were no match for 3 lettered function
                # names, we check for two lettered function names
                elif self.reader.pos + 1 <= self.reader.length and not match:
                    symbol = char + self.reader.peak()
                    if symbol in SYMBOLS:
                        token = Token(symbol, SYMBOLS[symbol])
                        self.tokens.append(token)
                        self.reader.read(1)
                        match = True
                # if there were no match at all, we just move
                # on to treat the character as a constant or variable
                if match:
                    continue

            # handle numeric constants e.g.: number 2
            if char.isnumeric():
                num = char
                # check if it's a bigger number
                # which can also de decimal
                while self.reader.pos != self.reader.length:
                    c = self.reader.peak()
                    if not c.isnumeric() and c != ".":
                        break
                    num += c
                    self.reader.next()
                token = Token(num, Variable.Constant)
                self.tokens.append(token)
            # handle variables e.g.: x
            elif char.isalpha():
                token = Token(char, Variable.Alpha)
                self.tokens.append(token)
            else:
                # token is undefined or not valid?
                dbg = "\'{0}\' index: {1}".format(char, str(self.reader.pos - 1))
                raise TokenError("Token was not valid or defined: \n{}".format(dbg))

        return self.tokens


class StringReader:

    def __init__(self, string):
        self.string = string
        self.idx = 0

    def next(self):
        if self.idx + 1 > len(self.string):
            raise IndexError("String index is out of range.")
        char = self.string[self.idx:self.idx + 1]
        self.idx += 1
        return char

    def peak(self, n=1):
        if self.idx + n > len(self.string):
            raise IndexError("String index is out of range.")
        return self.string[self.idx:self.idx + n]

    def read(self, n):
        if self.idx + n > len(self.string):
            raise IndexError("String index is out of range.")
        char = self.string[self.idx:self.idx + n]
        self.idx += n
        return char

    def read_until(self, c):
        if len(c) != 1:
            raise AttributeError("Argument can only be one character.")
        ret = ""
        while self.idx + 1 <= len(self.string):
            char = self.next()
            ret += char
            if char == c:
                return ret
        return ret

    def skip_whitespace(self):
        while self.idx + 1 <= len(self.string):
            peak_char = self.peak()
            if peak_char != " ":
                break
            self.idx += 1

    @property
    def pos(self):
        return self.idx

    @pos.setter
    def pos(self, value):
        if value < 0 or value >= len(self.string):
            raise IndexError("Position index is out of range.")
        self.idx = value

    @property
    def length(self):
        return len(self.string)
