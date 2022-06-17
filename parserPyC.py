from lexerPyC import *
import ply.yacc as yacc


class PyCParser:
    def __init__(self, lexer):
        self.parser = yacc.yacc(module=self)
        self.lexer = lexer

    tokens = PyCLexer.tokens

    # Flagi
    main_function_declared = False

    # Funkcje pomocnicze

    INDENT = "    "

    def indent_text(self, text):
        text = self.INDENT + text
        newlines = text.count("\n")
        text = text.replace("\n", "\n" + self.INDENT, newlines - 1)
        return text

    # PROGRAM

    precedence = (
        ('nonassoc', 'EQUAL', 'NOT_EQUAL', 'GREATER_EQUAL', 'LESSER_EQUAL', 'GREATER', 'LESSER'),
        # Nonassociative operators
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MUL', 'DIV'),
        ('right', 'UMINUS'),  # Unary minus operator
        ('nonassoc', 'ELSE_IF_WORSE'),
        ('nonassoc', 'ELSE_BETTER'),
        ('nonassoc', 'ELEMENT_EXTRACTION_FIRST'),
        # ('nonassoc', 'SHORTER_LAST'),
        # ('nonassoc', 'LONGER_FIRST')
    )

    start = "s_prim"

    def p_s_prim(self, p):
        '''s_prim : program'''
        if self.main_function_declared:
            p[0] = p[1] + "if __name__ == \"__main__\":\n" + self.INDENT + "main()"
        else:
            p[0] = p[1]


    def p_program(self, p):
        '''program : program_component
                   | program_component program'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            p[0] = p[1] + p[2]

    def p_program_component(self, p):
        '''program_component : declaration_statement
                             | function_definition_statement
                             | COMMENT
                             | PREPROCESSOR_LINE'''
        p[0] = p[1]

    # STATEMENTS

    def p_statement(self, p):
        '''statement : any_statement
                     | COMMENT
                     | SEMICOLON'''
        if p[1] == ";":
            p[0] = ""
        else:
            p[0] = p[1]

    def p_statements(self, p):
        '''statements : statement
                      | statement statements'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            p[0] = p[1] + p[2]

    def p_opt_statements(self, p):
        '''opt_statements : statements
                          | empty'''
        p[0] = p[1]

    def p_statements_block(self, p):
        '''statements_block : L_BRACE opt_statements R_BRACE'''
        p[0] = ":" + "\n" + self.indent_text(p[2]) + "\n"

    def p_any_statement(self, p):
        '''any_statement : declaration_statement
                         | assign_statement
                         | function_statement
                         | return_statement
                         | while_loop_statement
                         | do_while_loop_statement
                         | break_statement
                         | for_loop_statement
                         | if_statement_block
                         | print_statement
                         | scan_statement
                         '''

        p[0] = p[1]

    def p_declaration_statement(self, p):
        '''declaration_statement : opt_const type ID opt_array_mark
                                 | opt_const type ID opt_array_mark ASSIGN declaration_value_expression SEMICOLON'''
        dec_type = ""
        if p[2] in ["int", "float", "bool", "str"]:
            dec_type = p[2] + "()"

        dec_assign = ""
        if len(p) == 5:
            if p[4] != "":
                if dec_type != "":
                    dec_assign = " = " + "[" + dec_type + "]" + " * " "(" + p[4][1:-1] + ")"
                else:
                    dec_assign = " = " + "[None]" + " * " "(" + p[4][1:-1] + ")"
            else:
                if dec_type != "":
                    dec_assign = " = " + dec_type
                else:
                    dec_assign = " = 0"
        else:
            if p[4] != "":
                dec_assign = " = " + p[6]
            else:
                dec_assign = " = " + p[6]

        p[0] = p[3] + dec_assign + "\n"

    def p_assign_statement(self, p):
        '''assign_statement :  assign_expression SEMICOLON'''
        p[0] = p[1] + "\n"

    def p_function_statement(self, p):
        '''function_statement  : function_expression SEMICOLON'''
        p[0] = p[1] + "\n"

    def p_return_statement(self, p):
        '''return_statement : RETURN value_expression SEMICOLON'''
        p[0] = "return " + p[2] + "\n"

    def p_break_statement(self, p):
        '''break_statement : BREAK SEMICOLON'''
        p[0] = "break" + "\n"

    def p_function_definition_statement(self, p):
        '''function_definition_statement : type ID L_BRACKET opt_args R_BRACKET statements_block'''
        if p[2] == "main":
            self.main_function_declared = True
        p[0] = "def " + p[2] + "(" + p[4] + ")" + p[6] + "\n"

    def p_while_loop_statement(self, p):
        '''while_loop_statement : WHILE L_BRACKET logical_expression R_BRACKET statements_block'''
        p[0] = "while" + " " + p[3] + p[5]

    def p_do_while_loop_statement(self, p):
        '''do_while_loop_statement : DO statements_block WHILE L_BRACKET logical_expression  R_BRACKET SEMICOLON'''

        p[0] = "while True" + p[2] + self.INDENT + "if " + p[5] + ":\n" + 2 * self.INDENT + "break\n"

    def p_for_loop_statement(self, p):
        '''for_loop_statement : FOR L_BRACKET decl_stat_or_sem opt_logical_expression SEMICOLON opt_assign_expression R_BRACKET statements_block'''
        condition = p[4]
        if condition == "":
            condition = "True"

        preparation = p[3]
        body = "while(" + condition + ")" + p[8]
        end = self.INDENT + p[6] + "\n"
        p[0] = preparation + body + end

    def p_decl_stat_or_sem(self, t):
        '''decl_stat_or_sem : declaration_statement
                            | SEMICOLON'''
        if t[1] == ";":
            t[0] = ""
        else:
            t[0] = t[1]

    def p_if_statement_block(self, p):
        '''if_statement_block : if_statement
                              | if_statement else_else_if_statements_block'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            p[0] = p[1] + p[2]

    def p_if_statement(self, p):
        '''if_statement : IF L_BRACKET logical_expression R_BRACKET statements_block
                        | IF L_BRACKET value_expression R_BRACKET statements_block'''

        p[0] = "if" + " " + p[3] + p[5]

    def p_else_else_if_statements_block(self, p):
        '''else_else_if_statements_block : else_statement
                                         | else_if_statement else_else_if_statements_block %prec ELSE_BETTER
                                         | else_if_statement  %prec ELSE_IF_WORSE'''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            p[0] = p[1] + p[2]

    def p_else_statement(self, p):
        '''else_statement : ELSE statements_block '''

        p[0] = "else" + p[2]


    def p_else_if_statement(self, p):
        '''else_if_statement : ELSE if_statement'''

        p[0] = "el" + p[2]


    def p_print_statement(self, p):
        '''print_statement : PRINTF L_BRACKET value_expression R_BRACKET'''
        p[0] = "print" + "(" + p[3] + ")" + "\n"

    def p_scan_statement(self, p):
        '''scan_statement : SCANF L_BRACKET AMPERSAND ID  R_BRACKET'''
        p[0] = p[4] + " = " + "input" + "()" + "\n"

    # EXPRESSIONS

    def p_declaration_value_expression(self, p):
        '''declaration_value_expression : value_expression
                                        | L_BRACE listed_values R_BRACE
                                        | L_BRACE declaration_value_expression R_BRACE'''
        if len(p) == 2:
            p[0] = p[1]

        elif len(p) == 4:
            p[0] = "[" + p[2] + "]"

    def p_value_expression(self, p):
        '''value_expression : math_expression
                            | function_expression
                            | value
                            | trinary_mark_expression
                            | L_BRACKET value_expression R_BRACKET'''

        if len(p) == 2:
            p[0] = p[1]

        else:
            p[0] = "(" + p[2] + ")"

    def p_opt_value_expression(self, p):
        '''opt_value_expression : value_expression
                                | empty'''

        p[0] = p[1]

    def p_math_expression(self, p):
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

    def p_logical_expression(self, p):
        '''logical_expression : logical_expression bool_op logical_expression
                              | NEGATION logical_expression
                              | value_expression comparison_op value_expression
                              | L_BRACKET logical_expression R_BRACKET'''

        if len(p) == 2:
            p[0] = p[1]

        elif len(p) == 3:
            p[0] = "not " + p[2]

        elif len(p) == 4 and p[1] == "(":
            p[0] = "(" + p[2] + ")"

        elif len(p) == 4:
            p[0] = p[1] + " " + p[2] + " " + p[3]

    def p_function_expression(self, p):
        '''function_expression : ID L_BRACKET opt_listed_values R_BRACKET'''
        p[0] = p[1] + "(" + p[3] + ")"

    def p_trinary_mark_expression(self, p):
        '''trinary_mark_expression : logical_expression QUESTION_MARK value_expression COLON value_expression'''

        p[0] = "(" + p[5] + "," + p[3] + ")""[int(" + p[1] + ")]"

    def p_assign_expression(self, p):
        '''assign_expression : ID assign_op value_expression
                             | list_element_extraction assign_op value_expression %prec ELEMENT_EXTRACTION_FIRST
                             | unary_op ID
                             | ID unary_op'''
        if len(p) == 3:
            if p[1] == "-" or p[1] == "+":
                p[0] = p[2] + " " + p[1] + "= " + " 1"
            else:
                p[0] = p[1] + " " + p[2] + "= " + " 1"
        elif len(p) == 4:
            p[0] = p[1] + " " + p[2] + " " + p[3]


    def p_opt_logical_expression(self, p):
        '''opt_logical_expression : logical_expression
                                  | empty'''

        p[0] = p[1]

    def p_opt_assign_expression(self, p):
        '''opt_assign_expression : assign_expression
                                 | empty'''

        p[0] = p[1]

    # DEFINITIONS

    def p_type(self, p):
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

    def p_value(self, p):
        '''value : INTEGER
                 | DECIMAL
                 | CHARACTER
                 | STRING
                 | TRUE
                 | FALSE
                 | ID
                 | list_element_extraction %prec ELEMENT_EXTRACTION_FIRST'''

        if len(p) == 2:
            if p[1] == "true":
                p[0] = 'True'

            elif p[1] == "false":
                p[0] = "False"
            else:
                p[0] = p[1]


    def p_list_element_extraction(self, p):
        '''list_element_extraction : ID L_SQUARE_BRACKET value_expression  R_SQUARE_BRACKET'''

        p[0] = p[1] + "[" + p[3] + "]"

    def p_listed_values(self, p):
        '''listed_values : value_expression COMMA value_expression
                         | value_expression COMMA listed_values'''
        if len(p) == 2:
            p[0] = p[1]

        else:
            p[0] = p[1] + ", " + p[3]

    def p_math_op(self, p):
        '''math_op : PLUS
                   | MINUS
                   | MUL
                   | DIV
                   | MOD'''

        p[0] = p[1]

    def p_unary_op(self, p):
        '''unary_op : INCREMENT
                    | DECREMENT'''
        p[0] = p[1][0]

    def p_bool_op(self, p):
        '''bool_op : AND
                   | OR'''

        if p[1] == '&&':
            p[0] = "and"

        elif p[1] == '||':
            p[0] = 'or'

    def p_comparison_op(self, p):
        '''comparison_op : EQUAL
                         | NOT_EQUAL
                         | GREATER
                         | GREATER_EQUAL
                         | LESSER
                         | LESSER_EQUAL'''

        p[0] = p[1]

    def p_assign_op(self, p):
        '''assign_op : ASSIGN
                     | PLUS_ASSIGN
                     | MINUS_ASSIGN
                     | MUL_ASSIGN
                     | DIV_ASSIGN
                     | MOD_ASSIGN'''

        p[0] = p[1]

    def p_array_mark(self, p):
        '''array_mark : L_SQUARE_BRACKET opt_value_expression  R_SQUARE_BRACKET '''

        p[0] = "[" + p[2] + "]"

    def p_opt_const(self, p):
        '''opt_const : CONST
                     | empty'''
        p[0] = p[1]

    def p_opt_array_mark(self, p):
        '''opt_array_mark : array_mark
                          | empty'''

        p[0] = p[1]

    def p_opt_listed_values(self, p):
        '''opt_listed_values :  listed_values
                             | empty'''

        p[0] = p[1]

    def p_args(self, p):
        '''args : type ID
                | type ID COMMA args'''

        arg = p[2] + ": " + p[1]
        if len(p) == 3:
            p[0] = arg
        else:
            p[0] = arg + ", " + p[4]

    def p_opt_args(self, p):
        '''opt_args : args
                    | empty'''

        p[0] = p[1]

    def p_empty(self, p):
        '''empty : '''
        p[0] = ""

    # Errors

    def p_error(self, p):
        print(f"Syntax error at line {p.lineno}.")
        if not p:
            print("End of File!")
            return ""
        print("Whoa. You are seriously hosed at line", p.lineno, " token ", p, "\nterminating...")
        # Read ahead looking for a closing '}'
        while True:
            tok = self.parser.token()  # Get the next token
            if not tok or tok.type == 'R_BRACE' or tok.type == 'SEMICOLON':
                break

        return ""
