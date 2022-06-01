import ply.lex as lex
import ply.yacc as yacc

# Tokens
tokens = (
    'L_BRACKET', 'R_BRACKET', 'L_BRACE', 'R_BRACE', 'L_SQUARE_BRACKET', 'R_SQUARE_BRACKET',
    'SEMICOLON', 'COLON', 'COMMA', 'QUESTION_MARK',
    'INCREMENT', 'DECREMENT',
    'AND', 'OR', 'NEGATION',
    'EQUAL', 'NOT_EQUAL', 'GREATER_EQUAL', 'LESSER_EQUAL', 'GREATER', 'LESSER',
    'PLUS_ASSIGN', 'MINUS_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN', 'ASSIGN',
    'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD',
    'ID', 'DECIMAL', 'INTEGER', 'CHARACTER', "STRING",
    "PREPROCESSOR_LINE", 'COMMENT'
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
tokens += tuple(reserved.values())

# Token definitions

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


def t_ID(t):
    r'[a-zA-Z_][a-zA-zZ0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_CHARACTER(t):
    r'\'.\''
    t.value = t.value[1:-1]
    return t


def t_STRING(t):
    r'".*"'
    t.value = t.value[1:-1]
    return t


def t_PREPROCESSOR_LINE(t):
    r'\#[^\n]*'
    t.value = t.value[1:]
    return t


def t_COMMENT(t):
    r'(\/\/[^\n]*\n)|(\/\*(.|\n)*\*\/)'
    if (t.value[:2] == "//"):
        t.value = t.value[2:]
    else:
        t.value = t.value[2:-2]
    return t

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

# Tylko gramatyka w formacie Ply, brak działań
# PROGRAM
INDENT = "    "


def indent_text(text):
    text = INDENT + text
    newlines = text.count("\n")
    text = text.replace("\n", "\n" + INDENT, newlines-1)
    return text


def change_braces_to_brackets(text):
    change = True
    for i, c in enumerate(text):
        if c == "{" and change:
            text = text[:i] + '[' + text[i+1:]
        if c == "}" and change:
            text = text[:i] + ']' + text[i+1:]
        if c == "\"":
            change = not change

    return text


def p_s_prim(t):
    '''s_prim : program'''
    t[0] = t[1]
    print(t[0])



def p_program(t):
    '''program : program_component
               | program_component program'''
    if len(t) == 2:
        t[0] = t[1]
    elif len(t) == 3:
        t[0] = t[1] + t[2]


def p_program_component(t):
    '''program_component : declaration_statement
                         | function_definition_statement
                         | COMMENT
                         | PREPROCESSOR_LINE'''
    t[0] = t[1]

# STATEMENTS

def p_statement(t):
    '''statement : any_statement | COMMENT | SEMICOLON'''
    if t[1] == t_SEMICOLON:
        t[0] = ""
    else:
        t[0] = t[1]


def p_statements(t):
    '''statements : statement
                  | statement statements'''
    if len(t) == 2:
        t[0] = t[1]
    elif len(t) == 3:
        t[0] = t[1] + t[2]


def p_opt_statements(t):
    '''opt_statements : statements
                      | empty'''
    t[0] = t[1]


def p_statements_block(t):
    '''statements_block : L_BRACE opt_statements R_BRACE'''
    t[0] = ":" + "\n" + indent_text(t[2]) + "\n"


def p_any_statement(t):
    '''any_statement : declaration_statement
                     | assign_statement
                     | function_statement
                     | return_statement
                     | while_loop_statement
                     | for_loop_statement
                     | switch_statement
                     | if_statement opt_else_if_statements opt_else_statement
                     | print_statement'''
    if len(t) == 4:
        t[0] = t[1] + t[2] + t[3]
    else:
        t[0] = t[1]


def p_declaration_statement(t):
    '''declaration_statement : opt_const type ID opt_array_mark
                             | opt_const type ID opt_array_mark ASSIGN declaration_expression SEMICOLON'''
    dec_type = ""
    if t[2] == reserved["int"]:
        dec_type = "int()"
    if t[2] == reserved["float"]:
        dec_type = "float()"
    if t[2] == reserved["long"]:
        dec_type = "int()"
    if t[2] == reserved["double"]:
        dec_type = "float()"
    if t[2] == reserved["char"]:
        dec_type = "\"\""
    if t[2] == reserved["bool"]:
        dec_type = "bool()"
    if t[2] == reserved["void"]:
        dec_type = ""

    dec_assign = ""
    if len(t) == 5:
        if t[4] != "":
            if dec_type != "":
                dec_assign = " = " + "[" + dec_type + "]" + " * " "(" + t[4][1:-1] + ")"
            else:
                dec_assign = " = " + "[None]" + " * " "(" + t[4][1:-1] + ")"
        else:
            if dec_type != "":
                dec_assign = " = " + dec_type
            else:
                dec_assign = " = 0"
    else:
        if t[4] != "":
            dec_assign = " = " + change_braces_to_brackets(t[6])
        else:
            dec_assign = " = " + t[6]

    t[0] = t[3] + dec_assign + "\n"


def p_assign_statement(t):
    '''assign_statement : assign_expression SEMICOLON'''
    t[0] = t[1] + "\n"


def p_function_statement(t):
    '''function_statement  : function_expression SEMICOLON'''
    t[0] = t[1] + "\n"


def p_return_statement(t):
    '''return_statement : RETURN value_expression SEMICOLON'''
    t[0] = "return" + t[1] + "\n"


def p_break_statement(t):
    '''break_statement : BREAK SEMICOLON'''
    t[0] = "break" + "\n"


def p_function_definition_statement(t):
    '''function_definition_statement : type ID L_BRACKET opt_args R_BRACKET statements_block'''
    t[0] = "def " + t[2] + "(" + t[4] + ")" + t[6] + "\n"


def p_while_loop_statement(t):
    '''while_loop_statement : WHILE L_BRACKET logical_expression R_BRACKET statements_block'''
    t[0] = "while" + "(" + t[3] + ")" + t[5] + "\n"


def do_while_loop_statement(t):
    '''do_while_loop_statement : DO statements_block
                                WHILE L_BRACKET logical_expression  R_BRACKET SEMICOLON'''
    preparation = "do_while_loop_first_pass = True\n"
    body = "while(" + preparation + " or (" + t[5] + "))" + t[2]
    end = INDENT + "do_while_loop_first_pass = False\n"
    t[0] = preparation + body + end


def p_for_loop_statement(t):
    '''for_loop_statement : FOR L_BRACKET decl_stat_or_sem opt_logical_expression SEMICOLON opt_assign_expression R_BRACKET
                            statements_block'''
    condition = t[4]
    if condition == "":
        condition = "True"

    preparation = t[3]
    body = "while(" + condition + ")" + t[8]
    end = INDENT + t[6] + "\n"
    t[0] = preparation + body + end


def p_decl_stat_or_sem(t):
    '''decl_stat_or_sem : declaration_statement
                        | SEMICOLON'''
    if t[1] == t_SEMICOLON:
        t[0] = ""
    else:
        t[0] = t[1]

def p_if_statement(p):
    '''if_statement : IF L_BRACKET logical_expression R_BRACKET statements_block'''

    p[0] = "if" + "(" + p[3] + ")" + p[5]

def p_else_if_statement(p):
    '''else_if_statement : ELSE IF L_BRACKET logical_expression R_BRACKET statements_block'''

    p[0] = "elif" + "(" + p[4] + ")" + p[6]

def p_else_if_statements(p):
    '''else_if_statements : else_if_statement
                          | else_if_statement else_if_statements'''

    if len(p) == 3:
        p[0] = p[1] + p[2]

    elif len(p) == 2:
        p[0] = p[1]

def p_opt_else_if_statements(p):
    '''opt_else_if_statements : else_if_statements
                              | empty'''

    p[0] = p[1]

def p_else_statement(p):
    '''else_statement : ELSE statements_block'''

    p[0] = "else" + p[2]

def p_opt_else_statement(p):
    '''opt_else_statement : else_statement
                          | empty'''

    p[0] = p[1]

'''print_statement : PRINTF L_BRACKET value_expression R_BRACKET'''

'''scan_statement : SCANF L_BRACKET  R_BRACKET'''

# EXPRESSIONS
def p_declaration_value_expression(p):
    '''declaration_value_expression : value_expression
                                    | L_BRACE listed_values R_BRACE
                                    | L_BRACE declaration_value_expression R_BRACE'''
    if len(p) == 2:
        p[0] = p[1]

    elif len(p) == 4:
        p[0] = p[2]

'''value_expression : math_expression 
                    | logical_expression 
                    | function_expression
                    | value 
                    | trinary_mark_expression 
                    | L_BRACKET value_expression R_BRACKET'''

'''opt_value_expression : value_expression 
                        | empty'''

'''math_expression : math_expression math_op math_expression 
                   | MINUS math_expression 
                   | INTEGER 
                   | DECIMAL 
                   | CHARACTER 
                   | ID 
                   | L_BRACKET math_expression R_BRACKET'''

'''logical_expression : logical_expression bool_op logical_expression 
                      | TRUE  
                      | FALSE 
                      | NEGATION logical_expression  
                      | value_expression comparison_op value_expression 
                      | value_expression'''

'''function_expression: ID L_BRACKET opt_listed_values R_BRACKET'''

'''trinary_mark_expression : logical_expression Q_MARK value_expression COLON value_expression'''

'''assign_expression : ID assign_op value_expression 
                     | unary_op ID 
                     | ID unary_op'''

'''opt_logical_expression : logical_expression 
                          | empty'''

'''opt_assign_expression : assign_expression 
                         | empty'''

# DEFINITIONS

def p_type(p):
    '''type : INT
            | FLOAT
            | DOUBLE
            | CHAR
            | BOOL
            | LONG
            | VOID'''

    p[0] = p[1]

def p_value(p):
    '''value : INTEGER
             | DECIMAL
             | CHARACTER
            | STRING
            | ID
            | ID L_SQUARE_BRACKET value_expression  R_SQUARE_BRACKET'''

    if len(p) == 2:
        p[0] = p[1]

    else:
        p[0] = p[1] + "[" + p[3] + "]"

def p_listed_values(p):
    '''listed_values : value_expression
                     | listed_values COMMA listed_values'''

    if len(p) == 2:
        p[0] = p[1]

    else:
        p[0] = p[1] + "," + p[3]

'''math_op : PLUS 
           | MINUS 
           | MUL 
           | DIV 
           | MOD'''

'''unary_op : INCREMENT 
            | DECREMENT'''

'''bool_op : AND 
           | OR'''

'''comparsion_op : EQUAL 
                 | NOT_EQUAL
                 | GREATER 
                 | GREATER_EQUAL 
                 | LESSER 
                 | LESSER_EQUAL'''

'''assign_op : ASSIGN 
             | PLUS_ASSGIN 
             | MINUS_ASIGN 
             | MUL_ASSIGN 
             | DIV_ASSIGN 
             | MOD_ASSIGN'''

'''array_mark : L_SQUARE_BRACKET opt_value_expression  R_SQUARE_BRACKET '''

'''opt_const : CONST 
             | empty'''

'''opt_array_mark : array_mark 
                  | empty'''

'''opt_listed_values :  listed_values 
                     | empty'''

'''args : type ID
        | type ID COMMA args'''

def p_opt_args(p):
    '''opt_args : args type ID
                | empty'''


def p_empty(t):
    '''empty: '''
    t[0] = ""


def main():
    lexer = lex.lex()
    #parser = yacc.yacc()
    while True:
        try:
            a = lexer.input(input('<<'))
        except EOFError:
            break
        #parser.parse(a)

"""
    while True:
        try:
            s = input('calc > ')  # Use raw_input on Python 2
        except EOFError:
            break
        parser.parse(s)
"""

if __name__ == "__main__":
    main()
