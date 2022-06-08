import sys

import ply.lex as lex
import ply.yacc as yacc
from lexerPyC import *
from parserPyC import *

def main():
    lexer = PyCLexer()
    parser = PyCParser(lexer)

    lexer = lexer.lexer
    parser = parser.parser
    try:
        with open(sys.argv[1], "r") as f:
            file_body = f.read()
            result = parser.parse(file_body)
            print(result)

            if result is not None:
                with open("converted.py", "w") as out_f:
                    out_f.write(result)

    except IndexError:
        print(f"File path not added")

    except FileNotFoundError:
        print(f"File {sys.argv[1]} could not have been read.")

if __name__ == "__main__":
    main()

