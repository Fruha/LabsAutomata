from tree import Tree
from graph import Graph

class Regular:

    def __init__(self, regular : str):
        self.graph = Graph(regular)
    
    def compile(self) -> None:
        self.graph.compile()
        pass
    
    def match(self, string: str) -> dict:
        return self.graph.match(string)
    
    def getRe(self) -> str:
        """code here"""
        pass
    
    def addition(self):
        """code here"""
        pass
    
    def crossing(self):
        """code here"""
        pass


if __name__ == '__main__':
    r = Regular('a')
    r.compile()
    groups = r.match('a')
    if groups == None:
        raise NameError('')
    groups = r.match('b')
    if groups != None:
        raise NameError('')
    
    r = Regular('a|b')
    r.compile()
    groups = r.match('a')
    if groups == None:
        raise NameError('')
    groups = r.match('b')
    if groups == None:
        raise NameError('')
    groups = r.match('ab')
    if groups != None:
        raise NameError('')

    r = Regular('ab')
    r.compile()
    groups = r.match('a')
    if groups != None:
        raise NameError('')
    groups = r.match('b')
    if groups != None:
        raise NameError('')
    groups = r.match('ab')
    if groups == None:
        raise NameError('')

    r = Regular('&b')
    r.compile()
    groups = r.match('a')
    if groups != None:
        raise NameError('')
    groups = r.match('b')
    if groups == None:
        raise NameError('')

    r = Regular('a+')
    r.compile()
    groups = r.match('')
    if groups != None:
        raise NameError('')
    groups = r.match('a')
    if groups == None:
        raise NameError('')
    groups = r.match('aaaa')
    if groups == None:
        raise NameError('')
    groups = r.match('b')
    if groups != None:
        raise NameError('')

    r = Regular('a{1,3}')
    r.compile()
    groups = r.match('')
    if groups != None:
        raise NameError('')
    groups = r.match('a')
    if groups == None:
        raise NameError('')
    groups = r.match('aa')
    if groups == None:
        raise NameError('')
    groups = r.match('aaa')
    if groups == None:
        raise NameError('')
    groups = r.match('aaaa')
    if groups != None:
        raise NameError('')
    groups = r.match('b')
    if groups != None:
        raise NameError('')

    r = Regular('.')
    r.compile()
    groups = r.match('')
    if groups != None:
        raise NameError('')
    groups = r.match('a')
    if groups == None:
        raise NameError('')
    groups = r.match('b')
    if groups == None:
        raise NameError('')
    groups = r.match('ab')
    if groups != None:
        raise NameError('')

    r = Regular('(<a>(ab)+)')
    r.compile()
    t1 = len(r.graph._get_all_ids(r.graph.start_id, set()))
    groups = r.match('')
    if groups != None:
        raise NameError('')
    groups = r.match('ab')
    if groups == None:
        raise NameError('')
    if groups['<a>'] != 'ab':
        raise NameError('')
    groups = r.match('abab')
    if groups == None:
        raise NameError('')
    if groups['<a>'] != 'abab':
        raise NameError('')
    groups = r.match('aaaa')
    if groups != None:
        raise NameError('')

    r.graph.minimize()
    t2 = len(r.graph._get_all_ids(r.graph.start_id, set()))
    groups = r.match('')
    if t1 <= t2:
        raise NameError('')
    if groups != None:
        raise NameError('')
    groups = r.match('ab')
    if groups == None:
        raise NameError('')
    if groups['<a>'] != 'ab':
        raise NameError('')
    groups = r.match('abab')
    if groups == None:
        raise NameError('')
    if groups['<a>'] != 'abab':
        raise NameError('')
    groups = r.match('aaaa')
    if groups != None:
        raise NameError('')

    r = Regular('(<a>a)')
    r.compile()
    t1 = len(r.graph._get_all_ids(r.graph.start_id, set()))
    groups = r.match('a')
    if groups == None:
        raise NameError('')
    if groups['<a>'] != 'a':
        raise NameError('')

    r.graph.minimize()
    t2 = len(r.graph._get_all_ids(r.graph.start_id, set()))
    groups = r.match('a')
    if t1 <= t2:
        raise NameError('')
    if groups == None:
        raise NameError('')
    if groups['<a>'] != 'a':
        raise NameError('')

    r = Regular('(<c>(<a>ab)(<b>cd))')
    r.compile()
    groups = r.match('abcd')
    if groups == None:
        raise NameError('')
    if groups['<a>'] != 'ab':
        raise NameError('')
    if groups['<b>'] != 'cd':
        raise NameError('')
    if groups['<c>'] != 'abcd':
        raise NameError('')
    groups = r.match('ab')
    if groups != None:
        raise NameError('')
    groups = r.match('')
    if groups != None:
        raise NameError('')

    r = Regular('(<c>(<a>a{,})(<b>b{,}))')
    r.compile()
    groups = r.match('aaabbbb')
    if groups == None:
        raise NameError('')
    if groups['<a>'] != 'aaa':
        raise NameError('')
    if groups['<b>'] != 'bbbb':
        raise NameError('')
    if groups['<c>'] != 'aaabbbb':
        raise NameError('')
    groups = r.match('aaaaaa')
    if groups == None:
        raise NameError('')
    if groups['<a>'] != 'aaaaaa':
        raise NameError('')
    if groups['<b>'] != '':
        raise NameError('')
    if groups['<c>'] != 'aaaaaa':
        raise NameError('')
    groups = r.match('bbbbb')
    if groups == None:
        raise NameError('')
    if groups['<a>'] != '':
        raise NameError('')
    if groups['<b>'] != 'bbbbb':
        raise NameError('')
    if groups['<c>'] != 'bbbbb':
        raise NameError('')

    r = Regular('(<q>(a|b|c))<q>+(<w>1|23)<w>.<q>')
    r.compile()
    groups = r.match('aaaaa23231a')
    if groups == None:
        raise NameError('')
    if groups['<q>'] != 'a':
        raise NameError('')
    if groups['<w>'] != '23':
        raise NameError('')


    r = Regular('a+(<qwe>ab|(ba){,2})<qwe>{1,3}')
    r.compile()
    groups = r.match('aaaaabababab')
    if groups == None:
        raise NameError('')
    if groups['<qwe>'] != 'ab':
        raise NameError('')
    groups = r.match('aaaaababababab')
    if groups != None:
        raise NameError('')
    r.graph.visualize()
