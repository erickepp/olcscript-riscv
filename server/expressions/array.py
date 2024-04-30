from interfaces.instruction import Instruction
from environment.types import ExpressionType
from environment.value import Value

class Array(Instruction):
    def __init__(self, line, col, list_exp):
        self.line = line
        self.col = col
        self.list_exp = list_exp

    def ejecutar(self, ast, env, gen):
        arr_val = []
        for exp in self.list_exp:
            val = exp.ejecutar(ast, env, gen)
            arr_val.append(val.value)
        return Value(arr_val, ExpressionType.ARRAY)
