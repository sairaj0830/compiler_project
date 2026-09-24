from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import traceback

from compiler.lexer import Lexer, LexicalError
from compiler.parser import Parser, SyntaxError
from compiler.semantic import SemanticAnalyzer, SemanticError
from compiler.ir_generator import IRGenerator
from compiler.optimizer import Optimizer
from compiler.code_gen import CodeGen
from compiler.vm import StackVM
from ai_assistant.llm_service import explain_error, explain_optimization

app = FastAPI(title="Intelligent Compiler API")

# Configure CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompileRequest(BaseModel):
    code: str
    optimize: bool = False

@app.post("/api/compile")
async def compile_code(req: CompileRequest):
    code = req.code
    response_data = {
        "tokens": [],
        "tac_unoptimized": [],
        "tac_optimized": [],
        "assembly": [],
        "output": [],
        "error": None,
        "ai_explanation": None
    }
    
    try:
        # Phase 1: Lexical Analysis
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        response_data["tokens"] = [{"type": t.type, "value": t.value, "line": t.line} for t in tokens if t.type != 'EOF']
        
        # Phase 2: Syntax Analysis
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Phase 3: Semantic Analysis
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        # Phase 4: IR Generation
        ir_gen = IRGenerator()
        tac = ir_gen.generate(ast)
        response_data["tac_unoptimized"] = [instr.to_dict() for instr in tac]
        
        # Phase 5: Optimization
        opt = Optimizer()
        tac_opt = opt.optimize(tac) if req.optimize else tac
        response_data["tac_optimized"] = [instr.to_dict() for instr in tac_opt]
        
        if req.optimize and tac != tac_opt:
            response_data["ai_explanation"] = explain_optimization(tac, tac_opt)
        
        # Phase 6: Code Generation
        cg = CodeGen()
        assembly = cg.generate(tac_opt)
        response_data["assembly"] = [f"{instr[0]} {instr[1] if instr[1] is not None else ''}".strip() for instr in assembly]
        
        # Phase 7: VM Execution
        vm = StackVM()
        output = vm.execute(assembly)
        response_data["output"] = output
        
    except (LexicalError, SyntaxError, SemanticError) as e:
        error_msg = f"{type(e).__name__}: {e.message}"
        response_data["error"] = error_msg
        response_data["ai_explanation"] = explain_error(code, error_msg)
    except Exception as e:
        error_msg = f"Internal Compiler Error: {str(e)}"
        response_data["error"] = error_msg
        traceback.print_exc()
        
    return response_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
