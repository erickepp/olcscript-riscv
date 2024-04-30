from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.value import Value

class IndexOf(Expression):
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
            return Value('', ExpressionType.NULL)

        element = self.exp.ejecutar(ast, env, gen)
        loop_lbl = gen.new_label()
        end_loop_lbl = gen.new_label()
        true_lbl = gen.new_label()
        false_lbl = gen.new_label()

        gen.add_br()
        gen.add_la('t0', val.value)
        gen.add_lw('t1', f'{val.value}_len')
        gen.add_li('t2', '0')
        gen.add_li('t4', element.value)
        gen.add_lw('t3', '0(t4)')
        gen.add_li('t4', '1')
        gen.add_neg('t4', 't4')
        gen.add_li('t5', gen.new_temp())
        gen.add_sw('t4', '0(t5)')

        gen.new_body_label(loop_lbl)
        gen.add_bge('t2', 't1', end_loop_lbl)
        gen.add_lw('t4', '0(t0)')
        gen.add_lw('t4', '0(t4)')

        gen.add_br()
        gen.add_beq('t3', 't4', true_lbl)
        gen.add_jump(false_lbl)

        gen.new_body_label(true_lbl)
        gen.add_sw('t2', '0(t5)')
        gen.add_jump(end_loop_lbl)
       
        gen.new_body_label(false_lbl)
        gen.add_operation('addi', 't0', 't0', '4')
        gen.add_operation('addi', 't2', 't2', '1')
        gen.add_jump(loop_lbl)

        gen.new_body_label(end_loop_lbl)
        return Value('t5', ExpressionType.NUMBER)
