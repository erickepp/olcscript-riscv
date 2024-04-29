from interfaces.instruction import Instruction
from environment.types import ExpressionType

class Assignment(Instruction):
    def __init__(self, line, col, access, exp):
        self.line = line
        self.col = col
        self.access = access
        self.exp = exp

    def ejecutar(self, ast, env, gen):
        val = self.access.ejecutar(ast, env, gen)
        result = self.exp.ejecutar(ast, env, gen)

        if val.type == ExpressionType.NULL:
            return
        
        if val.type in [ExpressionType.NUMBER, ExpressionType.BOOLEAN, ExpressionType.CHAR]:
            gen.add_br()
            gen.add_li('t0', result.value)
            gen.add_lw('t1', '0(t0)')
            gen.add_li('t3', val.value)
            gen.add_sw('t1', '0(t3)')
        elif val.type == ExpressionType.FLOAT:
            gen.add_br()
            gen.add_la('t0', result.value)
            gen.add_lw('t1', '0(t0)')
            gen.add_la('t3', val.value)
            gen.add_sw('t1', '0(t3)')
