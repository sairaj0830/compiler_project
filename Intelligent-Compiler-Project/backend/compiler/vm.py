class StackVM:
    def __init__(self):
        self.stack = []
        self.memory = {}
        self.pc = 0
        self.output = []

    def execute(self, instructions):
        # instructions is a list of tuples: (opcode, arg)
        # e.g., ("PUSH", 5), ("STORE", "x"), ("LABEL", "L1")
        
        # Build label map
        labels = {}
        for i, instr in enumerate(instructions):
            if instr[0] == "LABEL":
                labels[instr[1]] = i

        self.pc = 0
        while self.pc < len(instructions):
            instr = instructions[self.pc]
            op = instr[0]
            arg = instr[1] if len(instr) > 1 else None

            if op == "PUSH":
                if str(arg).lstrip('-').isdigit():
                    self.stack.append(int(arg))
                else:
                    self.stack.append(True if arg == 'true' else False)
            elif op == "LOAD":
                self.stack.append(self.memory.get(arg, 0))
            elif op == "STORE":
                self.memory[arg] = self.stack.pop()
            elif op == "ADD":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
            elif op == "SUB":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
            elif op == "MUL":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
            elif op == "DIV":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a // b)
            elif op == "CMP_EQ":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a == b)
            elif op == "CMP_NEQ":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a != b)
            elif op == "CMP_LT":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a < b)
            elif op == "CMP_GT":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a > b)
            elif op == "AND":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(bool(a) and bool(b))
            elif op == "OR":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(bool(a) or bool(b))
            elif op == "NOT":
                a = self.stack.pop()
                self.stack.append(not bool(a))
            elif op == "JMP":
                self.pc = labels[arg]
            elif op == "JMP_IF_FALSE":
                cond = self.stack.pop()
                if not cond:
                    self.pc = labels[arg]
            elif op == "PRINT":
                val = self.stack.pop()
                self.output.append(str(val))
            
            self.pc += 1
            
        return self.output
