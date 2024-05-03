from interfaces.expression import Expression
from environment.value import Value
from environment.types import ExpressionType

class Break(Expression):
    def __init__(self, line, col):
        self.line = line
        self.col = col

    def ejecutar(self, ast, env, gen):
        if env.switch_validation() or env.loop_validation():
            return Value('', ExpressionType.BREAK)
        ast.set_errors('"break" no se encuentra dentro de un bloque "switch", "while" o "for".',
                       self.line, self.col, 'Semántico')
        return Value('', ExpressionType.NULL)
