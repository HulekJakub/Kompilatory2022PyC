import ply.lex as lex
import ply.yacc as yacc
from lexer import *

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
    #'unsigned': 'UNSIGNED',
    #'switch': 'SWITCH',
    'return': 'RETURN',
    'else': 'ELSE',
    'break': 'BREAK',
    #'case': 'CASE',
    #'default': 'DEFAULT',
    'const': 'CONST',
    'printf': 'PRINTF',
    'scanf': 'SCANF',
    'false': 'FALSE',
    'true': 'TRUE'
}
tokens += tuple(reserved.values())

# Token definitions

def t_PREPROCESSOR_LINE(t):
    r'\#[^\n]*'
    t.lexer.lineno += t.value.count("\n")
    #t.value = t.value[1:]

    t.value = t.value + "\n"
    return t


def t_COMMENT(t):
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



def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_DECIMAL(t):
    r'\d+\.\d+'
    #t.value = float(t.value)
    return t


def t_INTEGER(t):
    r'\d+'
    #t.value = int(t.value)
    return t


def t_CHARACTER(t):
    r'\'.\''
    #t.value = "\"" + t.value[1:-1] + "\""
    return t


def t_STRING(t):
    r'".*"'
    #t.value = t.value[1:-1]
    return t




# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Funkcje pomocnicze

INDENT = "    "

def indent_text(text):
    text = INDENT + text
    newlines = text.count("\n")
    text = text.replace("\n", "\n" + INDENT, newlines-1)
    return text

# PROGRAM


precedence = (
     ('nonassoc', 'EQUAL', 'NOT_EQUAL', 'GREATER_EQUAL', 'LESSER_EQUAL', 'GREATER', 'LESSER'),  # Nonassociative operators
     ('left', 'PLUS', 'MINUS'),
     ('left', 'MUL', 'DIV'),
     ('right', 'UMINUS'),            # Unary minus operator
 )

start = "s_prim"


def p_s_prim(t):
    '''s_prim : program'''
    t[0] = t[1] + "if __name__ == \"__main__\":\n" + INDENT + "main()"


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
    '''statement : any_statement
                 | COMMENT
                 | SEMICOLON'''
    if t[1] == ";":
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
                     | do_while_loop_statement
                     | break_statement
                     | for_loop_statement
                     | if_statement opt_else_if_statements opt_else_statement
                     | print_statement
                     | scan_statement'''
    if len(t) == 4:
        t[0] = t[1] + t[2] + t[3]
    else:
        t[0] = t[1]


def p_declaration_statement(t):
    '''declaration_statement : opt_const type ID opt_array_mark
                             | opt_const type ID opt_array_mark ASSIGN declaration_value_expression SEMICOLON'''
    dec_type = ""
    if t[2] in ["int", "float", "bool", "str"]:
        dec_type = t[2]+"()"

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
            dec_assign = " = " + t[6]
        else:
            dec_assign = " = " + t[6]

    t[0] = t[3] + dec_assign + "\n"


def p_assign_statement(t):
    '''assign_statement :  assign_expression SEMICOLON'''
    print("assign")
    t[0] = t[1] + "\n"


def p_function_statement(t):
    '''function_statement  : function_expression SEMICOLON'''
    t[0] = t[1] + "\n"


def p_return_statement(t):
    '''return_statement : RETURN value_expression SEMICOLON'''
    t[0] = "return " + t[2] + "\n"


def p_break_statement(t):
    '''break_statement : BREAK SEMICOLON'''
    t[0] = "break" + "\n"


def p_function_definition_statement(t):
    '''function_definition_statement : type ID L_BRACKET opt_args R_BRACKET statements_block'''
    
    t[0] = "def " + t[2] + "(" + t[4] + ")" + t[6] + "\n"


def p_while_loop_statement(t):
    '''while_loop_statement : WHILE L_BRACKET logical_expression R_BRACKET statements_block'''
    t[0] = "while" + "(" + t[3] + ")" + t[5]


def p_do_while_loop_statement(p):
    '''do_while_loop_statement : DO statements_block WHILE L_BRACKET logical_expression  R_BRACKET SEMICOLON'''
    preparation = "do_while_loop_first_pass = True\n"
    body = "while(" + preparation + " or (" + p[5] + "))" + p[2]
    end = INDENT + "do_while_loop_first_pass = False\n"
    p[0] = preparation + body + end


def p_for_loop_statement(p):
    '''for_loop_statement : FOR L_BRACKET decl_stat_or_sem opt_logical_expression SEMICOLON opt_assign_expression R_BRACKET statements_block'''
    condition = p[4]
    if condition == "":
        condition = "True"

    preparation = p[3]
    body = "while(" + condition + ")" + p[8]
    end = INDENT + p[6] + "\n"
    p[0] = preparation + body + end


def p_decl_stat_or_sem(t):
    '''decl_stat_or_sem : declaration_statement
                        | SEMICOLON'''
    if t[1] == t_SEMICOLON:
        t[0] = ""
    else:
        t[0] = t[1]


def p_if_statement(p):
    '''if_statement : IF L_BRACKET logical_expression R_BRACKET statements_block'''

    p[0] = "if" + " " + p[3]   + p[5]

def p_else_statement(p):
    '''else_statement : ELSE statements_block '''

    p[0] = "else" + p[2]

def p_else_if_statement(p):
    '''else_if_statement : ELSE IF L_BRACKET logical_expression R_BRACKET statements_block'''

    p[0] = "elif" + " " + p[4] + p[6]


def p_else_if_statements(p):
    '''else_if_statements : else_if_statement
                          | else_if_statement else_if_statements'''

    if len(p) == 3:
        p[0] = p[1] + p[2]

    elif len(p) == 2:
        p[0] = p[1]


def p_opt_else_statement(p):
    '''opt_else_statement : else_statement
                          | empty'''
    p[0] = p[1]


def p_opt_else_if_statements(p):
    '''opt_else_if_statements : else_if_statements
                              | empty'''

    p[0] = p[1]


def p_print_statement(p):
    '''print_statement : PRINTF L_BRACKET value_expression R_BRACKET'''
    p[0] = "print" + "(" + p[3] + ")" + "\n"


def p_scan_statement(p):
    '''scan_statement : SCANF L_BRACKET AMPERSAND ID  R_BRACKET'''
    p[0] = p[4] + " = " + "input" + "()" + "\n"

# EXPRESSIONS


def p_declaration_value_expression(p):
    '''declaration_value_expression : value_expression
                                    | L_BRACE listed_values R_BRACE
                                    | L_BRACE declaration_value_expression R_BRACE'''
    if len(p) == 2:
        p[0] = p[1]

    elif len(p) == 4:
        p[0] = "[" + p[2] + "]"


def p_value_expression(p):
    '''value_expression : math_expression
                        | function_expression
                        | value
                        | trinary_mark_expression
                        | L_BRACKET value_expression R_BRACKET'''

    if len(p) == 2:
        p[0] = p[1]

    else:
        p[0] = "(" + p[2] + ")"


def p_opt_value_expression(p):
    '''opt_value_expression : value_expression
                            | empty'''

    p[0] = p[1]


def p_math_expression(p):
    '''math_expression : L_BRACKET math_expression R_BRACKET
                       | MINUS math_expression %prec UMINUS
                       | MINUS value %prec UMINUS
                       | value math_op value'''

    if len(p) == 2:
        p[0] = p[1]

    elif len(p) == 3:
        p[0] = "-" + p[2]

    elif len(p) == 4 and p[1] == "(":
        p[0] = "(" + p[2] + ")"

    elif len(p) == 4:
        p[0] = f"{p[1]} {p[2]} {p[3]}"


def p_logical_expression(p):
    '''logical_expression : logical_expression bool_op logical_expression
                          | NEGATION logical_expression
                          | value_expression comparison_op value_expression'''

    if len(p) == 2:
        p[0] = p[1]

    elif len(p) == 3:
        p[0] = "not " + p[2]

    elif len(p) == 4:
        p[0] = p[1] + " " + p[2] + " " + p[3]


def p_function_expression(p):
    '''function_expression : ID L_BRACKET opt_listed_values R_BRACKET'''
    p[0] = p[1] + "(" + p[3] + ")"


def p_trinary_mark_expression(p):
    '''trinary_mark_expression : logical_expression QUESTION_MARK value_expression COLON value_expression'''

    p[0] = "(" + p[5] + "," + p[3] + ")""[int(" + p[1] + ")]"


def p_assign_expression(p):
    '''assign_expression : ID assign_op value_expression
                         | unary_op ID
                         | ID unary_op'''
    print("assign_exp")
    if len(p) == 3:
        if p[1] == "-" or p[1] == "+":
            p[0] = p[2] + p[1] + "=" + " 1"
        else:
            p[0] = p[1] + p[2] + "=" + " 1"
    else:
        p[0] = p[1] + p[2] + p[3]


def p_opt_logical_expression(p):
    '''opt_logical_expression : logical_expression
                              | empty'''

    p[0] = p[1]


def p_opt_assign_expression(p):
    '''opt_assign_expression : assign_expression
                             | empty'''

    p[0] = p[1]

# DEFINITIONS


def p_type(p):
    '''type : INT
            | FLOAT
            | DOUBLE
            | CHAR
            | BOOL
            | LONG
            | VOID'''
    py_type = ""
    if p[1] == "int":
        py_type = "int"
    if p[1] == "float":
        py_type = "float"
    if p[1] == "double":
        py_type = "float"
    if p[1] == "char":
        py_type = "str"
    if p[1] == "bool":
        py_type = "bool"
    if p[1] == "long":
        py_type = "int"
    if p[1] == "void":
        py_type = ""
    p[0] = py_type


def p_value(p):
    '''value : INTEGER
             | DECIMAL
             | CHARACTER
             | STRING
             | TRUE
             | FALSE
             | ID
             | ID L_SQUARE_BRACKET value_expression  R_SQUARE_BRACKET'''

    if len(p) == 2:
        if p[1] == "true":
            p[0] = 'True'

        elif p[1] == "false":
            p[0] = "False"
        else:
            p[0] = p[1]

    else:
        p[0] = p[1] + "[" + p[3] + "]"


def p_listed_values(p):
    '''listed_values : value_expression COMMA value_expression
                     | value_expression COMMA listed_values'''
    print(f"listing values cur:{p}")
    if len(p) == 2:
        p[0] = p[1]

    else:
        p[0] = p[1] + ", " + p[3]


def p_math_op(p):
    '''math_op : PLUS
               | MINUS
               | MUL
               | DIV
               | MOD'''

    p[0] = p[1]


def p_unary_op(p):
    '''unary_op : INCREMENT
                | DECREMENT'''
    p[0] = p[1][0]


def p_bool_op(p):
    '''bool_op : AND
               | OR'''

    if p[1] == '&&':
        p[0] = "and"

    elif p[1] == '||':
        p[0] = 'or'


def p_comparison_op(p):
    '''comparison_op : EQUAL
                     | NOT_EQUAL
                     | GREATER
                     | GREATER_EQUAL
                     | LESSER
                     | LESSER_EQUAL'''

    p[0] = p[1]


def p_assign_op(p):
    '''assign_op : ASSIGN
                 | PLUS_ASSIGN
                 | MINUS_ASSIGN
                 | MUL_ASSIGN
                 | DIV_ASSIGN
                 | MOD_ASSIGN'''

    p[0] = p[1]


def p_array_mark(p):
    '''array_mark : L_SQUARE_BRACKET opt_value_expression  R_SQUARE_BRACKET '''

    p[0] = "[" + p[2] + "]"


def p_opt_const(p):
    '''opt_const : CONST
                 | empty'''
    p[0] = p[1]


def p_opt_array_mark(p):
    '''opt_array_mark : array_mark
                      | empty'''

    p[0] = p[1]


def p_opt_listed_values(p):
    '''opt_listed_values :  listed_values
                         | empty'''

    p[0] = p[1]


def p_args(p):
    '''args : type ID
            | type ID COMMA args'''

    arg = p[2] + ": " + p[1]
    if len(p) == 3:
        p[0] = arg
    else:
        p[0] = arg + ", " + p[4]


def p_opt_args(p):
    '''opt_args : args
                | empty'''

    p[0] = p[1]


def p_empty(p):
    '''empty : '''
    p[0] = ""

# Errors


def p_error(p):

    if not p:
        print("End of File!")
        return ""
    print("Whoa. You are seriously hosed at line", p.lineno, " token ", p)
    # Read ahead looking for a closing '}'
    while True:
        tok = parser.token()  # Get the next token
        if not tok or tok.type == 'R_BRACE' or tok.type == 'SEMICOLON':
            break
    parser.restart()
    parser.errok()
    return ""


lexer = lex.lex()
parser = yacc.yacc()


def main():
    with open("source.c", "r") as f:
        while True:
            try:
                s = f.read()
            except EOFError:
                break
            if not s: continue
            result = parser.parse(s)
            # token = lexer.token()
            # print(token)
            # while token is not None:
            #     token = lexer.token()
            #     print(token)
            print(result)
            with open("converted.py", "w") as out_f:
                out_f.write(result)
                break



if __name__ == "__main__":
    main()
