from interfaces.instruction import Instruction
from environment.symbol import Symbol
from environment.types import ExpressionType
from expressions.primitive import Primitive

class Declaration(Instruction):
    def __init__(self, line, col, declaration_type, id, data_type=None, exp=None):
        self.line = line
        self.col = col
        self.declaration_type = declaration_type
        self.id = id
        self.data_type = data_type
        self.exp = exp

    def ejecutar(self, ast, env, gen):
        if self.data_type and self.exp:
            result = self.exp.ejecutar(ast, env, gen)
            if result.type != self.data_type:
                ast.set_errors('Declaración incorrecta: tipos de dato diferentes.',
                               self.line, self.col, 'Semántico')
                return
            sym = Symbol(self.line, self.col, self.id, self.data_type, result.value)
            env.save_variable(ast, self.id, sym, self.line, self.col, self.declaration_type)

        elif self.data_type is None and self.exp:
            result = self.exp.ejecutar(ast, env, gen)
            sym = Symbol(self.line, self.col, self.id, result.type, result.value)
            env.save_variable(ast, self.id, sym, self.line, self.col, self.declaration_type)

        elif self.data_type and self.exp is None:
            if self.data_type == ExpressionType.NUMBER:
                value = 0
            elif self.data_type == ExpressionType.FLOAT:
                value = 0.0
            elif self.data_type == ExpressionType.STRING:
                value = ''
            elif self.data_type == ExpressionType.BOOLEAN:
                value = True
            result = Primitive(self.line, self.col, value, self.data_type).ejecutar(ast, env, gen)
            sym = Symbol(self.line, self.col, self.id, self.data_type, result.value)
            env.save_variable(ast, self.id, sym, self.line, self.col, self.declaration_type)
