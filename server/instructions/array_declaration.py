from interfaces.instruction import Instruction
from environment.symbol import Symbol
from environment.types import ExpressionType

class ArrayDeclaration(Instruction):
    def __init__(self, line, col, declaration_type, id, data_type, exp):
        self.line = line
        self.col = col
        self.declaration_type = declaration_type
        self.id = id
        self.data_type = data_type
        self.exp = exp

    def ejecutar(self, ast, env, gen):
        arr_value = self.exp.ejecutar(ast, env, gen)

        if arr_value.type != ExpressionType.ARRAY:
            ast.set_errors(f'La expresión no es un array.', self.line, self.col, 'Semántico')
            return
        
        name_id = f'arr_{gen.new_temp()}'
        gen.variable_data(name_id, 'space', 100)
        gen.variable_data(f'{name_id}_len', 'word', len(arr_value.value))
        gen.add_br()
        gen.add_la('t0', name_id)

        for value in arr_value.value:
            gen.add_br()
            gen.add_li('t3', value)
            gen.add_sw('t3', '0(t0)')
            gen.add_operation('addi', 't0', 't0', '4')

        sym = Symbol(self.line, self.col, self.id, arr_value.type, name_id)
        env.save_variable(ast, self.id, sym, self.line, self.col, self.declaration_type)
