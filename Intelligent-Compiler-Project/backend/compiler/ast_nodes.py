from dataclasses import dataclass
from typing import List, Optional, Any

class ASTNode:
    pass

@dataclass
class ProgramNode(ASTNode):
    statements: List[ASTNode]

@dataclass
class VarDeclNode(ASTNode):
    var_type: str
    id: str
    expr: ASTNode
    line: int

@dataclass
class AssignNode(ASTNode):
    id: str
    expr: ASTNode
    line: int

@dataclass
class IfNode(ASTNode):
    condition: ASTNode
    then_block: 'BlockNode'
    else_block: Optional['BlockNode']
    line: int

@dataclass
class WhileNode(ASTNode):
    condition: ASTNode
    block: 'BlockNode'
    line: int

@dataclass
class BlockNode(ASTNode):
    statements: List[ASTNode]

@dataclass
class PrintNode(ASTNode):
    expr: ASTNode
    line: int

@dataclass
class BinOpNode(ASTNode):
    left: ASTNode
    op: str
    right: ASTNode
    line: int

@dataclass
class UnaryOpNode(ASTNode):
    op: str
    expr: ASTNode
    line: int

@dataclass
class IdentifierNode(ASTNode):
    name: str
    line: int

@dataclass
class LiteralNode(ASTNode):
    value: Any
    type: str # 'int' or 'bool'
    line: int
