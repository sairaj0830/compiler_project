from .ir_generator import TACInstruction
from typing import List

class Optimizer:
    def __init__(self):
        pass

    def optimize(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        # Run multiple passes until no more changes (simple fixed-point)
        changed = True
        while changed:
            original_len = len(instructions)
            instructions = self.constant_folding(instructions)
            instructions = self.dead_code_elimination(instructions)
            
            # If length changed or we want a deeper equality check
            changed = len(instructions) < original_len
            
        return instructions

    def constant_folding(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        optimized = []
        constants = {} # map temp -> value
        
        for instr in instructions:
            # Substitute known constants
            arg1 = instr.arg1
            arg2 = instr.arg2
            if arg1 in constants: arg1 = constants[arg1]
            if arg2 in constants: arg2 = constants[arg2]
            
            if instr.op in ('+', '-', '*', '/'):
                if str(arg1).lstrip('-').isdigit() and str(arg2).lstrip('-').isdigit():
                    val1 = int(arg1)
                    val2 = int(arg2)
                    result = 0
                    if instr.op == '+': result = val1 + val2
                    elif instr.op == '-': result = val1 - val2
                    elif instr.op == '*': result = val1 * val2
                    elif instr.op == '/' and val2 != 0: result = val1 // val2
                    else:
                        optimized.append(instr)
                        continue
                        
                    constants[instr.result] = str(result)
                    optimized.append(TACInstruction('ASSIGN', str(result), None, instr.result))
                    continue
                    
            elif instr.op == 'ASSIGN':
                if str(arg1).lstrip('-').isdigit() and str(instr.result).startswith('t'):
                    constants[instr.result] = str(arg1)
            
            instr.arg1 = arg1
            instr.arg2 = arg2
            optimized.append(instr)
            
        return optimized

    def dead_code_elimination(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        # Simple DCE: remove assignments to temporaries that are never used subsequently
        used = set()
        for instr in instructions:
            if instr.arg1 and str(instr.arg1).startswith('t'):
                used.add(instr.arg1)
            if instr.arg2 and str(instr.arg2).startswith('t'):
                used.add(instr.arg2)
        
        optimized = []
        for instr in instructions:
            if instr.op == 'ASSIGN' and instr.result.startswith('t') and instr.result not in used:
                continue # Dead code
            optimized.append(instr)
        return optimized
