
def recurse(object, tabs):
    for obj in object:
        print(' '*tabs, obj.type)
        if len(obj.codeblock) == 0:
            pass
        else:
            recurse(obj.codeblock, tabs=tabs+4)

def view(ast):
    for obj in ast:
        print(obj.type)
        if len(obj.codeblock) == 0:
            pass
        else:
            recurse(obj.codeblock, tabs=4)