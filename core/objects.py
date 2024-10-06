class VarAssign:
    def __init__(self, token, type, initialize=False):
        self.type = type
        self.name = token[0]
        self.value = token[1][:]
        self.codeblock = []
        self.initialize = initialize

class FuncCall:
    def __init__(self, token, type):
        self.type = type
        self.name = token[0][1]
        self.args = token[2:-1]
        self.codeblock = []

class Func():
    def __init__(self, token, type):
        self.type = type
        self.name = token[1][1]
        self.value = token[3:-2]
        self.codeblock = []

class Return():
    def __init__(self, token, type):
        self.type = type
        self.name = token[0][1]
        self.value = token[1:]
        self.codeblock = []

class Error:
    def __init__(self, type):
        self.type = type
        self.name = type.lower()
        self.codeblock = []

class Conditions():
    def __init__(self, token, type):
        self.type = type
        self.value = token[1:-1]
        self.codeblock = []

class Loops():
    def __init__(self, token, type):
        self.type = type
        self.value = []
        if self.type == 'FOR': self.for_loop(token)
        else: self.while_loop(token)
        self.codeblock = []

    def while_loop(self, token):
        self.value = token[1:-1]
    
    def for_loop(self, token):
        self.value = [token[1]] + token[3:-1]