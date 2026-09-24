import pytest
from backend.compiler.lexer import Lexer, LexicalError

def test_lexer_basic_tokens():
    code = "int x = 10;"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    assert len(tokens) == 6
    assert tokens[0].type == 'INT'
    assert tokens[1].type == 'ID'
    assert tokens[1].value == 'x'
    assert tokens[2].type == 'ASSIGN'
    assert tokens[3].type == 'NUMBER'
    assert tokens[3].value == '10'
    assert tokens[4].type == 'SEMI'
    assert tokens[5].type == 'EOF'

def test_lexer_keywords():
    code = "if else while print true false bool int"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    types = [t.type for t in tokens]
    assert types == ['IF', 'ELSE', 'WHILE', 'PRINT', 'TRUE', 'FALSE', 'BOOL', 'INT', 'EOF']

def test_lexer_operators():
    code = "+ - * / == != < > && || !"
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    types = [t.type for t in tokens]
    assert types == ['PLUS', 'MINUS', 'MUL', 'DIV', 'EQ', 'NEQ', 'LT', 'GT', 'AND', 'OR', 'NOT', 'EOF']

def test_lexer_error():
    code = "int x = 10 @;"
    lexer = Lexer(code)
    with pytest.raises(LexicalError):
        lexer.tokenize()
