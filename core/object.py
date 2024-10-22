class dynamicVar:
    def __init__(self, token, type):
        self.type = type
        self.name = token[0]
        self.value = token[1][:]
        self.codeblock = []

class staticVar:
    def __init__(self, dt, token, type):
        self.type = type
        self.datatype = dt
        self.name = token[0]
        self.value = token[1][:]
        self.codeblock = []

class Conditions:
    def __init__(self, token, type):
        self.type = type
        self.value = token[1:-1]
        self.codeblock = []
        self.var = {'static': set(), 'dynamic': set()}

class Loops:
    def __init__(self, token, type):
        self.type = type
        self.value = token[1:-1]
        self.codeblock = []
        self.var = {'static': set(), 'dynamic': set()}

class funccall:
    def __init__(self, token, type):
        self.type = type
        self.name = token[0][1]
        self.value = token[1:]
        self.codeblock = []

class dynamicFunc:
    def __init__(self, token, type):
        self.type = type
        self.name = token[1][1]
        self.args = token[3:-2]
        self.codeblock = []
        self.var = {'static': set(), 'dynamic': set()}
        for var in self.varlist(token[3:-2]):
            self.var['dynamic'].add(var)

    def varlist(self, token):
        var = []
        for t in token:
            if t[0] == 'NAME':
                var.append(t[1])
        return var
    
class Return:
    def __init__(self, token, type):
        self.type = type
        self.value = token[1:]
        self.codeblock = []

class Node:
    def __init__(self, token, type):
        self.type = type
        self.name = token[0][1]
        self.call = token[2:]
        self.codeblock = []