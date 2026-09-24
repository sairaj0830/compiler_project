class SymbolError(Exception):
    def __init__(self, message, line=None):
        super().__init__(message)
        self.message = message
        self.line = line

class SymbolTable:
    def __init__(self):
        # A list of dictionaries representing scopes
        self.scopes = [{}]
        self.offset = 0

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise SymbolError("Cannot exit global scope")

    def declare(self, name, var_type, line=None):
        current_scope = self.scopes[-1]
        if name in current_scope:
            raise SymbolError(f"Variable '{name}' already declared in this scope", line)
        current_scope[name] = {'type': var_type, 'offset': self.offset}
        self.offset += 1

    def lookup(self, name, line=None):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise SymbolError(f"Undeclared variable '{name}'", line)
