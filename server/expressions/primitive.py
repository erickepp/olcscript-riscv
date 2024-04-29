from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.value import Value

class Primitive(Expression):
    def __init__(self, line, col, value, type):
        self.line = line
        self.col = col
        self.value = value
        self.type = type

    def ejecutar(self, ast, env, gen):
        temp = gen.new_temp()

        if self.type == ExpressionType.NUMBER:
            gen.add_br()
            gen.add_li('t0', self.value)
            gen.add_li('t3', temp)
            gen.add_sw('t0', '0(t3)')
            return Value(str(temp), self.type)
        
        elif self.type == ExpressionType.FLOAT:
            name_id = f'float_{temp}'
            gen.variable_data(name_id, 'float', self.value)
            return Value(name_id, self.type)
        
        elif self.type == ExpressionType.BOOLEAN:
            gen.add_br()
            gen.add_li('t0', int(self.value))
            gen.add_li('t3', temp)
            gen.add_sw('t0', '0(t3)')
            return Value(str(temp), self.type)
        
        elif self.type == ExpressionType.STRING:
            name_id = f'str_{temp}'
            gen.variable_data(name_id, 'string', f'"{self.value}"')
            return Value(name_id, self.type)
        
        elif self.type == ExpressionType.CHAR:
            gen.add_br()
            gen.add_li('t0', ord(self.value))
            gen.add_li('t3', temp)
            gen.add_sw('t0', '0(t3)')
            return Value(str(temp), self.type)
        
        else:
            return Value('', ExpressionType.NULL)
