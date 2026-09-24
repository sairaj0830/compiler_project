import pytest
from backend.compiler.lexer import Lexer
from backend.compiler.parser import Parser, SyntaxError
from backend.compiler.ast_nodes import *

def parse(code):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()

def test_parser_var_decl():
    ast = parse("int x = 10;")
    assert len(ast.statements) == 1
    decl = ast.statements[0]
    assert isinstance(decl, VarDeclNode)
    assert decl.var_type == 'int'
    assert decl.id == 'x'
    assert isinstance(decl.expr, LiteralNode)
    assert decl.expr.value == 10

def test_parser_assignment():
    ast = parse("x = y + 5;")
    assert len(ast.statements) == 1
    assign = ast.statements[0]
    assert isinstance(assign, AssignNode)
    assert assign.id == 'x'
    assert isinstance(assign.expr, BinOpNode)
    assert assign.expr.op == '+'

def test_parser_if_statement():
    ast = parse("if (x > 0) { print(x); } else { print(0); }")
    assert len(ast.statements) == 1
    if_node = ast.statements[0]
    assert isinstance(if_node, IfNode)
    assert isinstance(if_node.condition, BinOpNode)
    assert len(if_node.then_block.statements) == 1
    assert len(if_node.else_block.statements) == 1

def test_parser_while_statement():
    ast = parse("while (x < 10) { x = x + 1; }")
    assert len(ast.statements) == 1
    while_node = ast.statements[0]
    assert isinstance(while_node, WhileNode)
    assert isinstance(while_node.condition, BinOpNode)
    assert len(while_node.block.statements) == 1

def test_parser_error():
    with pytest.raises(SyntaxError):
        parse("int x = ;")
