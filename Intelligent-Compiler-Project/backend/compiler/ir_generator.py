from .ast_nodes import *

class TACInstruction:
    def __init__(self, op, arg1, arg2, result):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __str__(self):
        if self.op == 'ASSIGN':
            return f"{self.result} = {self.arg1}"
        elif self.op == 'IF_GOTO':
            return f"IF {self.arg1} GOTO {self.result}"
        elif self.op == 'IF_FALSE_GOTO':
            return f"IF_FALSE {self.arg1} GOTO {self.result}"
        elif self.op == 'GOTO':
            return f"GOTO {self.result}"
        elif self.op == 'LABEL':
            return f"{self.result}:"
        elif self.op == 'PRINT':
            return f"PRINT {self.arg1}"
        else:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"

    def to_dict(self):
        return {
            "op": self.op,
            "arg1": self.arg1,
            "arg2": self.arg2,
            "result": self.result,
            "str": str(self)
        }

class IRGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def generate(self, node: ASTNode):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: ASTNode):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_ProgramNode(self, node: ProgramNode):
        for stmt in node.statements:
            self.generate(stmt)
        return self.instructions

    def visit_BlockNode(self, node: BlockNode):
        for stmt in node.statements:
            self.generate(stmt)

    def visit_VarDeclNode(self, node: VarDeclNode):
        expr_result = self.generate(node.expr)
        self.instructions.append(TACInstruction('ASSIGN', expr_result, None, node.id))

    def visit_AssignNode(self, node: AssignNode):
        expr_result = self.generate(node.expr)
        self.instructions.append(TACInstruction('ASSIGN', expr_result, None, node.id))
        return node.id

    def visit_IfNode(self, node: IfNode):
        cond_result = self.generate(node.condition)
        l_else = self.new_label()
        l_end = self.new_label()
        
        self.instructions.append(TACInstruction('IF_FALSE_GOTO', cond_result, None, l_else))
        self.generate(node.then_block)
        
        if node.else_block:
            self.instructions.append(TACInstruction('GOTO', None, None, l_end))
        
        self.instructions.append(TACInstruction('LABEL', None, None, l_else))
        
        if node.else_block:
            self.generate(node.else_block)
            self.instructions.append(TACInstruction('LABEL', None, None, l_end))

    def visit_WhileNode(self, node: WhileNode):
        l_start = self.new_label()
        l_end = self.new_label()
        
        self.instructions.append(TACInstruction('LABEL', None, None, l_start))
        cond_result = self.generate(node.condition)
        self.instructions.append(TACInstruction('IF_FALSE_GOTO', cond_result, None, l_end))
        
        self.generate(node.block)
        self.instructions.append(TACInstruction('GOTO', None, None, l_start))
        
        self.instructions.append(TACInstruction('LABEL', None, None, l_end))

    def visit_PrintNode(self, node: PrintNode):
        expr_result = self.generate(node.expr)
        self.instructions.append(TACInstruction('PRINT', expr_result, None, None))

    def visit_BinOpNode(self, node: BinOpNode):
        left_result = self.generate(node.left)
        right_result = self.generate(node.right)
        t = self.new_temp()
        self.instructions.append(TACInstruction(node.op, left_result, right_result, t))
        return t

    def visit_UnaryOpNode(self, node: UnaryOpNode):
        expr_result = self.generate(node.expr)
        t = self.new_temp()
        self.instructions.append(TACInstruction(node.op, expr_result, None, t))
        return t

    def visit_LiteralNode(self, node: LiteralNode):
        if node.type == 'bool':
            return str(node.value).lower()
        return str(node.value)

    def visit_IdentifierNode(self, node: IdentifierNode):
        return node.name
