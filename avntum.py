import argparse
from core.process import *
from core.transpile import *

parse = argparse.ArgumentParser(description='Avntum is dynamic programing language which transpile code to c++ and to a binary, avm code compiles in any platform, to use avm read tutorial.md and to run avm code do: \n\t~ python avntum.py xyz.avm', formatter_class=argparse.RawTextHelpFormatter)
parse.add_argument('file', type=str)
parse.add_argument('-v', '--version', action='version', version='Version: 1.9\n\nThis version includes printing, variables assignment, inputs, arthemtic operations, conditions, functions, file reading/writing, imports')

args = parse.parse_args()
file_name = args.file

with open(file_name) as f:
    core = Process(f.readlines())
    print('Transpilation performed Successfully...')
    Transpiler(core.ast, file_name, core.dynamic_var, core.static_var, core.header)
    print('Compilation performed Successfully...')