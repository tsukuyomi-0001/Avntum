import argparse, re

parse = argparse.ArgumentParser(description='avm file')
parse.add_argument('file', type=str)
parse.add_argument('-v', '--version', action='version', version='Version: 1.0.0\n\nThis version includes printing, variables assignment, arthemtic operations')

args = parse.parse_args()
file_name = args.file

token = {
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
}

token = '|'.join(f'(?P<{key}>{value})' for key,value in token.items())

class VarAssign():
    def __init__(self, token):
        self.name = token[0][1]
        self.value = token[2:]
        self.type = 'VARASSIGN'
        self.datatype = self.most(token).lower()
        
    def most(self, token):
        x = []
        for data in token:
            if data[0] in ['INT', 'CHAR', 'FLOAT', 'STRING']:
                x.append(data[0])
        return max(x)

class Compiler():
    def __init__(self, lines, filename):
        self.lines = lines
        self.token = token
        self.ast = []

        for index, line in enumerate(lines):
            code = self.Lexer(line, index)
            if code == 'TERM':
                break

        file = filename[:-3] + '.c++'
        self.code_convertion(file)
    
    def Lexer(self, code, index):
        token = []
        for match in re.finditer(self.token, code):
            count = 0
            type = match.lastgroup
            value = match.group(type)
            if type == 'COMMENT':
                return
            if type == 'SPACE':
                continue
            if type == 'CHAR':
                if len(value) > 3 and value[1] != '\\':
                    print(f'Error: (Line: {index+1})\n\t using char string but given string')
                    return 'TERM'
            if type == 'LPARAN':
                token.append((type, count))
                count+=1
            elif type == 'RPARAN':
                token.append((type, count))
                count-=1
            else:
                token.append((type, value))
        self.Parser(token)

    def TypeCheck(self, token):
        try:
            if token[1][0] == 'ASSIGN':
                return 'VARASSIGN'
        except:
            pass
        
    def Parser(self, token):
        x = self.TypeCheck(token)
        if x == 'VARASSIGN':
            var_obj = VarAssign(token)
            self.ast.append(var_obj)

    def code_convertion(self, file):
        header = []
        head = 'int main(){\n'
        lines = ['using namespace std;\n', head]
        tail = '}'

        for objects in self.ast:
            string = ''
            if objects.type == 'VARASSIGN':
                string = f'{objects.datatype} {objects.name} = '
                for token in objects.value:
                    print(token)
                    if token[0] == 'LPARAN':
                        string += '('
                    elif token[0] == 'RPARAN':
                        string += ')'
                    elif token[0] == 'STRING':
                        string += token[1]
                        header.append('#include <string>\n')
                    else:
                        string += token[1]
                string += ';\n'
            lines.append(string)
        lines.append(tail)

        with open(file, 'w') as f:
            f.writelines(header + lines)

with open(file_name) as f:
    x = Compiler(f.readlines(), file_name)