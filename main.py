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
    r'(\/\/[^\n]*)|(\/\*(.|\n)*\*\/)'
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
'''s_prim : program'''

'''program : program_component | program_component program'''

'''program_component : declaration_statement
           | function_definition_statement'''

# STATEMENTS
'''statement : any_statement | SEMICOLON'''

'''statements : statement 
              | statement statements'''

'''opt_statements : statements 
                  | empty'''

'''any_statement : declaration_statement 
                 | assign_statement 
                 | function_statement 
                 | return_statement 
                 | while_loop_statement 
                 | for_loop_statement
                 | switch_statement 
                 | if_statement opt_else_if_statements opt_else_statement'''

'''declaration_statement : opt_const type ID opt_array_mark ASSIGN declaration_expression SEMICOLON'''

'''assign_statement : assign_expression SEMICOLON'''

'''function_statement  : function_expression SEMICOLON'''

'''return_statement : RETURN value_expression SEMICOLON'''

'''break_statement : BREAK SEMICOLON'''

'''function_definition_statement : type ID L_BRACKET opt_args R_BRACKET L_BRACE statements R_BRACE'''

'''while_loop_statement : WHILE L_BRACKET logical_expression R_BRACKET L_BRACE opt_statements R_BRACE'''

'''do_while_loop_statement : DO L_BRACE opt_statements R_BRACE 
                                WHILE L_BRACKET logical_expression  R_BRACKET SEMICOLON'''

'''for_loop_statement : FOR L_BRACKET decl_stat_or_sem opt_logical_expression SEMICOLON opt_assign_expression R_BRACKET 
                            L_BRACE opt_statements R_BRACE'''

'''decl_stat_or_sem : declaration_statement 
                    | SEMICOLON'''

'''switch_statement : SWITCH L_BRACKET value_expression R_BRACKET 
                        L_BRACE opt_case_statements opt_default_statement opt_case_statements  R_BRACE'''

'''opt_case_statements : case_statement
                       | case_statement opt_case_statements
                       | empty'''

'''opt_default_statement : DEFAULT COLON opt_statements opt_break_statement'''

'''opt_break_statement : break_statement 
                       | empty'''

'''case_statement : CASE value_expression COLON opt_statements opt_break_statement'''

'''if_statement : IF L_BRACKET logical_expression R_BRACKET L_BRACE opt_statements R_BRACE'''

'''else_if_statement : ELSE IF L_BRACKET logical_expression R_BRACKET L_BRACE opt_statements R_BRACE'''

'''else_if_statements : else_if_statement  
                      | else_if_statement else_if_statements'''

'''opt_else_if_statements : else_if_statements
                          | empty'''

'''else_statement : ELSE L_BRACE opt_statements R_BRACE'''

'''opt_else_statement : else_statement 
                      | empty'''

# EXPRESSIONS
'''declaration_value_expression : value_expression 
                                | L_BRACE listed_values R_BRACE
                                | L_BRACE declaration_value_expression R_BRACE'''

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
'''type : INT 
        | FLOAT 
        | DOUBLE 
        | CHAR 
        | BOOL 
        | LONG 
        | VOID'''

'''value : INTEGER 
         | DECIMAL 
         | CHARACTER 
         | STRING 
         | ID 
         | ID L_SQUARE_BRACKET value_expression  R_SQUARE_BRACKET'''

'''listed_values : value_expression 
                 | listed_values COMMA listed_values'''

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

'''opt_args : args type ID 
            | empty'''

'''empty: '''


def main():
    lexer = lex.lex()
    # parser = yacc.yacc()
    while True:
        a = lexer.input(input('<<'))
        token = lexer.token()
        print(token)
        while token is not None:
            token = lexer.token()
            print(token)


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
