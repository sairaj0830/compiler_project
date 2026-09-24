from .ast_nodes import *
from .symbol_table import SymbolTable, SymbolError

class SemanticError(Exception):
    def __init__(self, message, line):
        super().__init__(f"{message} at line {line}")
        self.message = message
        self.line = line

class SemanticAnalyzer:
    def __init__(self):
        self.symtab = SymbolTable()

    def analyze(self, node: ASTNode):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: ASTNode):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_ProgramNode(self, node: ProgramNode):
        for stmt in node.statements:
            self.analyze(stmt)

    def visit_BlockNode(self, node: BlockNode):
        self.symtab.enter_scope()
        for stmt in node.statements:
            self.analyze(stmt)
        self.symtab.exit_scope()

    def visit_VarDeclNode(self, node: VarDeclNode):
        expr_type = self.analyze(node.expr)
        if expr_type != node.var_type:
            raise SemanticError(f"Type mismatch: cannot assign {expr_type} to {node.var_type}", node.line)
        try:
            self.symtab.declare(node.id, node.var_type, node.line)
        except SymbolError as e:
            raise SemanticError(e.message, e.line)

    def visit_AssignNode(self, node: AssignNode):
        try:
            var_info = self.symtab.lookup(node.id, node.line)
        except SymbolError as e:
            raise SemanticError(e.message, e.line)
        expr_type = self.analyze(node.expr)
        if var_info['type'] != expr_type:
            raise SemanticError(f"Type mismatch: cannot assign {expr_type} to {var_info['type']}", node.line)
        return var_info['type']

    def visit_IfNode(self, node: IfNode):
        cond_type = self.analyze(node.condition)
        if cond_type != 'bool':
            raise SemanticError(f"Condition must be bool, got {cond_type}", node.line)
        self.analyze(node.then_block)
        if node.else_block:
            self.analyze(node.else_block)

    def visit_WhileNode(self, node: WhileNode):
        cond_type = self.analyze(node.condition)
        if cond_type != 'bool':
            raise SemanticError(f"Condition must be bool, got {cond_type}", node.line)
        self.analyze(node.block)

    def visit_PrintNode(self, node: PrintNode):
        self.analyze(node.expr)

    def visit_BinOpNode(self, node: BinOpNode):
        left_type = self.analyze(node.left)
        right_type = self.analyze(node.right)
        
        if node.op in ('+', '-', '*', '/'):
            if left_type != 'int' or right_type != 'int':
                raise SemanticError(f"Operands for '{node.op}' must be int, got {left_type} and {right_type}", node.line)
            return 'int'
        elif node.op in ('<', '>', '==', '!='):
            if left_type != right_type:
                raise SemanticError(f"Operands for '{node.op}' must be of same type, got {left_type} and {right_type}", node.line)
            return 'bool'
        elif node.op in ('&&', '||'):
            if left_type != 'bool' or right_type != 'bool':
                raise SemanticError(f"Operands for '{node.op}' must be bool, got {left_type} and {right_type}", node.line)
            return 'bool'

    def visit_UnaryOpNode(self, node: UnaryOpNode):
        expr_type = self.analyze(node.expr)
        if node.op == '!':
            if expr_type != 'bool':
                raise SemanticError(f"Operand for '!' must be bool, got {expr_type}", node.line)
            return 'bool'

    def visit_LiteralNode(self, node: LiteralNode):
        return node.type

    def visit_IdentifierNode(self, node: IdentifierNode):
        try:
            var_info = self.symtab.lookup(node.name, node.line)
            return var_info['type']
        except SymbolError as e:
            raise SemanticError(e.message, e.line)
