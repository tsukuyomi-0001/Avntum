import argparse
from core.process import *
from core.transpile import *

parse = argparse.ArgumentParser(description='avm file')
parse.add_argument('file', type=str)
parse.add_argument('-v', '--version', action='version', version='Version: 1.6\n\nThis version includes printing, variables assignment, arthemtic operations')

args = parse.parse_args()
file_name = args.file

with open(file_name) as f:
    core = Process(f.readlines())
    Transpiler(core.ast, file_name, core.variables)