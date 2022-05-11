import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'L_BRACKET', 'R_BRACKET', 'L_BRACE', 'R_BRACE', 'L_SQUARE_BRACKET', 'R_SQUARE_BRACKET',
    'SEMICOLON', 'COLON', 'COMMA', 'QUESTION_MARK'  
    'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD',
    'INCREMENT', 'DECREMENT',
    'AND', 'OR', 'NEGATION'
    'EQUAL', 'NOT_EQUAL', 'GREATER', 'GREATER_EQUAL', 'LESSER', 'LESSER_EQUAL',
    'ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN'
    'ID', 'INTEGER', 'DECIMAL', 'CHARACTER', "STRING",
    "PREPROCESSOR_LINE", 'COMMENT'
)

# Tokens

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

t_PLUS = r'\+'
t_MINUS = r'-'
t_MUL = r'\*'
t_DIV = r'\/'
t_MOD = r'%'

t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'

t_AND = r'&&'
t_OR = r'\|\|'
t_NEGATION = r'!'

t_EQUAL = r'=='
t_NOT_EQUAL = r'!='
t_GREATER = r'>'
t_GREATER_EQUAL = r'>='
t_LESSER = r'<'
t_LESSER_EQUAL = r'<='
t_ASSIGN = r'='
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_MUL_ASSIGN = r'\*='
t_DIV_ASSIGN = r'\/='
t_MOD_ASSIGN = r'%='

t_ID = r'[a-zA-Z_][a-zA-zZ0-9_]*'

def t_INTEGER(t):
    '\d+'
    pass

def t_DECIMAL(t):
    '\d+\.\d+'
    pass

def t_CHARACTER(t):
    r'\'.\''
    pass

def t_STRING(t):
    r'".*"'
    pass

def t_PREPROCESSOR_LINE(t):
    r'\#[^\n]*'
    pass

def t_COMMENT(t):
    r'(\/\/[^\n]*)|(\/\*(.|\n)*\*\/)'
    pass

# keywords
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
    'unsigned': 'UNSIGNED',
    'switch': 'SWITCH',
    'return': 'RETURN',
    'else': 'ELSE',
    'break': 'BREAK',
    'case': 'CASE',
    'default': 'DEFAULT',
    'const': 'CONST',
    'printf': 'PRINTF',
    'scanf': 'SCANF',
    'false': 'FALSE',
    'true': 'TRUE'
}

tokens += list(reserved.values())
# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Parsing rules
# EXAMPLE TO DELETE
"""
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}


def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]


def p_statement_expr(t):
    'statement : expression'
    print(t[1])


def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]


def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]


def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]


def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0


def p_error(t):
    print("Syntax error at '%s'" % t.value)
"""


def main():
    lexer = lex.lex()
    parser = yacc.yacc()

    while True:
        try:
            s = input('calc > ')  # Use raw_input on Python 2
        except EOFError:
            break
        parser.parse(s)


if __name__ == "__main__":
    main()
