import ply.lex as lex
import ply.yacc as yacc
import argparse


# -------------------------
# Lexer
# -------------------------

# List of tokens
tokens = [
    'VARNAME',
    'NUMBER',
    'REGISTER',
    'OCTOTHORPE',
    'SEMICOLON',
    'EQUAL',
    'PLUS'
]

# Regular expression rules for simple tokens
t_OCTOTHORPE = r'\#'
t_SEMICOLON = r';'
t_EQUAL = r'='
t_PLUS = r'\+'

# Rule for varname
def t_VARNAME(token):
    r'[e-h]'
    return token

# Rule for numbers
def t_NUMBER(token):
    r'[0-9]'
    return token

# Rule for registers
def t_REGISTER(token):
    r'[A-D]'
    return token

# Ignored characters (spaces, tabs and linefeed)
t_ignore = ' \t\n'


# Error handling for illegal characters
def t_error(token):
    print(f"Illegal character '{token.value[0]}'")
    token.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# -------------------------
# Parser
# -------------------------

# Grammar rules
def p_program(p):
    '''program : statement SEMICOLON program 
               | empty'''

def p_statement(p):
    '''statement : normal_assignment 
                 | register_assignment'''

def p_normal_assignment(p):
    'normal_assignment : VARNAME EQUAL NUMBER'
    print(f"; {p[1]} = {p[3]}")
    print(f"MOV [{p[1]}], {p[3]}")

def p_register_assignment(p):
    'register_assignment : OCTOTHORPE REGISTER VARNAME EQUAL VARNAME PLUS VARNAME'
    print(f"; {p[3]} = {p[5]} + {p[7]}")
    print(f"MOV {p[2]}, [{p[5]}]")
    print(f"ADD {p[2]}, [{p[7]}]")
    print(f"MOV [{p[3]}], {p[2]}")

def p_empty(p):
    'empty :'
    pass


# Error rule for syntax errors
def p_error(p):
    print(f"Error: {p}")

# Build the parser
parser = yacc.yacc(debug=True) # Debug enabled to get parser.out

if __name__ == "__main__":
    # Takes a file as input and use it for lex
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("file")
    args = arg_parser.parse_args()

    with open(args.file, 'r') as fp:
        parser.parse(fp.read())
    
    print("HLT")
    print("; Variables")
    print("e: DB 0")
    print("f: DB 0")
    print("g: DB 0")
    print("h: DB 0")

