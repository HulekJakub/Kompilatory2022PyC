import sys
import os
from parserPyC import *


def main():
    for file_name in sys.argv[1:]:
        print(file_name)
        lexer = PyCLexer()
        parser = PyCParser(lexer)

        lexer = lexer.lexer
        parser = parser.parser
        try:
            """debug lexer tokens
            with open(file_name, "r") as f:
                file_body = f.read()
                file_tokens = list()
                lexer.input(file_body)
                token = lexer.token()
                while token is not None:
                    file_tokens.append(str(token))
                    token = lexer.token()
                with open(os.path.join("outputs", file_name.split(".")[0] + "_read_tokens.txt"), "w") as out_f:
                    out_f.write("\n".join(file_tokens))
                lexer.lineno = 1
            """
            with open(file_name, "r") as f:
                file_body = f.read()
                result = parser.parse(file_body)
                print(result)
                if result is not None:
                    with open(os.path.join("outputs", file_name.split(".")[0] + ".py"), "w") as out_f:
                        out_f.write(result)

        except IndexError as a:
            print(a)
            print(f"File path not added")

        except FileNotFoundError:
            print(f"File {file_name} could not have been read.")

if __name__ == "__main__":
    main()

