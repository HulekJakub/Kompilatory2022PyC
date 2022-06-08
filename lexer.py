import ply.lex as lex

import ply.lex as lex
import ply.yacc as yacc
import sys
from ply.lex import TOKEN


class Lexer():

    # CONSTRUCTOR
    def __init__(self):
        print('Lexer constructor called.')
        self.lexer = lex.lex(module=self)

