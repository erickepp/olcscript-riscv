class Generator:
    def __init__(self):
        self.temporal = 0x10000000
        self.label = 0
        self.code = []
        self.data = []
        self.final_code = []
        self.natives = []
        self.func_code = []
        self.temp_list = []
        self.print_string_flag = True
        self.concat_string_flag = True
        self.break_label = ''
        self.continue_label = ''
        self.main_code = False

    def get_code(self):
        return self.code

    def get_final_code(self):
        self.add_headers()
        self.add_footers()
        outstring = ''.join(self.code)
        return outstring

    def get_temps(self):
        return self.temp_list

    def add_break(self, lbl):
        self.break_label = lbl

    def add_code(self, code):
        self.code.append(code)
    
    def add_data_code(self, code):
        self.data.append(code)

    def add_continue(self, lbl):
        self.continue_label = lbl

    def new_temp(self):
        self.temporal += 4
        return self.temporal

    def new_label(self):
        temp = self.label
        self.label += 1
        return f'L{temp}'

    def add_br(self):
        self.code.append('\n')

    def comment(self, txt):
        self.code.append(f'### {txt}\n')

    def variable_data(self, name, type, value):
        self.data.append(f'{name}: .{type} {value}\n')

    def add_li(self, left, right):
        self.code.append(f'\tli {left}, {right}\n')

    def add_la(self, left, right):
        self.code.append(f'\tla {left}, {right}\n')

    def add_lw(self, left, right):
        self.code.append(f'\tlw {left}, {right}\n')

    def add_sw(self, left, right):
        self.code.append(f'\tsw {left}, {right}\n')

    def add_slli(self, target, left, right):
        self.code.append(f'\tslli {target}, {left}, {right}\n')

    def add_blt(self, left, right, target):
        self.code.append(f'\tblt {left}, {right}, {target}\n')

    def add_bgt(self, left, right, target):
        self.code.append(f'\tbgt {left}, {right}, {target}\n')

    def add_bge(self, left, right, target):
        self.code.append(f'\tbge {left}, {right}, {target}\n')

    def add_blez(self, left, right, target):
        self.code.append(f'\tblez {left}, {right}, {target}\n')

    def add_beq(self, left, right, target):
        self.code.append(f'\tbeq {left}, {right}, {target}\n')

    def add_bne(self, left, right, target):
        self.code.append(f'\tbne {left}, {right}, {target}\n')

    def add_jump(self, lbl):
        self.code.append(f'\tj {lbl}\n')

    def new_body_label(self, lbl):
        self.code.append(f'\n{lbl}:\n')

    def add_move(self, left, right):
        self.code.append(f'\tmv {left}, {right}\n')
    
    def add_lb(self, left, right):
        self.code.append(f'\tlb {left}, {right}\n')
    
    def add_seqz(self, left, right):
        self.code.append(f'\tseqz {left}, {right}\n')
    
    def add_snez(self, left, right):
        self.code.append(f'\tsnez {left}, {right}\n')
    
    def add_neg(self, left, right):
        self.code.append(f'\tneg {left}, {right}\n')
    
    def add_flw(self, target, left, right):
        self.code.append(f'\tflw {target}, {left}, {right}\n')
    
    def add_fsw(self, target, left, right):
        self.code.append(f'\tfsw {target}, {left}, {right}\n')
    
    def add_fcvt_s_w(self, left, right):
        self.code.append(f'\tfcvt.s.w {left}, {right}\n')
    
    def add_fneg_s(self, left, right):
        self.code.append(f'\tfneg.s {left}, {right}\n')

    def add_operation(self, operation, target, left, right):
        self.code.append(f'\t{operation} {target}, {left}, {right}\n')

    def add_system_call(self):
        self.code.append('\tecall\n')

    def add_headers(self):
        self.code.insert(0, '\n.text\n.globl _start\n\n_start:')
        self.data.insert(0, '.data\n')
        self.data.insert(1, 'str_false: .string "false"\n')
        self.data.insert(2, 'str_true: .string "true"\n')
        self.data.insert(3, 'str_null: .string "null"\n')
        self.code[:0] = self.data
            
    def add_footers(self):
        self.code.append('\n\tli a0, 0\n')
        self.code.append('\tli a7, 93\n')
        self.code.append('\tecall\n')
