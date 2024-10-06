import re
from .objects import *

token = {
    "INTEND": r"<INTEND>",
    "NAME": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
    # sorry
    "STR1": r"'[^']*'",
    "STR2": r'"[^"]*"',
    "INT": r"\b\d+\b",
    "LPARAN": r"[\[\(\{]",
    "RPARAN": r"[\]\)\}]",
    "SPACE": r"\s+",
    "EQUAL": r"==",
    "ASSIGN": r"=",
    "COMMENT": r"#.*",
    "ADD": r"\+",
    "SUB": r"-",
    "FLOOR": r"//",
    "DIV": r"/",
    "SQUR": r"\*\*",
    "MUL": r"\*",
    "SMALLEQ": r"<=",
    "BIGEQ": r">=",
    "NOTEQ": r"!=",
    "SMALL": r"<",
    "BIG": r'>',
    "INDT": r":$",
    "SEP": r","
}

# from - 
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
        self.variables = set()

        for index, line in enumerate(codelines):
            line = intendApply(line, index)
            if line == 'EMPTY': continue
            code = self.Lexer(line, index)
            if code == 'TERM' or line == 'TERM':
                break

        print(self.variables)

    def Lexer(self, line, index):
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
# to - perfect
    def TypeCheck(self, token):
        if ('ASSIGN', '=') in token:
            return 'VARASSIGN'
        elif token[0][1] in ['if', 'elif', 'else']:
            if token[0][1] == 'elif': return 'ELSE IF'
            else: return token[0][1].upper()
        elif token[0][1] in ['while', 'for']:
            return token[0][1].upper()
        elif token[0][1] == 'func':
            return token[0][1].upper()
        elif token[0][1] == 'return':
            return token[0][1].upper()

        elif token[0][0] == 'NAME' and token[1][0] == 'LPARAN': return 'FUNCCALL'

    def Parser(self, token):
        intends = token.count(('INTEND', '<INTEND>'))
        for i in range(intends): token.pop(token.index(('INTEND', '<INTEND>')))
        x = self.TypeCheck(token)

        if x == 'VARASSIGN':
            left = getName(token[:token.index(('ASSIGN', '='))])
            right = getValue(token[token.index(('ASSIGN', '='))+1:])
            for _ in range(len(left)):
                self.variables.add(left[_])
                self.toIntendApplier(VarAssign([left[_], right[_]], x), intends)
        elif x in ['IF', 'ELSE IF', 'ELSE']: self.toIntendApplier(Conditions(token, x), intends)
        elif x in ['WHILE', 'FOR']: 
            self.toIntendApplier(Loops(token, x), intends)
            if x == 'FOR': 
                self.variables.add(token[1][1])
        elif x == 'FUNCCALL':
            self.toIntendApplier(FuncCall(token, x), intends)

        elif x == 'FUNC':
            self.toIntendApplier(Func(token, x), intends)
            self.varInFunc(token[3:-2])
        elif x == 'RETURN':
            self.toIntendApplier(Return(token, x), intends)

    def varInFunc(self, token):
        for _ in token:
            if _[0] == 'NAME': self.variables.add(_[1])

    def toIntendApplier(self, object, intends):
        if intends == 0:
            self.ast.append(object)
        elif intends == 1:
            self.ast[-1].codeblock.append(object)
        else:
            self.recursiveLink(self.ast[-1].codeblock, object, intends)
        
    def recursiveLink(self, to, object, intend):
        if intend == 1:
            to.codeblock.append(object)
        else:
            link = to[-1]
            self.recursiveLink(link, object, intend-1)