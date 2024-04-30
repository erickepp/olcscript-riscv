from interfaces.instruction import Instruction
from environment.types import ExpressionType

class Assignment(Instruction):
    def __init__(self, line, col, id, exp):
        self.line = line
        self.col = col
        self.id = id
        self.exp = exp

    def ejecutar(self, ast, env, gen):
        result = self.exp.ejecutar(ast, env, gen)
        sym = env.get_variable(ast, self.id, self.line, self.col)

        if sym.type == ExpressionType.NULL:
            return
        
        if sym.type in [ExpressionType.NUMBER, ExpressionType.BOOLEAN, ExpressionType.CHAR]:
            gen.add_br()
            if 't' in result.value:
                gen.add_move('t0', result.value)
            else:
                gen.add_li('t0', result.value)
            gen.add_lw('t1', '0(t0)')
            gen.add_li('t3', sym.position)
            gen.add_sw('t1', '0(t3)')
        elif sym.type == ExpressionType.FLOAT:
            gen.add_br()
            gen.add_la('t0', result.value)
            gen.add_lw('t1', '0(t0)')
            gen.add_la('t3', sym.position)
            gen.add_sw('t1', '0(t3)')
