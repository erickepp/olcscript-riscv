from interfaces.instruction import Instruction
from environment.environment import Environment
from environment.execute import statement_executer

class Switch(Instruction):
    def __init__(self, line, col, exp, case_list, default_instruction):
        self.line = line
        self.col = col
        self.exp = exp
        self.case_list = case_list
        self.default_instruction = default_instruction

    def ejecutar(self, ast, env, gen):
        switch_exp = self.exp.ejecutar(ast, env, gen)
        switch_env = Environment(env, 'SWITCH_CASE')
        new_lbl = gen.new_label()

        for case in self.case_list:
            case_exp = case['expression'].ejecutar(ast, env, gen)
            if switch_exp.type != case_exp.type:
                ast.set_errors('Los tipos de dato no son iguales.', self.line, self.col, 'Semántico')
                return

            true_lbl = gen.new_label()
            false_lbl = gen.new_label()

            gen.add_li('t3', switch_exp.value)
            gen.add_lw('t0', '0(t3)')
            gen.add_li('t3', case_exp.value)
            gen.add_lw('t1', '0(t3)')
                
            gen.add_br()
            gen.add_beq('t0', 't1', true_lbl)
            gen.add_jump(false_lbl)

            gen.new_body_label(true_lbl)
            return_value = statement_executer(case['block'], ast, switch_env, gen)
            if return_value:
                gen.add_jump(new_lbl)
            gen.new_body_label(false_lbl)
                
        if self.default_instruction:
            switch_env = Environment(env, 'SWITCH_DEFAULT')
            return_value = statement_executer(self.default_instruction, ast, switch_env, gen)
            if return_value:
                gen.add_jump(new_lbl)
    
        gen.new_body_label(new_lbl)
