from .ir_generator import TACInstruction
from typing import List, Tuple

class CodeGen:
    def __init__(self):
        self.assembly = []

    def generate(self, instructions: List[TACInstruction]) -> List[Tuple[str, str]]:
        for instr in instructions:
            if instr.op == 'LABEL':
                self.assembly.append(('LABEL', instr.result))
            elif instr.op == 'ASSIGN':
                if str(instr.arg1).lstrip('-').isdigit() or str(instr.arg1) in ('true', 'false'):
                    self.assembly.append(('PUSH', instr.arg1))
                else:
                    self.assembly.append(('LOAD', instr.arg1))
                self.assembly.append(('STORE', instr.result))
            elif instr.op == 'GOTO':
                self.assembly.append(('JMP', instr.result))
            elif instr.op == 'IF_FALSE_GOTO':
                if str(instr.arg1).lstrip('-').isdigit() or str(instr.arg1) in ('true', 'false'):
                    self.assembly.append(('PUSH', instr.arg1))
                else:
                    self.assembly.append(('LOAD', instr.arg1))
                self.assembly.append(('JMP_IF_FALSE', instr.result))
            elif instr.op == 'PRINT':
                if str(instr.arg1).lstrip('-').isdigit() or str(instr.arg1) in ('true', 'false'):
                    self.assembly.append(('PUSH', instr.arg1))
                else:
                    self.assembly.append(('LOAD', instr.arg1))
                self.assembly.append(('PRINT', None))
            elif instr.op in ('+', '-', '*', '/', '==', '!=', '<', '>', '&&', '||'):
                if str(instr.arg1).lstrip('-').isdigit() or str(instr.arg1) in ('true', 'false'):
                    self.assembly.append(('PUSH', instr.arg1))
                else:
                    self.assembly.append(('LOAD', instr.arg1))
                
                if str(instr.arg2).lstrip('-').isdigit() or str(instr.arg2) in ('true', 'false'):
                    self.assembly.append(('PUSH', instr.arg2))
                else:
                    self.assembly.append(('LOAD', instr.arg2))
                
                op_map = {
                    '+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV',
                    '==': 'CMP_EQ', '!=': 'CMP_NEQ', '<': 'CMP_LT', '>': 'CMP_GT',
                    '&&': 'AND', '||': 'OR'
                }
                self.assembly.append((op_map[instr.op], None))
                self.assembly.append(('STORE', instr.result))
            elif instr.op == '!':
                if str(instr.arg1).lstrip('-').isdigit() or str(instr.arg1) in ('true', 'false'):
                    self.assembly.append(('PUSH', instr.arg1))
                else:
                    self.assembly.append(('LOAD', instr.arg1))
                self.assembly.append(('NOT', None))
                self.assembly.append(('STORE', instr.result))
        return self.assembly
