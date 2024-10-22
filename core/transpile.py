# import ast_viewer as astv
import os

directory = os.getcwd()

imports = {
    'dynamicVar': [f'#include "{directory}/builtins/core.h"\n', '#include <vector>\n'],
    'STRING': ['#include <iostream>\n'],
    'dynamicFunc': ['#include <vector>\n', '#include <tuple>\n'],
}

builtinFunc = ['print', 'input', 'type', 'len', 'range', 'read', 'write', 'decoded_int', 'decoded_float', 'decoded_string']

class Transpiler:
    def __init__(self, ast, filename, dynamicVar, staticVar, headers, import_file=False):
        self.ast = ast
        self.filename = filename
        self.dynamicVar = dynamicVar
        self.staticVar = staticVar

        self.dynamicVarTrack = dynamicVar.copy()
        self.staticVarTrack = staticVar.copy()

        self.funcdynamicvar = []


        self.header = set()
        self.function = []
        self.core = []
        for header in headers:
            self.header.add(f'#include "{header}.cpp"\n')
            header = header.split('/')[-1]
            self.core.append(f'\t{header} {header};\n\t{header}.main();\n')

        self.codeConvert()
        self.finalize(import_file)

    def linearConvert(self, object, t=''):
        code_string = '\t'+t
        if object.type == 'staticVar':
            if object.name in self.staticVarTrack:
                type = ''
                if object.datatype == 'int': type = 'int'
                if object.datatype == 'int16': type = 'short'
                if object.datatype == 'int32': type = 'long'
                if object.datatype == 'int64': type = 'long long'
                if object.datatype == 'float': type = 'float'
                if object.datatype == 'float64': type = 'double'
                if object.datatype == 'float128': type = 'long double'
                if object.datatype == 'string': type = 'string'

                code_string += f'{type} {object.name} = {self.convert(object.value, calltype='static')};\n'
                self.staticVarTrack.remove(object.name)
            else:
                code_string += f'{object.name} = {self.convert(object.value)};\n'
        if object.type == 'dynamicVar':
            for header in imports['dynamicVar']: self.header.add(header)
            if object.name in self.dynamicVarTrack:
                code_string += f'vector<float> {object.name} = {self.convert(object.value)};\n'
                self.dynamicVarTrack.remove(object.name)
            else:
                code_string += f'{object.name} = {self.convert(object.value)};\n'
        if object.type in ['if', 'else if']:
            code_string += f'{object.type} ({self.convert(object.value)})'
            # for var in object.var['dynamic']:
            #     self.dynamicVar.add(var)
            #     self.dynamicVarTrack.add(var)
            # for var in object.var['static']:
            #     self.staticVar.add(var)
            #     self.staticVarTrack.add(var)
        
        if object.type == 'for':
            code_string += f'for (float& {object.value[0][1]} : {self.convert(object.value[2:])})'
            self.staticVar.add(object.value[0][1])
        if object.type == 'while':
            code_string += f'while ({self.convert(object.value)})'
            self.staticVar.add(object.value[0][1])
        if object.type == 'dynamicFunc':
            for header in imports[object.type]:
                self.header.add(header)
            for var in object.var['dynamic']:
                self.dynamicVar.add(var)
                self.dynamicVarTrack.add(var)
            self.function.append(f'vector<float> {object.name}({self.convert(object.args, sector='FUNC')})')
            self.recursiveCodeApply(object, 'FUNC', object.var['dynamic'])
            object.codeblock = []
        if object.type == 'funccall':
            for func in builtinFunc:
                if func == object.name:
                    self.header.add(f'#include "{directory}/builtins/core.h"\n')
            code_string += f'{object.name}{self.convert(object.value)};\n'
        if object.type in ['else']:
            code_string += f'{object.type}'
        if object.type == 'return':
            code_string += f'return {self.convert(object.value)};\n'
        if object.type == 'node':
            code_string += f'{object.name}.{self.convert(object.call)};\n'
        return code_string

    def codeConvert(self):
        for object in self.ast:
            self.core.append(self.linearConvert(object))
            self.recursiveCodeApply(object)

    def recursiveCodeApply(self, object, sector='', dynamicVarfunc=[]):
        if len(object.codeblock) == 0:
            return None
        elif sector == 'FUNC':
            self.function.append('{\n')
            for linear in object.codeblock:
                self.function.append(self.linearConvert(linear, '\t'))
                if len(linear.codeblock) > 0:
                    self.recursiveCodeApply(linear, 'FUNC')
            self.function.append('\t}\n')
            for var in dynamicVarfunc:
                self.dynamicVarTrack.add(var)
        else:
            self.core.append('{\n')
            for linear in object.codeblock:
                self.core.append(self.linearConvert(linear, '\t'))
                if len(linear.codeblock) > 0:
                    self.recursiveCodeApply(linear)
            self.core.append('\t}\n')

    def convert(self, value, calltype='main', sector=''):
        header = set()
        code_string = ''

        for token in value:
            if token[0] == 'LPARAN': code_string = code_string + '(' * (token[1]+1)
            elif token[0] == 'RPARAN': code_string = code_string + ')' * (token[1]+1)
            elif token[0] == 'STRING':
                if calltype == 'static':
                    code_string += f'"{token[1]}"'
                else:
                    code_string += f'encode("{token[1]}")'
                for _ in imports[token[0]]:
                    header.add(_)
            elif token[0] == 'SEP': code_string += ','
            elif token[0] == 'NAME':
                if token[1] in self.staticVar:
                    code_string += f'encode({token[1]})'
                elif token[1] in self.dynamicVar:
                    if sector == 'FUNC':
                        code_string += f'vector<float> '
                        self.dynamicVarTrack.remove(token[1])
                    code_string += f'{token[1]}'
                else:
                    for func in builtinFunc:
                        if func == token[1]:
                            self.header.add(f'#include "{directory}/builtins/core.h"\n')
                    code_string += f'{token[1]}'
            
            elif token[0] in ['INT', 'FLOAT']:
                if calltype == 'static':
                    code_string += f'{token[1]}'
                else:
                    code_string += f'encode({token[1]})'
            else:
                code_string += str(token[1])
        self.header = self.header.union(header)
        return code_string
    
    def finalize(self, import_file):
        if import_file == True:
            local = self.filename.split('/')[-1]
            final = list(self.header) + ['using namespace std;\n'] + [f'class {local[:-4]}', '{\n\tpublic:\n'] + self.function + ['\t\tvoid main(){\n'] + self.core + ['\t}\n};']
            with open(self.filename[:-4]+'.cpp', 'w') as f:
                f.writelines(final)
        else:
            final = list(self.header) + ['using namespace std;\n'] + self.function + ['int main(){\n'] + self.core + ['}']
            with open(self.filename[:-4]+'.c++', 'w') as f:
                f.writelines(final)

            import os
            os.system(f'g++ ./builtins/core.cpp ./builtins/core.h {self.filename[:-4]+'.c++'} -o {self.filename[:-4]}')