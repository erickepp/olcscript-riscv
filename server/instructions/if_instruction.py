from interfaces.instruction import Instruction
from environment.environment import Environment
from environment.types import ExpressionType
from environment.execute import statement_executer

class If(Instruction):
    def __init__(self, line, col, exp, block, else_if_list, else_instruction):
        self.line = line
        self.col = col
        self.exp = exp
        self.block = block
        self.else_if_list = else_if_list
        self.else_instruction = else_instruction

    def ejecutar(self, ast, env, gen):
        if_exp = self.exp.ejecutar(ast, env, gen)
        if if_exp.type != ExpressionType.BOOLEAN:
            ast.set_errors(f'Expresión incorrecta: el tipo de dato no es boolean.',
                           self.line, self.col, 'Semántico')
            return

        true_lbl = gen.new_label()
        false_lbl = gen.new_label()
        new_lbl = gen.new_label()

        gen.add_li('t3', if_exp.value)
        gen.add_lw('t0', '0(t3)')
        gen.add_li('t1', '1')

        gen.add_br()
        gen.add_beq('t0', 't1', true_lbl)
        gen.add_jump(false_lbl)

        gen.new_body_label(true_lbl)
        if_env = Environment(env, 'IF')
        statement_executer(self.block, ast, if_env, gen)
        gen.add_jump(new_lbl)

        gen.new_body_label(false_lbl)
        else_if_env = Environment(env, 'ELSE_IF')
        for else_if in self.else_if_list:
            else_if_exp = else_if['expression'].ejecutar(ast, env, gen)
            if else_if_exp.type != ExpressionType.BOOLEAN:
                ast.set_errors(f'Expresión incorrecta: el tipo de dato no es boolean".',
                               else_if.line, else_if.col, 'Semántico')
                return

            true_lbl = gen.new_label()
            false_lbl = gen.new_label()

            gen.add_li('t3', else_if_exp.value)
            gen.add_lw('t0', '0(t3)')
            gen.add_li('t1', '1')

            gen.add_br()
            gen.add_beq('t0', 't1', true_lbl)
            gen.add_jump(false_lbl)

            gen.new_body_label(true_lbl)
            statement_executer(else_if['block'], ast, else_if_env, gen)
            gen.add_jump(new_lbl)
            gen.new_body_label(false_lbl)
        
        if self.else_instruction:
            else_env = Environment(env, 'ELSE')
            statement_executer(self.else_instruction, ast, else_env, gen)
        
        gen.add_jump(new_lbl)
        gen.new_body_label(new_lbl)
