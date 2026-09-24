import pytest
from backend.compiler.lexer import Lexer
from backend.compiler.parser import Parser
from backend.compiler.semantic import SemanticAnalyzer
from backend.compiler.ir_generator import IRGenerator
from backend.compiler.optimizer import Optimizer
from backend.compiler.code_gen import CodeGen
from backend.compiler.vm import StackVM

def run_program(code, optimize=False):
    lexer = Lexer(code)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    ir_gen = IRGenerator()
    tac = ir_gen.generate(ast)
    
    if optimize:
        opt = Optimizer()
        tac = opt.optimize(tac)
        
    cg = CodeGen()
    assembly = cg.generate(tac)
    
    vm = StackVM()
    return vm.execute(assembly)

def test_full_pipeline_factorial():
    code = """
    int n = 5;
    int result = 1;
    while (n > 0) {
        result = result * n;
        n = n - 1;
    }
    print(result);
    """
    output = run_program(code)
    assert output == ["120"]

def test_optimization():
    code = """
    int x = 5 * 2;
    int y = x + 10;
    print(y);
    """
    output_unopt = run_program(code, optimize=False)
    output_opt = run_program(code, optimize=True)
    assert output_unopt == ["20"]
    assert output_opt == ["20"]
