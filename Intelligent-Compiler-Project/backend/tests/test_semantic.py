import pytest
from backend.compiler.lexer import Lexer
from backend.compiler.parser import Parser
from backend.compiler.semantic import SemanticAnalyzer, SemanticError

def analyze(code):
    lexer = Lexer(code)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    return analyzer

def test_semantic_var_decl():
    # Should not raise exception
    analyze("int x = 10; bool y = true;")

def test_semantic_type_mismatch_decl():
    with pytest.raises(SemanticError, match="Type mismatch"):
        analyze("int x = true;")

def test_semantic_undeclared_var():
    with pytest.raises(SemanticError, match="Undeclared variable 'y'"):
        analyze("x = y + 5;")

def test_semantic_scope():
    code = """
    int x = 10;
    if (x > 0) {
        int y = 20;
    }
    x = y; // y should be undeclared here
    """
    with pytest.raises(SemanticError, match="Undeclared variable 'y'"):
        analyze(code)

def test_semantic_binop_type():
    with pytest.raises(SemanticError):
        analyze("int x = 10 + true;")
