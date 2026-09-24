from .lexer import Token, LexicalError
from .ast_nodes import *
from typing import List

class SyntaxError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"{message} at line {line}, column {column}")
        self.message = message
        self.line = line
        self.column = column

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def consume(self, expected_type: str):
        token = self.current_token()
        if token.type == expected_type:
            self.pos += 1
            return token
        else:
            raise SyntaxError(f"Expected {expected_type}, got {token.type}", token.line, token.column)

    def match(self, expected_type: str) -> bool:
        if self.current_token().type == expected_type:
            self.pos += 1
            return True
        return False

    def parse(self) -> ProgramNode:
        statements = []
        while self.current_token().type != 'EOF':
            statements.append(self.parse_statement())
        return ProgramNode(statements)

    def parse_statement(self) -> ASTNode:
        token = self.current_token()
        if token.type in ('INT', 'BOOL'):
            return self.parse_var_decl()
        elif token.type == 'ID':
            return self.parse_assignment()
        elif token.type == 'IF':
            return self.parse_if_stmt()
        elif token.type == 'WHILE':
            return self.parse_while_stmt()
        elif token.type == 'PRINT':
            return self.parse_print_stmt()
        elif token.type == 'LBRACE':
            return self.parse_block()
        else:
            raise SyntaxError(f"Unexpected token {token.type}", token.line, token.column)

    def parse_block(self) -> BlockNode:
        self.consume('LBRACE')
        statements = []
        while self.current_token().type not in ('RBRACE', 'EOF'):
            statements.append(self.parse_statement())
        self.consume('RBRACE')
        return BlockNode(statements)

    def parse_var_decl(self) -> VarDeclNode:
        type_token = self.current_token()
        self.pos += 1 # Consume INT or BOOL
        id_token = self.consume('ID')
        self.consume('ASSIGN')
        expr = self.parse_expression()
        self.consume('SEMI')
        return VarDeclNode(type_token.value, id_token.value, expr, type_token.line)

    def parse_assignment(self) -> AssignNode:
        id_token = self.consume('ID')
        self.consume('ASSIGN')
        expr = self.parse_expression()
        self.consume('SEMI')
        return AssignNode(id_token.value, expr, id_token.line)

    def parse_if_stmt(self) -> IfNode:
        if_token = self.consume('IF')
        self.consume('LPAREN')
        condition = self.parse_expression()
        self.consume('RPAREN')
        then_block = self.parse_block()
        else_block = None
        if self.match('ELSE'):
            else_block = self.parse_block()
        return IfNode(condition, then_block, else_block, if_token.line)

    def parse_while_stmt(self) -> WhileNode:
        while_token = self.consume('WHILE')
        self.consume('LPAREN')
        condition = self.parse_expression()
        self.consume('RPAREN')
        block = self.parse_block()
        return WhileNode(condition, block, while_token.line)
        
    def parse_print_stmt(self) -> PrintNode:
        print_token = self.consume('PRINT')
        self.consume('LPAREN')
        expr = self.parse_expression()
        self.consume('RPAREN')
        self.consume('SEMI')
        return PrintNode(expr, print_token.line)

    def parse_expression(self) -> ASTNode:
        return self.parse_logical_or()

    def parse_logical_or(self) -> ASTNode:
        node = self.parse_logical_and()
        while self.current_token().type == 'OR':
            op = self.consume('OR')
            right = self.parse_logical_and()
            node = BinOpNode(node, op.value, right, op.line)
        return node

    def parse_logical_and(self) -> ASTNode:
        node = self.parse_relational()
        while self.current_token().type == 'AND':
            op = self.consume('AND')
            right = self.parse_relational()
            node = BinOpNode(node, op.value, right, op.line)
        return node

    def parse_relational(self) -> ASTNode:
        node = self.parse_additive()
        if self.current_token().type in ('LT', 'GT', 'EQ', 'NEQ'):
            op = self.current_token()
            self.pos += 1
            right = self.parse_additive()
            node = BinOpNode(node, op.value, right, op.line)
        return node

    def parse_additive(self) -> ASTNode:
        node = self.parse_term()
        while self.current_token().type in ('PLUS', 'MINUS'):
            op = self.current_token()
            self.pos += 1
            right = self.parse_term()
            node = BinOpNode(node, op.value, right, op.line)
        return node

    def parse_term(self) -> ASTNode:
        node = self.parse_factor()
        while self.current_token().type in ('MUL', 'DIV'):
            op = self.current_token()
            self.pos += 1
            right = self.parse_factor()
            node = BinOpNode(node, op.value, right, op.line)
        return node

    def parse_factor(self) -> ASTNode:
        token = self.current_token()
        if token.type == 'NUMBER':
            self.pos += 1
            return LiteralNode(int(token.value), 'int', token.line)
        elif token.type in ('TRUE', 'FALSE'):
            self.pos += 1
            val = True if token.type == 'TRUE' else False
            return LiteralNode(val, 'bool', token.line)
        elif token.type == 'ID':
            self.pos += 1
            return IdentifierNode(token.value, token.line)
        elif token.type == 'LPAREN':
            self.pos += 1
            node = self.parse_expression()
            self.consume('RPAREN')
            return node
        elif token.type == 'NOT':
            self.pos += 1
            node = self.parse_factor()
            return UnaryOpNode('!', node, token.line)
        else:
            raise SyntaxError(f"Unexpected token in expression: {token.type}", token.line, token.column)
