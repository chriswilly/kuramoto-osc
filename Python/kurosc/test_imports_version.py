"""
test imports version
"""

from importlib import import_module
import sys

def load_dependencies(file):
    reader = open(file,'r')
    dependencies = reader.readlines()
    reader.close()
    dependencies = [x.strip() for x in dependencies] # remove spaces
    count = len(dependencies)
    success = 0
    for module in dependencies:
        try:
            globals()[module] = import_module(module)
            success +=1
        except:
            print(f'failed to import line {module}')
    return count, success


def version_print(count,success):
    modulenames = set(sys.modules) & set(globals())
    allmodules = [sys.modules[name] for name in modulenames]
    versioned = 0

    print("\nImported Version")
    for module in allmodules:
        try:
            print(module.__name__, module.__version__)
            versioned+=1
        except:
            try:
                print(module.__name__, module.version)
                versioned+=1
            except:
                print(module.__name__, "does not have version info" )

    print('\n\n',versioned, "of", len(allmodules), \
          "imported libraries provide '__version__' or 'version'",\
          f'\n& {success} out of {count} lines imported from requirements')

if __name__=='__main__':
    lines,imported = load_dependencies('requirements.txt')
    version_print(lines,imported)
