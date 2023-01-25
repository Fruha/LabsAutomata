import regex

class RGXParser():
    
    def __init__(self):
        self.clear()

    def clear(self):
        self._result = {"command" : "", "keys" : []}
        self._is_acceptable = True
        self.tokens_list = []

    def parse(self, string):
        try:
            m = regex.match(r"^\s*(?P<Command>[a-zA-Z0-9./]+)((?:\s)+-(?P<Keys>[a-zA-Z])+)+\s*$", string)
            return f"{m.captures('Command')[0]} : {' '.join(sorted(list(set(m.captures('Keys')))))}"
        except:
            return "INCORRECT"


if __name__ == '__main__':
    data = """56pwQIuU6Q	vS)-Z	 
    6cB		-mqoz%4]=NGb	 	
    eU*-Q	D"x*;,F-u  	-tFsL	-eOT 	 f2O-ef 
    w'5A~OPPi -F 	-Bua	 -bpl 6M*-BLMsy -fPCPUMW;V\  	-WEUGU 	
    s6zLEmzHTF 		-l  
    LYThV3eseg	 	-rPL 		
    wDMF6.33O		-cTKRC -c		
    TVa	-q 	-Un """
    rgx = RGXParser()
    for i, string in enumerate(data.split('\n')):
        print(i, rgx.parse(string))