import pytest
from backend.compiler.lexer import Lexer
from backend.compiler.parser import Parser
from backend.compiler.ir_generator import IRGenerator

def generate_tac(code):
    lexer = Lexer(code)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    generator = IRGenerator()
    return generator.generate(ast)

def test_ir_basic_math():
    tac = generate_tac("int x = 5 + 3;")
    assert len(tac) == 2
    assert tac[0].op == '+'
    assert tac[0].arg1 == '5'
    assert tac[0].arg2 == '3'
    assert tac[0].result == 't1'
    assert tac[1].op == 'ASSIGN'
    assert tac[1].arg1 == 't1'
    assert tac[1].result == 'x'

def test_ir_if():
    tac = generate_tac("if (x > 0) { y = 1; }")
    assert len(tac) == 4
    assert tac[0].op == '>'
    assert tac[1].op == 'IF_FALSE_GOTO'
    assert tac[2].op == 'ASSIGN'
    assert tac[3].op == 'LABEL'
