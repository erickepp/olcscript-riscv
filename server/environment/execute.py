from environment.types import ExpressionType

def root_executer(instruction_list, ast, env, gen):
    for inst in instruction_list or []:
        inst.ejecutar(ast, env, gen)

def statement_executer(instruction_list, ast, env, gen):
    for inst in instruction_list:
        res = inst.ejecutar(ast, env, gen)
        if res and res.type != ExpressionType.NULL:
            return res
    return None
