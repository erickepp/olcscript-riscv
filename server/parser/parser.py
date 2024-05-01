import parser.ply.lex as lex
import parser.ply.yacc as yacc

from environment.types import ExpressionType
from expressions.primitive import Primitive
from expressions.operation import Operation
from expressions.access import Access
from expressions.array import Array
from expressions.array_access import ArrayAccess
from expressions.pop import Pop
from expressions.index_of import IndexOf
from expressions.length import Length
from expressions.break_statement import Break

from instructions.declaration import Declaration
from instructions.assignment import Assignment
from instructions.array_declaration import ArrayDeclaration
from instructions.push import Push
from instructions.if_instruction import If
from instructions.switch_instruction import Switch
from instructions.console_log import ConsoleLog

class codeParams:
    def __init__(self, line, column):
        self.line = line
        self.column = column

ast = None

reserved = {
    'number': 'NUMBER',
    'float' : 'FLOAT',
    'string': 'STRING',
    'boolean': 'BOOLEAN',
    'char': 'CHAR',
    'var': 'VAR',
    'const': 'CONST',
    'if': 'IF',
    'else': 'ELSE',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'while': 'WHILE',
    'for': 'FOR',
    'of': 'OF',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'push': 'PUSH',
    'pop': 'POP',
    'indexOf': 'INDEXOF',
    'length': 'LENGTH',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'console': 'CONSOLE',
    'log': 'LOG',
    'parseInt': 'PARSEINT',
    'parseFloat': 'PARSEFLOAT',
    'toString': 'TOSTRING',
    'toLowerCase': 'TOLOWERCASE',
    'toUpperCase': 'TOUPPERCASE',
    'typeof': 'TYPEOF'
}

tokens = [
    'INCREMENTO',
    'DECREMENTO',
    'MENIGQUE',
    'MAYIGQUE',
    'DOBLEIG',
    'NOIG',
    'OR',
    'AND',
    'DOSPTS',
    'PUNTO',
    'PTCOMA',
    'COMA',
    'LLAVIZQ',
    'LLAVDER',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'MODULO',
    'MENQUE',
    'MAYQUE',
    'NOT',
    'IGUAL',
    'DECIMAL',
    'ENTERO',
    'TRUE',
    'FALSE',
    'CADENA',
    'CARACTER',
    'ID'
] + list(reserved.values())

t_INCREMENTO = r'\+='
t_DECREMENTO = r'-='
t_MENIGQUE   = r'<='
t_MAYIGQUE   = r'>='
t_DOBLEIG    = r'=='
t_NOIG       = r'!='
t_OR         = r'\|\|'
t_AND        = r'&&'
t_DOSPTS     = r':'
t_PUNTO      = r'\.'
t_PTCOMA     = r';'
t_COMA       = r','
t_LLAVIZQ    = r'{'
t_LLAVDER    = r'}'
t_PARIZQ     = r'\('
t_PARDER     = r'\)'
t_CORIZQ     = r'\['
t_CORDER     = r'\]'
t_MAS        = r'\+'
t_MENOS      = r'-'
t_POR        = r'\*'
t_DIVIDIDO   = r'/'
t_MODULO     = r'%' 
t_MENQUE     = r'<' 
t_MAYQUE     = r'>' 
t_NOT        = r'!' 
t_IGUAL      = r'='


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        float_value = float(t.value)
        params = get_params(t)
        t.value = Primitive(params.line, params.column, float_value, ExpressionType.FLOAT)
    except ValueError:
        print('Error al convertir a decimal %d', t.value)
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t


def t_ENTERO(t):
    r'\d+'
    try:
        int_value = int(t.value)
        params = get_params(t)
        t.value = Primitive(params.line, params.column, int_value, ExpressionType.NUMBER)
    except ValueError:
        print('Error al convertir a entero %d', t.value)
        t.value = Primitive(0, 0, None, ExpressionType.NULL)
    return t


def t_TRUE(t):
    r'true'
    params = get_params(t)
    t.value = Primitive(params.line, params.column, True, ExpressionType.BOOLEAN)
    return t


def t_FALSE(t):
    r'false'
    params = get_params(t)
    t.value = Primitive(params.line, params.column, False, ExpressionType.BOOLEAN)
    return t


def t_CADENA(t):
    r'\"([^\n\"\\]|\\(n|r|t|\\|\'|\"))*\"'
    str_value = t.value[1:-1]
    params = get_params(t)
    t.value = Primitive(params.line, params.column, str_value, ExpressionType.STRING)
    return t


def t_CARACTER(t):
    r'\'([^\n\'\\]|\\(n|r|t|\\|\'|\"))\''
    char_value = t.value[1:-1]
    params = get_params(t)
    t.value = Primitive(params.line, params.column, char_value, ExpressionType.CHAR)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_COMENTARIO_SIMPLE(t):
    r'//.*'
    t.lexer.lineno += 1


def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


t_ignore = ' \t\r'


def t_error(t):
    params = get_params(t)
    ast.set_errors(f'El carácter "{t.value[0]}" no pertenece al lenguaje.',
                   params.line, params.column, 'Léxico')
    t.lexer.skip(1)


precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'MAYQUE', 'MENQUE', 'MAYIGQUE', 'MENIGQUE', 'DOBLEIG', 'NOIG'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO', 'MODULO'),
    ('right', 'UMENOS'),
)


def p_init(p):
    'init : instrucciones'
    p[0] = p[1]


def p_lista_instrucciones(p):
    '''instrucciones : instrucciones instruccion
                     |'''
    if len(p) > 1:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = []


def p_instrucciones_error(p):
    'instrucciones : instrucciones error instruccion'
    p[1].append(p[3])
    p[0] = p[1]


def p_instruccion_declaracion(p):
    '''instruccion : VAR ID DOSPTS tipo_dato IGUAL expresion PTCOMA
                   | CONST ID DOSPTS tipo_dato IGUAL expresion PTCOMA
                   | VAR ID IGUAL expresion PTCOMA
                   | CONST ID IGUAL expresion PTCOMA
                   | VAR ID DOSPTS tipo_dato PTCOMA'''
    params = get_params(p)
    if p[5] == '=':
        p[0] = Declaration(params.line, params.column, p[1], p[2], p[4], p[6])
    elif p[3] == '=':
        p[0] = Declaration(params.line, params.column, p[1], p[2], exp=p[4])
    elif p[5] == ';':
        p[0] = Declaration(params.line, params.column, p[1], p[2], data_type=p[4])


def p_instruccion_asignacion(p):
    'instruccion : ID IGUAL expresion PTCOMA'
    params = get_params(p)
    p[0] = Assignment(params.line, params.column, p[1], p[3])


def p_instruccion_declaracion_array(p):
    '''instruccion : VAR ID DOSPTS tipo_dato CORIZQ CORDER IGUAL expresion PTCOMA
                   | CONST ID DOSPTS tipo_dato CORIZQ CORDER IGUAL expresion PTCOMA'''
    params = get_params(p)
    p[0] = ArrayDeclaration(params.line, params.column, p[1], p[2], p[4], p[8])


def p_expresion_array(p):
    '''expresion : CORIZQ lista_expresiones CORDER
                 | CORIZQ CORDER'''
    params = get_params(p)
    if len(p) > 3:
        p[0] = Array(params.line, params.column, p[2])
    else:
        p[0] = Array(params.line, params.column, [])


def p_instruccion_push(p):
    'instruccion : expresion PUNTO PUSH PARIZQ expresion PARDER PTCOMA'
    params = get_params(p)
    p[0] = Push(params.line, params.column, p[1], p[5])


def p_expresion_pop(p):
    'expresion : expresion PUNTO POP PARIZQ PARDER'
    params = get_params(p)
    p[0] = Pop(params.line, params.column, p[1])


def p_expresion_index_of(p):
    'expresion : expresion PUNTO INDEXOF PARIZQ expresion PARDER'
    params = get_params(p)
    p[0] = IndexOf(params.line, params.column, p[1], p[5])


def p_expresion_length(p):
    'expresion : expresion PUNTO LENGTH'
    params = get_params(p)
    p[0] = Length(params.line, params.column, p[1])


def p_expresion_acceso(p):
    '''acceso : ID CORIZQ expresion CORDER
              | ID'''
    params = get_params(p)
    if len(p) > 2:
        p[0] = ArrayAccess(params.line, params.column, p[1], p[3])
    else:
        p[0] = Access(params.line, params.column, p[1])


def p_instruccion_if(p):
    'instruccion : IF PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER lista_else_if else'
    params = get_params(p)
    p[0] = If(params.line, params.column, p[3], p[6], p[8], p[9])


def p_lista_else_if(p):
    '''lista_else_if : lista_else_if ELSE IF PARIZQ expresion PARDER LLAVIZQ instrucciones LLAVDER
                     |'''
    if len(p) > 1:
        p[1].append({'expression': p[5], 'block': p[8]})
        p[0] = p[1]
    else:
        p[0] = []


def p_else(p):
    '''else : ELSE LLAVIZQ instrucciones LLAVDER
            |'''
    if len(p) > 1:
        p[0] = p[3]
    else:
        p[0] = None


def p_instruccion_switch(p):
    'instruccion : SWITCH PARIZQ expresion PARDER LLAVIZQ lista_case default LLAVDER'
    params = get_params(p)
    p[0] = Switch(params.line, params.column, p[3], p[6], p[7])


def p_lista_case(p):
    '''lista_case : lista_case CASE expresion DOSPTS instrucciones
                  |'''
    if len(p) > 1:
        p[1].append({'expression': p[3], 'block': p[5]})
        p[0] = p[1]
    else:
        p[0] = []


def p_default(p):
    '''default : DEFAULT DOSPTS instrucciones
               |'''
    if len(p) > 1:
        p[0] = p[3]
    else:
        p[0] = None


def p_instruccion_break(p):
    'instruccion : BREAK PTCOMA'
    params = get_params(p)
    p[0] = Break(params.line, params.column)


def p_instruccion_console_log(p):
    '''instruccion : CONSOLE PUNTO LOG PARIZQ lista_expresiones PARDER PTCOMA
                   | CONSOLE PUNTO LOG PARIZQ PARDER PTCOMA'''
    params = get_params(p)
    if len(p) > 7:
        p[0] = ConsoleLog(params.line, params.column, p[5])
    else:
        p[0] = ConsoleLog(params.line, params.column, [])


def p_lista_expresiones(p):
    '''lista_expresiones : lista_expresiones COMA expresion
                         | expresion'''
    if len(p) > 2:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]


def p_tipo_dato(p):
    '''tipo_dato : NUMBER
                 | FLOAT
                 | STRING
                 | CHAR
                 | BOOLEAN'''
    if p[1] == 'number':
        p[0] = ExpressionType.NUMBER
    elif p[1] == 'float': 
        p[0] = ExpressionType.FLOAT
    elif p[1] == 'string':
        p[0] = ExpressionType.STRING
    elif p[1] == 'char':
        p[0] = ExpressionType.CHAR
    elif p[1] == 'boolean':
        p[0] = ExpressionType.BOOLEAN


def p_expresion(p):
    '''expresion : ENTERO
                 | DECIMAL
                 | TRUE
                 | FALSE
                 | CADENA
                 | CARACTER
                 | acceso'''
    p[0] = p[1]


def p_expresion_aritmetica(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVIDIDO expresion
                 | expresion MODULO expresion'''
    params = get_params(p)
    if p[2] == '+':
        p[0] = Operation(params.line, params.column, '+', p[1], p[3])
    elif p[2] == '-':
        p[0] = Operation(params.line, params.column, '-', p[1], p[3])
    elif p[2] == '*':
        p[0] = Operation(params.line, params.column, '*', p[1], p[3])
    elif p[2] == '/':
        p[0] = Operation(params.line, params.column, '/', p[1], p[3])
    elif p[2] == '%':
        p[0] = Operation(params.line, params.column, '%', p[1], p[3])


def p_expresion_unaria(p):
    'expresion : MENOS expresion %prec UMENOS'
    params = get_params(p)
    p[0] = Operation(params.line, params.column, '-', p[2])


def p_expresion_agrupacion(p):
    'expresion : PARIZQ expresion PARDER'
    p[0] = p[2]


def p_expresion_relacional(p):
    '''expresion : expresion MAYQUE expresion
                 | expresion MENQUE expresion
                 | expresion MAYIGQUE expresion
                 | expresion MENIGQUE expresion
                 | expresion DOBLEIG expresion
                 | expresion NOIG expresion'''
    params = get_params(p)
    if p[2] == '>':
        p[0] = Operation(params.line, params.column, '>', p[1], p[3])
    elif p[2] == '<':
        p[0] = Operation(params.line, params.column, '<', p[1], p[3])
    elif p[2] == '>=':
        p[0] = Operation(params.line, params.column, '>=', p[1], p[3])
    elif p[2] == '<=':
        p[0] = Operation(params.line, params.column, '<=', p[1], p[3])
    elif p[2] == '==':
        p[0] = Operation(params.line, params.column, '==', p[1], p[3])
    elif p[2] == '!=':
        p[0] = Operation(params.line, params.column, '!=', p[1], p[3])


def p_expresion_logica(p):
    '''expresion : expresion OR expresion
                 | expresion AND expresion
                 | NOT expresion'''
    params = get_params(p)
    if p[2] == '||':
        p[0] = Operation(params.line, params.column, '||', p[1], p[3])
    elif p[2] == '&&':
        p[0] = Operation(params.line, params.column, '&&', p[1], p[3])
    elif p[1] == '!':
        p[0] = Operation(params.line, params.column, '!', p[2])


def p_error(p):
    if p:
        params = get_params(p)
        ast.set_errors(f'No se esperaba el token "{p.type}".', params.line, params.column, 'Sintáctico')
    else:
        ast.set_console('Error sintáctico irrecuperable')
        ast.set_errors(f'Error irrecuperable.', 0, 0, 'Sintáctico')


def get_params(t):
    line = t.lexer.lineno
    lexpos = t.lexpos if isinstance(t.lexpos, int) else 0
    column = lexpos - t.lexer.lexdata.rfind('\n', 0, lexpos) 
    return codeParams(line, column)


class Parser:
    def __init__(self, ast):
        self.ast = ast

    def interpretar(self, input):
        global ast; ast = self.ast
        lexer = lex.lex()
        parser = yacc.yacc()
        result = parser.parse(input)
        return result
