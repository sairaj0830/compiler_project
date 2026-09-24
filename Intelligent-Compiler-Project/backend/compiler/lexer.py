import re
from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"

class LexicalError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"{message} at line {line}, column {column}")
        self.message = message
        self.line = line
        self.column = column

class Lexer:
    # Token specification ordered by precedence
    TOKEN_SPEC = [
        ('COMMENT',  r'//.*'),
        ('NUMBER',   r'\d+'),
        ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('EQ',       r'=='),
        ('NEQ',      r'!='),
        ('AND',      r'&&'),
        ('OR',       r'\|\|'),
        ('ASSIGN',   r'='),
        ('LT',       r'<'),
        ('GT',       r'>'),
        ('PLUS',     r'\+'),
        ('MINUS',    r'-'),
        ('MUL',      r'\*'),
        ('DIV',      r'/'),
        ('NOT',      r'!'),
        ('LPAREN',   r'\('),
        ('RPAREN',   r'\)'),
        ('LBRACE',   r'\{'),
        ('RBRACE',   r'\}'),
        ('SEMI',     r';'),
        ('WS',       r'[ \t]+'),
        ('NEWLINE',  r'\n'),
        ('MISMATCH', r'.'),
    ]

    KEYWORDS = {'int', 'bool', 'if', 'else', 'while', 'print', 'true', 'false'}

    def __init__(self, code: str):
        self.code = code
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.TOKEN_SPEC)
        self.get_token = re.compile(tok_regex).match
        self.line_num = 1
        self.line_start = 0

    def tokenize(self) -> List[Token]:
        tokens = []
        pos = 0
        mo = self.get_token(self.code, pos)
        
        while mo is not None:
            kind = mo.lastgroup
            value = mo.group(kind)
            column = mo.start() - self.line_start + 1

            if kind == 'NEWLINE':
                self.line_start = mo.end()
                self.line_num += 1
            elif kind == 'WS' or kind == 'COMMENT':
                pass # Ignore whitespace and comments
            elif kind == 'MISMATCH':
                raise LexicalError(f"Unexpected character '{value}'", self.line_num, column)
            else:
                if kind == 'ID' and value in self.KEYWORDS:
                    kind = value.upper() # Keywords become their own token type (e.g. 'int' -> 'INT')
                tokens.append(Token(kind, value, self.line_num, column))
            
            pos = mo.end()
            mo = self.get_token(self.code, pos)
            
        if pos != len(self.code):
            raise LexicalError(f"Unexpected character '{self.code[pos]}'", self.line_num, pos - self.line_start + 1)
            
        tokens.append(Token('EOF', '', self.line_num, pos - self.line_start + 1))
        return tokens

# Small test snippet to verify functionality if run directly
if __name__ == '__main__':
    code = '''
    // This is a test
    int x = 10;
    while (x > 0) {
        x = x - 1;
    }
    '''
    lexer = Lexer(code)
    try:
        tokens = lexer.tokenize()
        for t in tokens:
            print(t)
    except LexicalError as e:
        print(f"Error: {e}")
