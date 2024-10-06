imports = {
    'VARASSIGN': ['#include "./builtins/core.c++"\n', '#include <vector>\n'],
    "print": ['#include "./builtins/core.c++"\n'],
    "input": ['#include <iostream>\n'],
    "STRING": ['#include <string>\n'],
    "FUNC": ['#include <vector>\n', '#include <tuple>\n']
}

builtin_func = ['print', 'input', 'range']

class Transpiler:
    def __init__(self, ast, filename, variables):
        self.ast = ast
        self.filename = filename
        self.variables = variables
        self.vartrack = variables.copy()
        
        self.header = set()

        self.function = []
        self.upperhead = ['int main(){\n']
        self.core = []

        self.codeConvert()
        self.finalize()

    def LinearConvert(self, object, t=''):
        code_string = '\t'+t
        if object.type == 'VARASSIGN':
            for header in imports[object.type]: self.header.add(header)
            if object.name in self.vartrack:
                code_string += f'vector<float> {object.name} = {self.convert(object.value)};\n'
                self.vartrack.remove(object.name)
            else:
                code_string += f'{object.name} = {self.convert(object.value)};\n'

        if object.type == 'FUNCCALL':
            for func in builtin_func:
                if func == object.name:
                    for header in imports[func]:
                        self.header.add(header)
                    code_string += f'{func}({self.convert(object.args)});\n'

        if object.type in ['IF', 'ELSE IF']:
            code_string += f'{object.type.lower()} ({self.convert(object.value)})'
        if object.type == 'ELSE':
            code_string += f'{object.type.lower()}'
        if object.type == 'WHILE':
            code_string += f'{object.type.lower()} ({self.convert(object.value)})'
        if object.type == 'FOR':
            code_string += f'{object.type.lower()} (const auto& {object.value[0][1]}: {self.convert(object.value[1:])})'
        if object.type == 'FUNC':
            for header in imports[object.type]:
                self.header.add(header)
            self.function.append(f'vector<float> {object.name}({self.convert(object.value, 'FUNC')})')
            self.recursiveCodeApply(object, 'FUNC')

            object.codeblock = []
        
        if object.type == 'RETURN':
            code_string += f'return {self.convert(object.value)};\n'

        if object.type == 'TRY':
            code_string += f'{object.name}'
        if object.type == 'CATCH':
            code_string += f'{object.name}(...)'
        code_string+='\t'
        return code_string

    def codeConvert(self):
        for object in self.ast:
            self.core.append(self.LinearConvert(object))
            self.recursiveCodeApply(object)
    
    def recursiveCodeApply(self, object, lock=''):
        if len(object.codeblock) == 0:
            return None
        elif lock == 'FUNC':
            self.function.append('{\n')
            for linear in object.codeblock:
                self.function.append(self.LinearConvert(linear, '\t'))
                if len(linear.codeblock) > 0:
                    self.recursiveCodeApply(linear, 'FUNC')
            self.function.append('\t}\n')
        else:
            self.core.append('{\n')
            for linear in object.codeblock:
                self.core.append(self.LinearConvert(linear, '\t'))
                if len(linear.codeblock) > 0:
                    self.recursiveCodeApply(linear)
            self.core.append('\t}\n')

    def convert(self, value, sec=''):
        header = set()
        code_string = ''
        for token in value:
            if token[0] == 'LPARAN': code_string = code_string + '(' * (token[1]+1)
            elif token[0] == 'RPARAN': code_string = code_string + ')' * (token[1]+1)
            elif token[0] == 'STRING':
                code_string += f'encode("{token[1]}")'
                for _ in imports[token[0]]:
                    header.add(_)
            elif token[0] == 'SEP': code_string += ','
            elif token[0] == 'NAME':
                if sec == 'FUNC':
                    for h in imports['VARASSIGN']:
                        self.header.add(h)
                    code_string+= f'vector<float> {token[1]}'
                elif token[1] in self.variables and token[1] in self.vartrack: 
                    code_string+= f'{token[1]}'
                elif token[1] in self.variables and not token[1] in self.vartrack: 
                    code_string+= f'encode({token[1]})'
                
                for func in builtin_func:
                    if func == token[1]:
                        code_string = token[1]
            elif token[0] in ['INT', 'FLOAT']:
                code_string += f'encode({token[1]})'
            elif token[0] == 'RETURN':
                code_string += 'return'
            else:
                code_string += str(token[1])
        self.header = self.header.union(header)
        return code_string
    
    def finalize(self):
        try:
            final = list(self.header) + ['using namespace std;\n'] + self.function + self.upperhead + self.core + ['}']
        except:
            final = self.upperhead + self.core + self.tail
        with open(self.filename[:-4]+'.c++', 'w') as f:
            f.writelines(final)