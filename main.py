import sys
from parserPyC import *

def main():
    lexer = PyCLexer()
    parser = PyCParser(lexer)

    lexer = lexer.lexer
    parser = parser.parser
    try:
        with open("source.c", "r") as f:
            file_body = f.read()
            file_tokens = list()
            lexer.input(file_body)
            token = lexer.token()
            while token is not None:
                file_tokens.append(str(token))
                token = lexer.token()
            with open("read_tokens.txt", "w") as out_f:
                print("aha")
                out_f.write("\n".join(file_tokens))

        with open("source.c", "r") as f:
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

