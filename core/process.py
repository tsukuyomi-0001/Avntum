import re
from .object import *
from .transpile import *

"""
2) global and local
making a variable in object named variable which stores
variables created inside of it

7) function - both static and dynamic for
this too we will make two more list that store 
static functions and dynamic functions

for args there are two position, and placeholder
a,b,c
a,b, c = 3

also args -> for that args x
"""

token = {
    "INTEND": r"<INTEND>",
    "NAME": r"\b[a-zA-Z][a-zA-Z0-9_]*\b",

    "int": r"int",
    "string": r"str",
    "float": r"float",
    
    "int16": r"int16",
    "int32": r"int32",
    "int64": r"int64",

    "float64": r"float64",
    "float128": r"float128",

    "STR1": r"'[^']*'",
    "STR2": r'"[^"]*"',
    "FLOAT": r'\b\d+\.\d+\b',
    "INT": r'\b\d+\b',

    "LPARAN": r'[\[\(\{]',
    "RPARAN": r'[\]\)\}]',

    "SPACE": r'\s+',
    "COMMENT": r'#',

    "EQUAL": r'==',
    "ASSIGN": r'=',
    "ADD": r'\+',
    "SUB": r'-',
    "DIV": r'/',
    "MUL": r'\*',

    "SMALLEQ": r'<=',
    "BIGEQ": r'>=',
    "NOTEQ": r'!=',
    "SMALL": r'<',
    "BIG": r'>',
    "INDT": r':$',
    "SEP": r',',
    'NODE': r'.',
}

types = '|'.join(f'(?P<{key}>{value})' for key,value in token.items())

def getValue(right):
    value = []
    partial_value = []
    count = 0
    for _ in right:
        if _[0] == 'LPARAN':
            partial_value.append(_)
            count+=1
        elif _[0] == 'RPARAN':
            count -=1
            partial_value.append(_)
        elif count == 0 and _[0] == 'SEP':
            value.append(partial_value)
            partial_value = []
        else:
            partial_value.append(_)
    value.append(partial_value)
    return value

def getName(left):
        names = []
        for _ in left:
            if _[0] == 'NAME': names.append(_[1])

        return names

def intendApply(line, index):
    if not line.startswith(' '): return line
    elif len(line)*' ' == line: return 'EMPTY'

    intend = '<INTEND>'
    tab_count = (len(line) - len(line.lstrip())) / 4
    line = line.lstrip()
    if tab_count.is_integer(): 
        for i in range(int(tab_count)): line = intend+line
    else:
        print(f'Intendation Error at line: {index+1}')
        return "TERM"

    return line

class Process():
    def __init__(self, codelines):
        self.ast = []
        self.static_var = set()
        self.dynamic_var = set()
        self.header = set()

        for index, line in enumerate(codelines):
            line = intendApply(line, index)
            if line == 'EMPTY': continue
            code = self.Lexer(line)
            if code == 'TERM' or line == 'TERM':
                break
    
    def importProcess(self, x):
        self.address = ''
        for token in x:
            if token[1] == '.':
                self.address += '/'
            else:
                self.address += token[1]
        with open(self.address + '.avm') as f:
            core = Process(f.readlines())
            Transpiler(core.ast, self.address+'.avm', core.dynamic_var, core.static_var, set(), import_file=True)
        
        self.header.add(self.address)

    def Lexer(self, line):
        token = []
        paran_count = 0
        for match in re.finditer(types, line):
            type = match.lastgroup
            value = match.group(type)
            if type == 'COMMENT': return 
            if type == 'SPACE': continue

            if 'PARAN' in type:
                if type.startswith('L'): 
                    token.append((type, paran_count))
                    paran_count+=1
                else: 
                    paran_count-=1
                    token.append((type, paran_count))
            elif type in ['STR1', 'STR2']: token.append(('STRING', value[1:][:-1]))
            else: token.append((type, value))

        if len(token) != 0:
                self.Parser(token)

    def TypeCheck(self, token):
        if token[0][1] == 'func':
            return 'dynamicFunc'
        elif ('ASSIGN', '=') in token:
            if token[0][1] in ['int', 'float', 'string', 'int16', 'int32', 'int64', 'float64', 'float128']:
                return 'staticVar'
            else:
                return 'dynamicVar'
        if token[0][1] == 'import':
            return 'import'
        elif token[0][1] in ['if', 'elif', 'else']:
            if token[0][1] == 'elif': return 'else if'
            else: return token[0][1]
        elif token[0][1] in ['while', 'for']:
            return token[0][1]
        elif token[0][0] == 'NAME' and token[1][0] == 'LPARAN':
            return 'funccall'
        elif token[0][1] == 'return': return 'return'
        elif ('NODE', ".") in token: 
            return 'node'
        
    def Parser(self, token):
        intends = token.count(('INTEND', '<INTEND>'))
        for i in range(intends): token.pop(token.index(('INTEND', '<INTEND>')))
        x = self.TypeCheck(token)

        if x == 'dynamicVar':
            left = getName(token[:token.index(('ASSIGN', '='))])
            right = getValue(token[token.index(('ASSIGN', '='))+1:])
            for _ in range(len(left)):
                self.toIntendApplier(dynamicVar([left[_], right[_]], x), intends, ('dynamic', left[_]))
                self.dynamic_var.add(left[_])
        elif x == 'staticVar':
            dt = token[0][1]
            left = getName(token[1:token.index(('ASSIGN', '='))])
            right = getValue(token[token.index(('ASSIGN', '='))+1:])
            for _ in range(len(left)):
                self.toIntendApplier(staticVar(dt, [left[_], right[_]], x), intends, ('static', left[_]))
                self.static_var.add(left[_])
        elif x == 'import':
            self.importProcess(token[1:])
        elif x in ['if', 'else if', 'else']: self.toIntendApplier(Conditions(token, x), intends)
        elif x in ['while', 'for']: self.toIntendApplier(Loops(token, x), intends)
        elif x == 'dynamicFunc': self.toIntendApplier(dynamicFunc(token, x), intends)
        elif x == 'funccall': self.toIntendApplier(funccall(token, x), intends)
        elif x == 'return': self.toIntendApplier(Return(token, x), intends)
        elif x == 'node': self.toIntendApplier(Node(token, x), intends)
    
    def toIntendApplier(self, object, intends, caller=(0,1)):
        if intends == 0:
            self.ast.append(object)
        elif intends == 1:
            if caller != (0,1):
                self.ast[-1].codeblock.append(object)
                self.ast[-1].var[caller[0]].add(caller[1])
            else:
                self.ast[-1].codeblock.append(object)
        else:
            self.resursiveLink(self.ast[-1].codeblock, object, intends, caller)

    def resursiveLink(self, to, object, intends, caller):
        if intends == 1:
            if caller != (0,1):
                to.codeblock.append(object)
                to.var[caller[0]].add(caller[1])
            else:
                to.codeblock.append(object)
        else:
            link = to[-1]
            self.resursiveLink(link, object, intends-1, caller) 