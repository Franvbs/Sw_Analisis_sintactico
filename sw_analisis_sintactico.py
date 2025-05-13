import ply.lex as lex
import ply.yacc as yacc

# ---------------------
# ANÁLISIS LÉXICO
# ---------------------

# Palabras clave
keywords = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
}

# Lista de tokens
tokens = [
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN',
    'ID', 'EQ', 'NEQ', 'GT', 'LT',
] + list(keywords.values())

# Reglas de tokens (símbolos)
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQ      = r'=='
t_NEQ     = r'!='
t_GT      = r'>'
t_LT      = r'<'

# Números (enteros y decimales)
def t_NUMBER(t):
    r'\d+\.\d+|\d+'
    t.value = float(t.value)
    return t

# Identificadores y palabras clave
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'ID')
    return t

# Ignorar espacios
t_ignore = ' \t'

# Saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Errores léxicos
def t_error(t):
    print(f"Caracter ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

# Crear el lexer
lexer = lex.lex()


# ---------------------
# ANÁLISIS SINTÁCTICO
# ---------------------

# Precedencia de operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# Reglas de gramática

def p_statement_expr(p):
    'statement : expression'
    print("Resultado:", p[1])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+': p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_expression_id(p):
    'expression : ID'
    p[0] = 0  # Puedes agregar una tabla de variables si deseas

# Estructura IF-ELSE
def p_statement_if_else(p):
    'statement : IF expression statement ELSE statement'
    if p[2]:
        p[3]
    else:
        p[5]

# Estructura WHILE
def p_statement_while(p):
    'statement : WHILE expression statement'
    while p[2]:
        p[3]

# Error de sintaxis
def p_error(p):
    if p:
        print("Error de sintaxis en '%s'" % p.value)
    else:
        print("Error de sintaxis al final de la entrada")

# Crear parser
parser = yacc.yacc()


# ---------------------
# PROGRAMA PRINCIPAL
# ---------------------

def main():
    print("Analizador léxico y sintáctico con PLY")
    print("Escribe una expresión (Ctrl+C para salir)\n")

    while True:
        try:
            s = input(">> ")
        except (EOFError, KeyboardInterrupt):
            print("\nFinalizado.")
            break
        if not s:
            continue
        parser.parse(s)

if __name__ == '__main__':
    main()
