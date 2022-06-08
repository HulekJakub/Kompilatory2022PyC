import ply.lex as lex

import ply.lex as lex
import ply.yacc as yacc
import sys
from ply.lex import TOKEN


class PyCLexer():

    # CONSTRUCTOR
    def __init__(self):
        print('Lexer constructor called.')
        self.lexer = lex.lex(module=self)

    # Tokens
    tokens = (
        "PREPROCESSOR_LINE", 'COMMENT',
        'L_BRACKET', 'R_BRACKET', 'L_BRACE', 'R_BRACE', 'L_SQUARE_BRACKET', 'R_SQUARE_BRACKET',
        'SEMICOLON', 'COLON', 'COMMA', 'QUESTION_MARK', 'AMPERSAND',
        'INCREMENT', 'DECREMENT',
        'AND', 'OR', 'NEGATION',
        'EQUAL', 'NOT_EQUAL', 'GREATER_EQUAL', 'LESSER_EQUAL', 'GREATER', 'LESSER',
        'PLUS_ASSIGN', 'MINUS_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN', 'ASSIGN',
        'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD',
        'ID', 'DECIMAL', 'INTEGER', 'CHARACTER', "STRING"

    )

    # Keywords
    reserved = {
        'int': 'INT',
        'float': 'FLOAT',
        'long': 'LONG',
        'double': 'DOUBLE',
        'char': 'CHAR',
        'bool': 'BOOL',
        'void': 'VOID',
        'if': 'IF',
        'for': 'FOR',
        'do': 'DO',
        'while': 'WHILE',
        'return': 'RETURN',
        'else': 'ELSE',
        'break': 'BREAK',
        'const': 'CONST',
        'printf': 'PRINTF',
        'scanf': 'SCANF',
        'false': 'FALSE',
        'true': 'TRUE'
    }
    tokens += tuple(reserved.values())

    # Token definitions

    def t_PREPROCESSOR_LINE(self, t):
        r'\#[^\n]*'
        t.lexer.lineno += t.value.count("\n")
        # t.value = t.value[1:]

        t.value = t.value + "\n"
        return t

    def t_COMMENT(self, t):
        r'(\/\/[^\n]*\n)|(\/\*(.|\n)*\*\/)'
        t.lexer.lineno += t.value.count("\n")
        if t.value[:2] == "//":
            t.value = "#" + t.value[2:]
        else:
            t.value = t.value[2:-2]
            t.value = "\"\"\"" + t.value + "\"\"\""
            t.value = t.value + "\n"
        return t

    t_L_BRACKET = r'\('
    t_R_BRACKET = r'\)'
    t_L_BRACE = r'\{'
    t_R_BRACE = r'\}'
    t_L_SQUARE_BRACKET = r'\['
    t_R_SQUARE_BRACKET = r'\]'

    t_SEMICOLON = r';'
    t_COLON = r':'
    t_COMMA = r','
    t_QUESTION_MARK = r'\?'
    t_AMPERSAND = r'&'

    t_INCREMENT = r'\+\+'
    t_DECREMENT = r'--'

    t_AND = r'&&'
    t_OR = r'\|\|'
    t_NEGATION = r'!'

    t_EQUAL = r'=='
    t_NOT_EQUAL = r'!='
    t_GREATER_EQUAL = r'>='
    t_LESSER_EQUAL = r'<='
    t_GREATER = r'>'
    t_LESSER = r'<'

    t_PLUS_ASSIGN = r'\+='
    t_MINUS_ASSIGN = r'-='
    t_MUL_ASSIGN = r'\*='
    t_DIV_ASSIGN = r'\/='
    t_MOD_ASSIGN = r'%='
    t_ASSIGN = r'='

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MUL = r'\*'
    t_DIV = r'\/'
    t_MOD = r'%'

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_DECIMAL(self, t):
        r'\d+\.\d+'
        # t.value = float(t.value)
        return t

    def t_INTEGER(self, t):
        r'\d+'
        # t.value = int(t.value)
        return t

    def t_CHARACTER(self, t):
        r'\'.\''
        # t.value = "\"" + t.value[1:-1] + "\""
        return t

    def t_STRING(self, t):
        r'".*"'
        # t.value = t.value[1:-1]
        return t

    # Ignored characters
    t_ignore = " \t"

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
