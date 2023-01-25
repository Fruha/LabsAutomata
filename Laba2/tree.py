import string
import graphviz


class Node:
    max_id = 0
    state = None
    value = None

    id = None
    root = None
    left = None
    right = None

    def __init__(self, nodes: dict(), state: str, value):
        self.id = Node.max_id
        Node.max_id += 1
        self.state = state
        self.value = value
        nodes[self.id] = self
        """code here"""
        pass

    def __repr__(self):
        return f'(id:{self.id} state:{self.state} value:"{self.value}")'



class Tree:
    root = None
    busy_characters = r'&.()<>{,}+?|'
    nodes = dict()

    def __init__(self, regular = None):
        if regular:
            self.build(regular)
        

    def _check_shielding(self, regular: list):
        i = -1
        while i < len(regular) - 1:
            i += 1
            if regular[i].value == '&' and regular[i].state == None:
                regular[i].state = 'T'
                regular[i].value = regular[i+1].value
                del regular[i+1]
        return

    def _check_uses_group(self, regular: list):
        lefts = []
        rights = []
        for i, node in enumerate(regular):
            if node.value == '<' and node.state == None:
                lefts.append(i)
            if node.value == '>' and node.state == None:
                rights.append(i)
        if len(lefts) != len(rights):
            raise NameError('count < != count >')
        temp = [lefts[i // 2] if i % 2 == 0 else rights[i // 2] for i in range(2*len(lefts))]
        if temp != sorted(temp):
            raise NameError('Error brackets')

        for i1 in range(len(lefts)-1, -1, -1):
            # print(i1)
            group_name = ''
            for i2 in range(lefts[i1]+1, rights[i1]):
                group_name += regular[i2].value
            regular[lefts[i1]].value = group_name
            regular[lefts[i1]].state = 'UG'
            del regular[lefts[i1]+1:rights[i1]+1]
        return

    def _check_closing(self, regular: list):

        lefts = []
        rights = []
        commas = []
        # print(1,regular)
        for i, node in enumerate(regular):
            if node.value == '+' and node.state == None:
                regular[i].state = 'CL'
                regular[i].value = [1,None]
            if node.value == '?' and node.state == None:
                regular[i].state = 'CL'
                regular[i].value = [0,1]
            if node.value == '{' and node.state == None:
                lefts.append(i)
            if node.value == '}' and node.state == None:
                rights.append(i)
            if node.value == ',' and node.state == None:
                commas.append(i)    
        if (len(lefts) != len(rights)) or (len(lefts) != len(commas)):
            raise NameError("different counts of brackets")
        temp = []
        for i in range(len(lefts)):
            temp.append(lefts[i])
            temp.append(commas[i])
            temp.append(rights[i])
        if temp != sorted(temp):
            raise NameError('brackets Error')
        # print(2, regular)
        # print('------------------------DEBUG--------------------')    
        for i1 in range(len(lefts)-1, -1, -1):
            num1 = ''
            num2 = ''
            for i2 in range(lefts[i1]+1, commas[i1]):
                num1 += regular[i2].value
            for i2 in range(commas[i1]+1, rights[i1]):
                num2 += regular[i2].value
            if num1 == '':
                num1 = None
            else:
                num1 = int(num1)
            if num2 == '':
                num2 = None
            else:
                num2 = int(num2)
            regular[lefts[i1]].state = 'CL'
            regular[lefts[i1]].value = [num1, num2]
            del regular[lefts[i1]+1:rights[i1]+1]
        # print(3, regular)
        # if regular[0].state == 'CL':
        #     raise NameError('First node CL')
        
        # print('------------------------DEBUG--------------------') 

        i = 1
        while i < len(regular):
            if regular[i].state == 'CL':
                regular[i].left = regular[i-1].id
                regular[i-1].root = regular[i].id
                del regular[i-1]
                continue
            i+=1
        return

    def _check_concatenate(self, regular: list):
        if regular[0].value == '|' and regular[0].state == None:
            raise NameError('First char is |')
        concatenate_list = []
        for i1,node in enumerate(regular[:-1]):
            if node.value != '|' and regular[i1+1].value != '|':
                concatenate_list.append(i1)
        for i in concatenate_list[::-1]:
            new = Node(self.nodes, 'CON', None)
            new.left = regular[i].id
            new.right = regular[i+1].id
            regular[i].root = new.id
            regular[i+1].root = new.id
            del regular[i+1]
            regular[i] = new
        return

    def _check_or(self, regular: list):
        if regular[0].value == '|':
            raise NameError('First char is |')
        or_list = []
        for i1,node in enumerate(regular[1:-1]):
            if node.value == '|' and regular[i1].value != '|' and regular[i1+2].value != '|':
                or_list.append(i1+1)
        for i in or_list[::-1]:
            regular[i].state = 'OR'
            regular[i].value = None
            regular[i].left = regular[i-1].id
            regular[i].right = regular[i+1].id
            del regular[i+1]
            del regular[i-1]
        return

    def _check_non_group(self, regular: list) -> Node:
        self._check_uses_group(regular)
        # print('start non_group')
        # print(regular)
        self._check_closing(regular)
        # print('closing')
        # print(regular)
        self._check_concatenate(regular)
        # print('concatenate')
        # print(regular)
        self._check_or(regular)
        # print('or (end)')
        # print(regular)
        return regular[0]

    def _check_group_name(self, regular: list) -> Node:
        
        """code here"""
        # print('_check_group_name start')
        # print(regular)
        st = 0
        group_name = None
        if regular[0].value == '<' and regular[0].state == None:
            group_name = ''
            fl = False
            for i, node in enumerate(regular[1:]):
                if node.value == '>' and node.state == None:
                    fl = True
                    break
            if fl==False:
                raise NameError('<> Error')        
            for node in regular[1:i+1]:
                if not (node.value in string.ascii_letters + string.digits):
                    raise NameError('<non ascii_letters> Error')
                group_name += node.value
            st = i + 2
        node = self._check_non_group(regular[st:])
        if group_name:
            group = Node(self.nodes, 'G', group_name)
            group.left = node.id
            return group
        else:
            return node

    def _find_cls_brck(self, regular: list):
        left = -1
        right = -1
        for i, node in enumerate(regular):
            if node.value == '(' and node.state == None:
                left = i
            elif node.value ==')' and node.state == None:
                right = i
                break
        if left == -1 ^ right == -1:
            raise NameError('Error brackets')
        return (left, right)

    def _check_dots(self, regular: list):
        i = -1
        while i < len(regular) - 1:
            i += 1
            if regular[i].value == '.' and regular[i].state == None:
                regular[i].state = 'D'
        return

    def build(self, regular: str) -> bool:
        reg = list('((' + regular + ')#)')
        regular = []
        for i, ch in enumerate(reg):
            if (ch == '#') and (i == len(reg)-2):
                regular.append(Node(self.nodes, 'END', ch))
            elif not(ch in self.busy_characters):
                regular.append(Node(self.nodes, 'T', ch))
            else:
                regular.append(Node(self.nodes, None, ch))
        self._check_shielding(regular)
        self._check_dots(regular)
        brackets = self._find_cls_brck(regular)
        while brackets[0] != -1 and brackets[1] != -1:
            node = self._check_group_name(regular[brackets[0]+1:brackets[1]])
            del regular[brackets[0]:brackets[1]+1]
            regular.insert(brackets[0], node)
            brackets = self._find_cls_brck(regular)
        self.root = node.id

    def add_edges(self, graph, root_id):
        if l := self.nodes[root_id].left:
            node = self.nodes[root_id]
            node2 = self.nodes[node.left]
            graph.edge(f'{node.id}, {node.state}, "{node.value}"', f'{node2.id}, {node2.state}, "{node2.value}"')
            self.add_edges(graph, l)
        if r := self.nodes[root_id].right:
            node = self.nodes[root_id]
            node2 = self.nodes[node.right]
            graph.edge(f'{node.id}, {node.state}, "{node.value}"', f'{node2.id}, {node2.state}, "{node2.value}"')
            self.add_edges(graph, r)


    def visualize(self):
        graph = graphviz.Digraph('tree')
        self.add_edges(graph, self.root)
        graph.render()

if __name__ == '__main__':
    # t = Tree('a+.(<qwe>ab|(ba){,2})<qwe>{1,3}')
    t = Tree('a|a')
    # t.build('a+.(<qwe>ab|(ba){,2})<qwe>{1,3}')
    # t.build('123(&(&))+.(<qwe>abo|ba{,1})<qwe>{1,3}')
    # t.build('q.&.qq|c?w+&?e&&c(<gr1>w+) <gr1> <gr2> (<gr2>r{,2})<gr2>+')
    t.visualize()