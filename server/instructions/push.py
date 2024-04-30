from interfaces.instruction import Instruction
from environment.types import ExpressionType

class Push(Instruction):
    def __init__(self, line, col, array, exp):
        self.line = line
        self.col = col
        self.array = array
        self.exp = exp

    def ejecutar(self, ast, env, gen):
        val = self.array.ejecutar(ast, env, gen)

        if val.type != ExpressionType.ARRAY:
            ast.set_errors(f'La variable "{self.array.id}" no es un array.',
                           self.line, self.col, 'Semántico')
            return
        
        element = self.exp.ejecutar(ast, env, gen)
        loop_lbl = gen.new_label()
        end_loop_lbl = gen.new_label()

        gen.add_br()
        gen.add_la('t0', val.value)
        gen.add_lw('t1', f'{val.value}_len')
        gen.add_li('t2', '0')

        gen.new_body_label(loop_lbl)
        gen.add_bge('t2', 't1', end_loop_lbl)
        gen.add_operation('addi', 't0', 't0', '4')
        gen.add_operation('addi', 't2', 't2', '1')
        gen.add_jump(loop_lbl)

        gen.new_body_label(end_loop_lbl)
        gen.add_operation('addi', 't1', 't1', '1')
        gen.add_la('t3', f'{val.value}_len')
        gen.add_sw('t1', '0(t3)')
        gen.add_li('t2', element.value)
        gen.add_sw('t2', '0(t0)')
