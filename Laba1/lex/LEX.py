import ply.lex as lex
from ply.lex import Lexer

class LEXParser():
    tokens = (
        'COMMAND',
        'KEYS',
        'SPACE'
    )

    tokens_list = []

    t_COMMAND = r"[a-zA-Z0-9./]+"
    t_KEYS = r"-[a-zA-Z]+"
    t_SPACE = r"[ \t]+"

    t_ignore = r""

    def __init__(self):
        self.lexer: Lexer = lex.lex(module=self)
        self.clear()

    def t_error(self, t):
        return False

    def genTokens(self, inp):
        self.lexer.input(inp)
        while True:
            try:
                tok = self.lexer.token()
            except lex.LexError:
                self.clear()
                return False
            if not tok:
                break
            self.tokens_list.append(tok)
        return True

    def check(self):
        if self.tokens_list:
            command = self.tokens_list.pop(0)
        else:
            return False
        if command.type != 'COMMAND':
            if command.type == 'SPACE':
                if self.tokens_list:
                    command = self.tokens_list.pop(0)
                else:
                    return False
                if command.type != 'COMMAND':
                    return False
            else:
                return False

        self._result['command'] = command.value
        while self.tokens_list:
            space = self.tokens_list.pop(0)
            if space.type != 'SPACE':
                return False
            if self.tokens_list:
                keys = self.tokens_list.pop(0)
            else:
                if self._result['keys']:
                    return True
                else:
                    return False
            if keys.type != 'KEYS':
                return False
            self._result['keys'] += list(keys.value[1:])
        
        return True

    def parse(self, inp: str):
        self.clear()
        if not self.genTokens(inp):
            return "INCORRECT"
        if self.check():
            self._result['keys'] = sorted(list(set(self._result['keys'])))
            return f"{self._result['command']} : {' '.join(self._result['keys'])}"
        else:
            return "INCORRECT"


    def clear(self):
        self._result = {"command" : "", "keys" : []}
        self._is_acceptable = True
        self.tokens_list = []


if __name__ == '__main__':
    data = """
    qwe -qw
    qwe -qw -w
    qwe      -qw -w
    qwe -qw -w
        qwe -q -w -e -w
    qwe -qw -ww -qwe --qqw w ww-wqs-  -qw-- -w   - w-q-x--  -
    qwe -w -w -w -w -w -w -w -w"""
    lx = LEXParser()
    for i, string in enumerate(data.split('\n')):
        print(i, lx.parse(string))
