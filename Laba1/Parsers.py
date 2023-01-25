import sys, os
pypath = os.path.dirname(__file__)
for dir_name in os.listdir():
    dir_path = os.path.join(pypath, dir_name)
    if os.path.isdir(dir_path):
        sys.path += [dir_path]

from smc import SMC
from lex import LEX
from rgx import RGX


if __name__ == '__main__':
    data = """pP7jHk4e 		-ZY -nLPEnsTdfa. 
    qwe -q -w -w   """
    rgx = RGX.RGXParser()
    lex = LEX.LEXParser()
    smc = SMC.SMCParser()

    parsers = [rgx, lex, smc]
    for parser in parsers:
        for i, string in enumerate(data.split('\n')):
            print(i, parser.parse(string))
        print()
