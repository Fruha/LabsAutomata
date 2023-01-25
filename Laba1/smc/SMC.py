
import AppClass_sm

class SMCParser():

    def __init__(self):
        self._fsm = AppClass_sm.AppClass_sm(self)
        self.clear()

    def isChar(self, x):
        if (x >= 'a' and x <= 'z') or (x >= 'A' and x <= 'Z'):
            return True
        return False

    def isDigit(self, x):
        if x >= '0' and x <= '9':
            return True
        return False

    def isSkip(self, x):
        return x in [' ', '\t']

    def isDotOrSlash(self, x):
        return x in ['.','/']

    def isHyphen(self, x):
        return x == '-'

    def clear(self):
        self._result = {"command" : "", "keys" : []}
        self._word = ''
        self._is_acceptable = True
        self._fsm.setState(AppClass_sm.Map.PreCommand)

    def parse(self, inp: str):
        self.clear()
        for self._ch in inp:
            if not self._is_acceptable:
                break
            if self.isChar(self._ch):
                # print('isChar')
                self._fsm.char()
            elif self.isDigit(self._ch):
                # print('isDigit')
                self._fsm.digit()
            elif self.isSkip(self._ch):
                # print('isSkip')
                self._fsm.skip()
            elif self.isHyphen(self._ch):
                # print('isHyphen')
                self._fsm.hyphen()
            elif self.isDotOrSlash(self._ch):
                # print('isDotOrSlash')
                self._fsm.dotOrSlash()
            else:
                # print('unknown')
                self._fsm.unknown()
            # print(self._is_acceptable)
        self._fsm.end()
        # print(self._is_acceptable)
        return self.Ending()

    def addChar(self):
        self._word += self._ch

    def clearWord(self):
        self._word = ''   

    def addCommand(self):
        self._result['command'] = self._word
        self.clearWord()

    def addKey(self):
        self._result['keys'] += self._word
        self.clearWord()

    def Unacceptable(self):
        self._is_acceptable = False

    def NotEmptyKeys(self):
        return bool(self._result['keys'])
        
    # def Ending(self):
    #     """ Return JSON """
    #     self._result['keys'] = list(self._result['keys'])
    #     if self._is_acceptable:
    #         return {'is_acceptable' : True, **(self._result)}
    #     else:
    #         return {'is_acceptable' : False}

    def Ending(self):
        """ Return string """
        self._result['keys'] = sorted(list(set(self._result['keys'])))
        if self._is_acceptable:
            return f"{self._result['command']} : {' '.join(self._result['keys'])}"
        else:
            return "INCORRECT"

if __name__ == '__main__':
    data = """XsYmf2Dr9o		 -YF 	-YsZI2I		 """
    smc = SMCParser()
    for i, string in enumerate(data.split('\n')):
        print(i, smc.parse(string))