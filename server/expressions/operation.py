from interfaces.expression import Expression
from environment.types import ExpressionType
from environment.value import Value
from expressions.primitive import Primitive

class Operation(Expression):
    def __init__(self, line, col, operador, opL, opR=Primitive(0, 0, None, ExpressionType.NULL)):
        self.line = line
        self.col = col
        self.operador = operador
        self.opL = opL
        self.opR = opR

    def get_dominant_type(self, op1, op2):
        if self.operador in ['+', '-', '*', '/', '%']:
            if op1.type == ExpressionType.NUMBER and op2.type == ExpressionType.NUMBER:
                return ExpressionType.NUMBER
            elif op1.type == ExpressionType.NUMBER and op2.type == ExpressionType.FLOAT:
                return ExpressionType.FLOAT
            elif op1.type == ExpressionType.FLOAT and op2.type == ExpressionType.FLOAT:
                return ExpressionType.FLOAT
            elif op1.type == ExpressionType.FLOAT and op2.type == ExpressionType.NUMBER:
                return ExpressionType.FLOAT
            elif op1.type == ExpressionType.STRING and op2.type == ExpressionType.STRING:
                return ExpressionType.STRING
        elif self.operador in ['==', '!=', '>', '>=', '<', '<=']:
            if op1.type == ExpressionType.NUMBER and op2.type == ExpressionType.NUMBER:
                return ExpressionType.BOOLEAN
            elif op1.type == ExpressionType.FLOAT and op2.type == ExpressionType.FLOAT:
                return ExpressionType.BOOLEAN
            elif op1.type == ExpressionType.BOOLEAN and op2.type == ExpressionType.BOOLEAN:
                return ExpressionType.BOOLEAN
            elif op1.type == ExpressionType.STRING and op2.type == ExpressionType.STRING:
                return ExpressionType.BOOLEAN
            elif op1.type == ExpressionType.CHAR and op2.type == ExpressionType.CHAR:
                return ExpressionType.BOOLEAN
        elif self.operador in ['&&', '||']:
            if op1.type == ExpressionType.BOOLEAN and op2.type == ExpressionType.BOOLEAN:
                return ExpressionType.BOOLEAN
        return ExpressionType.NULL

    def ejecutar(self, ast, env, gen):
        op1 = self.opL.ejecutar(ast, env, gen)
        op2 = self.opR.ejecutar(ast, env, gen)
        dominant_type = self.get_dominant_type(op1, op2)
        temp = gen.new_temp()

        if dominant_type != ExpressionType.NULL:
            if dominant_type in [ExpressionType.NUMBER, ExpressionType.BOOLEAN]:
                gen.add_br()
                gen.add_li('t3', op1.value) 
                gen.add_lw('t1', '0(t3)')
                gen.add_li('t3', op2.value) 
                gen.add_lw('t2', '0(t3)')
                gen.add_br()
            elif dominant_type == ExpressionType.FLOAT:
                gen.add_br()
                if op1.type == ExpressionType.NUMBER:
                    gen.add_li('t3', op1.value) 
                    gen.add_lw('t0', '0(t3)')   
                    gen.add_fcvt_s_w('fa1', 't0')
                else:
                    gen.add_flw('fa1', op1.value, 't0')
                if op2.type == ExpressionType.NUMBER:
                        gen.add_li('t3', op2.value) 
                        gen.add_lw('t0', '0(t3)') 
                        gen.add_fcvt_s_w('fa2', 't0')
                else:
                    gen.add_flw('fa2', op2.value, 't0')
                gen.add_br()

            if self.operador == '+':
                if dominant_type == ExpressionType.NUMBER:
                    gen.add_operation('add', 't0', 't1', 't2')
                    gen.add_li('t3', temp)
                    gen.add_sw('t0', '0(t3)')
                    return Value(str(temp), dominant_type)
                elif dominant_type == ExpressionType.FLOAT:
                    name_id = f'float_{temp}'
                    gen.variable_data(name_id, 'float', '0.0')
                    gen.add_operation('fadd.s', 'fa0', 'fa1', 'fa2')
                    gen.add_fsw('fa0', name_id, 't0')
                    return Value(name_id, dominant_type) 
                
            elif self.operador == '-':
                if dominant_type == ExpressionType.NUMBER:
                    gen.add_operation('sub', 't0', 't1', 't2')
                    gen.add_li('t3', temp)
                    gen.add_sw('t0', '0(t3)')
                    return Value(str(temp), dominant_type)
                elif dominant_type == ExpressionType.FLOAT:
                    name_id = f'float_{temp}'
                    gen.variable_data(name_id, 'float', '0.0')
                    gen.add_operation('fsub.s', 'fa0', 'fa1', 'fa2')
                    gen.add_fsw('fa0', name_id, 't0')
                    return Value(name_id, dominant_type)            
                ast.set_errors('Tipos incorrectos para aplicar el operador resta (-).',
                               self.line, self.col, 'Semántico')
                return Value('', ExpressionType.NULL)
            
            elif self.operador == '*':
                if dominant_type == ExpressionType.NUMBER:
                    gen.add_operation('mul', 't0', 't1', 't2')
                    gen.add_li('t3', temp)
                    gen.add_sw('t0', '0(t3)')
                    return Value(str(temp), dominant_type)
                elif dominant_type == ExpressionType.FLOAT:
                    name_id = f'float_{temp}'
                    gen.variable_data(name_id, 'float', '0.0')
                    gen.add_operation('fmul.s', 'fa0', 'fa1', 'fa2')
                    gen.add_fsw('fa0', name_id, 't0')
                    return Value(name_id, dominant_type)           
                ast.set_errors('Tipos incorrectos para aplicar el operador multiplicación (*).',
                               self.line, self.col, 'Semántico')
                return Value('', ExpressionType.NULL)
            
            elif self.operador == '/':
                if dominant_type == ExpressionType.NUMBER:
                    gen.add_operation('div', 't0', 't1', 't2')
                    gen.add_li('t3', temp)
                    gen.add_sw('t0', '0(t3)')
                    return Value(str(temp), dominant_type)
                elif dominant_type == ExpressionType.FLOAT:
                    name_id = f'float_{temp}'
                    gen.variable_data(name_id, 'float', '0.0')
                    gen.add_operation('fdiv.s', 'fa0', 'fa1', 'fa2')
                    gen.add_fsw('fa0', name_id, 't0')
                    return Value(name_id, dominant_type)     
                ast.set_errors('Tipos incorrectos para aplicar el operador división (/).',
                               self.line, self.col, 'Semántico')
                return Value('', ExpressionType.NULL)
            
            elif self.operador == '%':
                if dominant_type == ExpressionType.NUMBER:
                    gen.add_operation('rem', 't0', 't1', 't2')
                    gen.add_li('t3', temp)
                    gen.add_sw('t0', '0(t3)')
                    return Value(str(temp), dominant_type)
                ast.set_errors('Tipos incorrectos para aplicar el operador módulo (%).',
                               self.line, self.col, 'Semántico')
                return Value('', ExpressionType.NULL)
            
            elif self.operador == '==':
                gen.add_operation('xor', 't0', 't1', 't2')
                gen.add_seqz('t0', 't0')
                gen.add_li('t3', temp)
                gen.add_sw('t0', '0(t3)')
                return Value(str(temp), dominant_type)
            
            elif self.operador == '!=':
                gen.add_operation('xor', 't0', 't1', 't2')
                gen.add_snez('t0', 't0')
                gen.add_li('t3', temp)
                gen.add_sw('t0', '0(t3)')
                return Value(str(temp), dominant_type)
            
            elif self.operador == '>':
                gen.add_operation('slt', 't0', 't2', 't1')
                gen.add_li('t3', temp)
                gen.add_sw('t0', '0(t3)')
                return Value(str(temp), dominant_type)
            
            elif self.operador == '>=':
                gen.add_operation('slt', 't0', 't1', 't2')
                gen.add_operation('xori', 't0', 't0', '1')
                gen.add_li('t3', temp)
                gen.add_sw('t0', '0(t3)')
                return Value(str(temp), dominant_type)
            
            elif self.operador == '<':
                gen.add_operation('slt', 't0', 't1', 't2')
                gen.add_li('t3', temp)
                gen.add_sw('t0', '0(t3)')
                return Value(str(temp), dominant_type)
            
            elif self.operador == '<=':
                gen.add_operation('slt', 't0', 't2', 't1')
                gen.add_operation('xori', 't0', 't0', '1')
                gen.add_li('t3', temp)
                gen.add_sw('t0', '0(t3)')
                return Value(str(temp), dominant_type)
            
            elif self.operador == '&&':
                gen.add_operation('and', 't0', 't1', 't2')
                gen.add_li('t3', temp)
                gen.add_sw('t0', '0(t3)')
                return Value(str(temp), dominant_type)
            
            elif self.operador == '||':
                gen.add_operation('or', 't0', 't1', 't2')
                gen.add_li('t3', temp)
                gen.add_sw('t0', '0(t3)')
                return Value(str(temp), dominant_type)

        elif op1.type != ExpressionType.NULL and op2.type == ExpressionType.NULL:
            if op1.type in [ExpressionType.NUMBER, ExpressionType.BOOLEAN]:
                gen.add_br()
                gen.add_li('t3', op1.value) 
                gen.add_lw('t1', '0(t3)')
                gen.add_br()
            elif op1.type == ExpressionType.FLOAT:
                gen.add_br()
                gen.add_flw('fa1', op1.value, 't0')
                gen.add_br()

            if self.operador == '-':
                if op1.type == ExpressionType.NUMBER:
                    gen.add_neg('t0', 't1')
                    gen.add_li('t3', temp) 
                    gen.add_sw('t0', '0(t3)')
                    return Value(str(temp), op1.type)
                elif op1.type == ExpressionType.FLOAT:
                    name_id = f'float_{temp}'
                    gen.variable_data(name_id, 'float', '0.0')
                    gen.add_fneg_s('fa0', 'fa1')
                    gen.add_fsw('fa0', name_id, 't0')
                    return Value(name_id, op1.type)
                
            elif self.operador == '!' and op1.type == ExpressionType.BOOLEAN:
                gen.add_operation('xori', 't0', 't1', '1')
                gen.add_li('t3', temp)
                gen.add_sw('t0', '0(t3)')
                return Value(str(temp), op1.type)
            
            ast.set_errors(f'Tipo incorrecto para aplicar el operador ({self.operador}).',
                           self.line, self.col, 'Semántico')
            return Value('', ExpressionType.NULL)
 
        ast.set_errors(f'Tipos incorrectos para aplicar el operador ({self.operador}).',
                       self.line, self.col, 'Semántico')
        return Value('', ExpressionType.NULL)
