import argparse, re

parse = argparse.ArgumentParser(description='avm file')
parse.add_argument('file', type=str)
parse.add_argument('-v', '--version', action='version', version='Version: 1.0.0\n\nThis version includes printing, variables assignment, arthemtic operations')

args = parse.parse_args()
file_name = args.file

token = {
    "END": r"<END>",
    "INTEND": r"<INTEND>",
    "STRING": r'"[^"]*"',
    "CHAR": r"'[^']*'",
    "NAME": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
    "INT": r"\b\d+\b",
    "LPARAN": r"[\[\(\{]",
    "RPARAN": r"[\]\)\}]",
    "SPACE": r"\s+",
    "ASSIGN": r"=",
    "COMMENT": r"#.*",
    "ADD": r"\+",
    "SUB": r"-",
    "DIV": r"/",
    "MUL": r"\*",
    "SMALL": r"<",
    "INDT": r":$",
    "OUTCALL": r'>',
    "INCALL": r'~!'
}

token = '|'.join(f'(?P<{key}>{value})' for key,value in token.items())

def intendApply(line):
    if not line.startswith(' '):
        return line
    elif len(line)*' ' == line:
        return 'EMPTY'
    
    intend = '<INTEND>'
    space_count = len(line) - len(line.lstrip())
    line = line.lstrip()
    for i in range(int(space_count / 4)): line = intend+line

    return line

class VarAssign():
    def __init__(self, token, intends):
        self.type = 'VARASSIN'
        self.name = token[0][1]
        self.value = token[2:]
        self.datatype = self.most(token).lower()
        self.intend = intends

    def most(self, token):
        x = []
        for data in token:
            if data[0] in ['INT', 'CHAR', 'FLOAT', 'STRING']: x.append(data[0])
        return max(x)

class Calls():
    def __init__(self, token, intends):
        self.type = token[0][0]
        self.value = token[1:]
        self.intend = intends 

class Conditions():
    def __init__(self, token, intends, x):
        self.type = x.lower()
        self.value = token[1:-1]
        self.intend = intends

class Loops():
    def __init__(self, token, intends, x):
        self.type = x.lower()
        self.value = token[1:-1]
        self.intend = intends

class END():
    def __init__(self):
        self.type = 'END'
        self.value = 'END'
        self.intend = 0

class Core():
    def __init__(self, filedata):
        self.lines = filedata
        self.token = token
        self.ast = []
        self.variables = set()
        self.indent = 1
        filedata.append('<END>')
        
        for index, line in enumerate(self.lines):
            line = intendApply(line)
            if line == 'EMPTY': continue
            code = self.Lexer(line, index)
            if code == 'TERM':
                break

    def Lexer(self,line, index):
        token = []
        paran_count = 0
        for match in re.finditer(self.token, line):
            type = match.lastgroup
            value = match.group(type)
            if type == 'COMMENT': return
            if type == 'SPACE': continue
            if type == 'CHAR' and len(value) > 3 and value[1] != '\\':
                    print(f'Error: (Line: {index+1})\n\t using char string but given string')
                    return 'TERM'
            if type == 'LPARAN': 
                token.append((type, paran_count))
                paran_count+=1
            elif type == 'RPARAN':
                paran_count-=1
                token.append((type, paran_count))
            else: token.append((type, value))

        if len(token) != 0:
            self.Parser(token)

    def Parser(self, token):
        intends = token.count(('INTEND', '<INTEND>'))
        for i in range(intends): token.pop(token.index(('INTEND', '<INTEND>')))
        x = self.TypeCheck(token)
        
        if x == 'VARASSIGN': 
            self.ast.append(VarAssign(token, intends))
            self.variables.add(self.ast[-1].name)
        elif x in ['OUTCALL', 'INCALL']: self.ast.append(Calls(token, intends))
        elif x in ['IF', 'ELSE IF', 'ELSE']: self.ast.append(Conditions(token, intends, x))
        elif x in ['WHILE', 'FOR']: self.ast.append(Loops(token, intends, x))
        elif x == 'END': self.ast.append(END())

    def TypeCheck(self, token):
        try:
            if token[0][0] == 'END': return 'END'
            elif token[1][0] == 'ASSIGN': return 'VARASSIGN'
            elif token[0][0] == 'OUTCALL': return 'OUTCALL'
            elif token[0][0] == 'INCALL': return 'INCALL'
            elif token[0][1] in ['if', 'elif', 'else']:
                if token[0][1] == 'elif': return 'ELSE IF'
                else: return token[0][1].upper()
            elif token[0][1] in ['while', 'for']: return token[0][1].upper()
        except:
            print('ERROR: Something went wrong...')

class Compiler():
    def __init__(self, ast, filename, variables):
        self.ast = ast
        self.variables = variables
        self.filename = filename

        self.header = set()
        self.upperhead = ['using namespace std;\n']
        self.head = ['int main(){\n']
        self.core = []
        self.tail = ['}']
        
        self.codeConvert()
        self.go()

    def codeConvert(self):
        intend_level = 0
        for objects in self.ast:
            string, intend_level = self.intendApply(objects, intend_level)
            self.core.append(string)

    def intendApply(self, object, level):
        object_intend_level = object.intend

        code_sting = ''
        if level < object_intend_level:
            code_sting += '{\n'
            level +=1
        elif level > object_intend_level:
            code_sting += '}\n'
            level -=1

        code_sting += code_sting + '\t'*object.intend
        if object.type == 'VARASSIN':
            if object.name in self.variables:
                code_sting += f'{object.datatype} {object.name} = {self.converter(object.value)};\n'
                self.variables.remove(object.name)
            else:
                code_sting += f'{object.name} = {self.converter(object.value)};\n'
        if object.type == 'OUTCALL':
            self.header = self.header.union({'#include <iostream>\n'})
            code_sting += f'cout << {self.converter(object.value)} << endl;\n'
        if object.type == 'INCALL':
            self.header = self.header.union({'#include <iostream>\n'})
            code_sting += f'cin >> {self.converter(object.value)};\n'
        if object.type in ['if', 'else if']:
            code_sting += f'{object.type} ({self.converter(object.value)})\n'
        if object.type == 'else': code_sting += f'{object.type}\n'
        if object.type in ['while', 'for']:
            code_sting += f'{object.type} ({self.converter(object.value)})\n'

        return code_sting, level

    def converter(self, values):
        header = set()
        code_string = ''
        for token in values:
            if token[0] == 'LPARAN': code_string = code_string + '(' * (token[1]+1)
            elif token[0] == 'RPARAN': code_string = code_string + ')' * (token[1]+1)
            elif token[0] == 'STRING': 
                code_string += token[1]
                header.add('#include <string>\n')
            elif token[0] == 'OUTCALL': code_string += '>'
            else: 
                code_string += str(token[1])
        self.header = self.header.union(header)
        return code_string
            
    def go(self):
        final = list(self.header) + self.upperhead + self.head + self.core + self.tail

        with open(self.filename[:-4]+'.c++', 'w') as f:
            f.writelines(final)

        import os

        os.system(f'g++ {self.filename[:-4]+'.c++'} -o {self.filename[:-4]}')
        os.system(f'./{self.filename[:-4]}')

with open(file_name) as f:
    core = Core(f.readlines())
    Compiler(core.ast, file_name, core.variables)