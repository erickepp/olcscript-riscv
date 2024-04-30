from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.value import Value

class ArrayAccess(Expression):
    def __init__(self, line, col, id, index):
        self.line = line
        self.col = col
        self.id = id
        self.index = index

    def ejecutar(self, ast, env, gen):
        sym = env.get_variable(ast, self.id, self.line, self.col)
        if sym.type != ExpressionType.ARRAY:
            return Value('', ExpressionType.NULL)
        index_val = self.index.ejecutar(ast, env, gen)
        if index_val.type != ExpressionType.NUMBER:
            ast.set_errors('El índice contiene un valor incorrecto.', self.line, self.col, 'Semántico')
            return Value('', ExpressionType.NULL)

        gen.add_br()
        if 't' in index_val.value:
            gen.add_move('t3', index_val.value)
        else:
            gen.add_li('t3', index_val.value)
        gen.add_lw('t1', '0(t3)')
        gen.add_move('t0', 't1')
        gen.add_slli('t0', 't0', '2')
        gen.add_la('t1', sym.position)
        gen.add_lw('t1', '0(t1)')
        gen.add_operation('add', 't2', 't1', 't0')
        return Value('t2', ExpressionType.NUMBER)
