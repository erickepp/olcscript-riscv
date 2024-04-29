from interfaces.expression import Expression
from environment.value import Value

class Access(Expression):
    def __init__(self, line, col, id):
        self.line = line
        self.col = col
        self.id = id

    def ejecutar(self, ast, env, gen):
        sym = env.get_variable(ast, self.id, self.line, self.col)
        return Value(sym.position, sym.type)
