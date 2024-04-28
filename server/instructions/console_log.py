from interfaces.instruction import Instruction
from environment.types import ExpressionType

class ConsoleLog(Instruction):
    def __init__(self, line, col, exp):
        self.line = line
        self.col = col
        self.exp = exp

    def handle_boolean(self, gen):
        true_lbl = gen.new_label()
        false_lbl = gen.new_label()
        new_lbl = gen.new_label()

        gen.add_br()
        gen.add_beq('t0', 't1', true_lbl)
        gen.add_jump(false_lbl)

        gen.new_body_label(true_lbl)
        gen.add_la('a0', 'str_true')
        gen.add_jump(new_lbl)

        gen.new_body_label(false_lbl)
        gen.add_la('a0', 'str_false')

        gen.new_body_label(new_lbl)
        gen.add_li('a7', '4')

    def ejecutar(self, ast, env, gen):
        for exp in self.exp:
            val = exp.ejecutar(ast, env, gen)
            gen.add_br()

            if val.type == ExpressionType.NUMBER:
                gen.add_li('t3', val.value)
                gen.add_lw('a0', '0(t3)')
                gen.add_li('a7', '1')
            elif val.type == ExpressionType.FLOAT:
                gen.add_flw('fa0', val.value, 't0')
                gen.add_li('a7', '2')
            elif val.type == ExpressionType.BOOLEAN:
                gen.add_li('t3', val.value)
                gen.add_lw('t0', '0(t3)')
                gen.add_li('t1', '1')
                self.handle_boolean(gen)
            elif val.type == ExpressionType.STRING:
                gen.add_la('a0', val.value)
                gen.add_li('a7', '4')
            elif val.type == ExpressionType.CHAR:
                gen.add_li('t3', val.value)
                gen.add_lb('a0', '0(t3)')
                gen.add_li('a7', '11')
            elif val.type == ExpressionType.NULL:
                gen.add_la('a0', 'str_null')
                gen.add_li('a7', '4')

            gen.add_system_call()
            gen.add_br()
            gen.add_li('a0', '32')
            gen.add_li('a7', '11')
            gen.add_system_call()

        gen.add_br()
        gen.add_li('a0', '10')
        gen.add_li('a7', '11')
        gen.add_system_call()
