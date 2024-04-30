from interfaces.instruction import Instruction
from environment.types import ExpressionType

class ConsoleLog(Instruction):
    def __init__(self, line, col, exp):
        self.line = line
        self.col = col
        self.exp = exp

    def ejecutar(self, ast, env, gen):
        for exp in self.exp:
            val = exp.ejecutar(ast, env, gen)
            gen.add_br()

            if val.type == ExpressionType.NUMBER:
                if 't' in val.value:
                    gen.add_move('t3', val.value)
                else:
                    gen.add_li('t3', val.value)
                gen.add_lw('a0', '0(t3)')
                gen.add_li('a7', '1')
            elif val.type == ExpressionType.FLOAT:
                gen.add_flw('fa0', val.value, 't0')
                gen.add_li('a7', '2')
            elif val.type == ExpressionType.BOOLEAN:
                self.handle_boolean(gen, val.value)
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
            elif val.type == ExpressionType.ARRAY:
                self.handle_array(gen, val.value)

            gen.add_system_call()
            gen.add_br()
            gen.add_li('a0', '32')
            gen.add_li('a7', '11')
            gen.add_system_call()

        gen.add_br()
        gen.add_li('a0', '10')
        gen.add_li('a7', '11')
        gen.add_system_call()

    def handle_boolean(self, gen, value):
        true_lbl = gen.new_label()
        false_lbl = gen.new_label()
        new_lbl = gen.new_label()

        gen.add_li('t3', value)
        gen.add_lw('t0', '0(t3)')
        gen.add_li('t1', '1')

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
    
    def handle_array(self, gen, value):
        loop_lbl = gen.new_label()
        end_loop_lbl = gen.new_label()

        gen.add_la('t0', value)
        gen.add_lw('t1', f'{value}_len')
        gen.add_li('t2', '0')

        gen.add_br()
        gen.add_li('a0', '91')
        gen.add_li('a7', '11')
        gen.add_system_call()

        gen.new_body_label(loop_lbl)
        gen.add_bge('t2', 't1', end_loop_lbl)
        gen.add_lw('t3', '0(t0)')
        gen.add_lw('a0', '0(t3)')
        gen.add_li('a7', '1')
        gen.add_system_call()

        gen.add_br()
        gen.add_operation('addi', 't3', 't2', '1')
        gen.add_bge('t3', 't1', end_loop_lbl)
        gen.add_li('a0', '44')
        gen.add_li('a7', '11')
        gen.add_system_call()

        gen.add_br()
        gen.add_li('a0', '32')
        gen.add_li('a7', '11')
        gen.add_system_call()

        gen.add_br()
        gen.add_operation('addi', 't0', 't0', '4')
        gen.add_operation('addi', 't2', 't2', '1')
        gen.add_jump(loop_lbl)

        gen.new_body_label(end_loop_lbl)
        gen.add_li('a0', '93')
        gen.add_li('a7', '11')
