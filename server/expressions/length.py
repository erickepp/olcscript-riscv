from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.value import Value

class Length(Expression):
    def __init__(self, line, col, array):
        self.line = line
        self.col = col
        self.array = array

    def ejecutar(self, ast, env, gen):
        val = self.array.ejecutar(ast, env, gen)

        if val.type != ExpressionType.ARRAY:
            ast.set_errors(f'La variable "{self.array.id}" no es un array.',
                           self.line, self.col, 'Semántico')
            return Value('', ExpressionType.NULL)        

        gen.add_br()
        gen.add_la('t2', f'{val.value}_len')
        return Value('t2', ExpressionType.NUMBER)
