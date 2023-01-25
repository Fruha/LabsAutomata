from os import stat
from tree import Tree
import string 
import graphviz

class State:
    max_id = 0
    id = None
    output = dict()
    input = dict()
    type = None
    value = None

    def __init__(self, states:dict, type=None, value=None):
        self.input = dict()
        self.output = dict()
        self.id = State.max_id
        states[self.max_id] = self
        State.max_id += 1
        self.type = type
        self.value = value
        """code here"""
        pass
    
    def __repr__(self) -> str:
        return f'(id:{self.id}, type:{self.type}, value:{self.value}, \n output:{self.output} \n input:{self.input})'

class Graph:
    is_compile = False
    states = dict()
    tree = None
    start_id = None

    def __init__(self, regular:str = None):
        self.tree = Tree(regular=regular)

    def _get_all_ids(self, start_state_id, ans):
        # print(ans)
        if start_state_id == None:
            return ans
        if start_state_id in ans:
            return ans
        ans.update({self.states[start_state_id].id})
        for key in self.states[start_state_id].output.keys():
            for temp_id in self.states[start_state_id].output[key]:
                self._get_all_ids(self.states[temp_id].id, ans)
        for key in self.states[start_state_id].input.keys():
            for temp_id in self.states[start_state_id].input[key]:
                self._get_all_ids(self.states[temp_id].id, ans)
        return ans 

    def _copy_graph(self, start_state_id: int, end_state_id: int):
        # print('copy_graph_start')
        # print(start_state_id, end_state_id)
        # self.print(start_state_id)
        all_ids = list(self._get_all_ids(start_state_id, set()))
        new_ids = []
        for i in range(len(all_ids)):
            temp = State(self.states)
            new_ids.append(temp.id)
        mask = {all_ids[i]: new_ids[i] for i in range(len(all_ids))}
        
        # print('all_ids', all_ids)
        # print('new_ids', new_ids)
        for old_id, new_id in zip(all_ids, new_ids):
            # print('old', old_id, 'new', new_id)
            self.states[new_id].type = self.states[old_id].type
            self.states[new_id].value = self.states[old_id].value
            self.states[new_id].input = self.states[old_id].input.copy()
            self.states[new_id].output = self.states[old_id].output.copy()
            for key in self.states[old_id].input.keys():
                self.states[new_id].input[key] = set([mask[id] for id in self.states[old_id].input[key]])
            for key in self.states[old_id].output.keys():
                self.states[new_id].output[key] = set(mask[id] for id in self.states[old_id].output[key])
        # print('copy_graph_end')
        # self.print(mask[start_state_id])
        return mask[start_state_id], mask[end_state_id]

    def _CON(self, left_id_start, left_id_end, right_id_start, right_id_end):
        # print(f'left_id_start:{left_id_start}, left_id_end:{left_id_end} \n right_id_start:{right_id_start}, right_id_end:{right_id_end}')    
        self._union_states(left_id_end, right_id_start)
        return (left_id_start, right_id_end)

    def _union_states(self, left_id, right_id):
        if self.states[right_id].type:
            self.states[left_id].type = self.states[right_id].type
        if self.states[right_id].value:
            self.states[left_id].value = self.states[right_id].value
        all_ids = self._get_all_ids(left_id, set())
        all_ids = self._get_all_ids(right_id, all_ids)
        # print('START')
        for key in self.states[right_id].input.keys():
            if not self.states[left_id].input.get(key, None):
                self.states[left_id].input[key] = set()
            self.states[left_id].input[key].update(self.states[right_id].input[key])
        for key in self.states[right_id].output.keys():
            if not self.states[left_id].output.get(key, None):
                self.states[left_id].output[key] = set()
            self.states[left_id].output[key].update(self.states[right_id].output[key])

        # self.states[left_id].input |= self.states[right_id].input
        # self.states[left_id].output |= self.states[right_id].output
        # print('END')
        # self.print(left_id)
        # print('all_ids', left_id, right_id, all_ids)
        for id in all_ids:
            # self.print(id)
            for key in self.states[id].output.keys():
                temp_set = self.states[id].output[key].copy()
                for id_ in temp_set:
                    if id_ == right_id:
                        self.states[id].output[key].remove(id_)
                        self.states[id].output[key].add(left_id)
            for key in self.states[id].input.keys():
                temp_set = self.states[id].input[key].copy()   
                for id_ in temp_set:
                    if id_ == right_id:
                        self.states[id].input[key].remove(id_)
                        self.states[id].input[key].add(left_id)
                        # self.states[id].input[key][i] = left_id
        # print('END OR')
        # self.print(left_id)
        return left_id

    def _deep_pass(self, start_tree_id:int) -> list:
        if start_tree_id == None:
            return [None, None]

        # self.print()

        left_id_start, left_id_end = self._deep_pass(self.tree.nodes[start_tree_id].left)
        # print(self._deep_pass(self.tree.nodes[start_tree_id].right))
        right_id_start, right_id_end = self._deep_pass(self.tree.nodes[start_tree_id].right)

        # print(f'start_tree_id:{start_tree_id}, \n left_id_start:{left_id_start}, left_id_end:{left_id_end} \n right_id_start:{right_id_start}, right_id_end:{right_id_end}')
        

        if self.tree.nodes[start_tree_id].state in ['T', 'END']:
            # print('T')
            term = self.tree.nodes[start_tree_id].value
            start = State(self.states)
            end = State(self.states)
            # print(1, start)
            start.output[term] = set([end.id])
            end.input[term] = set([start.id])
            # print(2, start)
            # print(start.id, end.id)
            # self.print(start.id)
            return (start.id, end.id)
        
        if self.tree.nodes[start_tree_id].state == 'UG':
            # print('UG')
            term = self.tree.nodes[start_tree_id].value
            term = f'<{term}>'
            start = State(self.states)
            end = State(self.states)
            start.output[term] = set([end.id])
            end.input[term] = set([start.id])
            return (start.id, end.id)

        if self.tree.nodes[start_tree_id].state == 'D':
            # print('D')
            start = State(self.states)
            end = State(self.states)
            for term in string.ascii_letters + string.digits:
                start.output[term] = set([end.id])
                end.input[term] = set([start.id])
            return (start.id, end.id)

        if self.tree.nodes[start_tree_id].state == 'G':
            # print('G')
            # self.print(left_id_start)
            new_start1 = State(self.states)
            new_start2 = State(self.states)
            new_end1 = State(self.states)
            new_end2 = State(self.states)
            
            new_start1.output['EPS'] = set([new_start2.id])
            new_start2.output['EPS'] = set([left_id_start])
            self.states[left_id_end].output['EPS'] = set([new_end1.id])
            new_end1.output['EPS'] = set([new_end2.id])

            new_start2.input['EPS'] = set([new_start1.id])
            self.states[left_id_start].input['EPS'] = set([new_start2.id])
            new_start1.input['EPS'] = set([left_id_end])
            new_start2.input['EPS'] = set([new_start1.id])

            new_start2.type = '<'
            new_start2.value = self.tree.nodes[start_tree_id].value
            new_end1.type = '>'
            new_end1.value = self.tree.nodes[start_tree_id].value 
            # print('G end')
            # print(new_start1.id)
            # self.print(new_start1.id)
            return (new_start1.id, new_end2.id)

        if self.tree.nodes[start_tree_id].state == 'CON':
            # print('CON')
            return self._CON(left_id_start, left_id_end, right_id_start, right_id_end)


        if self.tree.nodes[start_tree_id].state == 'OR':
            # print('OR')
            # self.print(left_id_start)
            # self.print(right_id_start)
            # self.print(left_id_start)
            # self.print(right_id_start)
            # print('-------------')

            self._union_states(left_id_start, right_id_start)
            # self.print(left_id_start)
            # self.print(right_id_start)
            # # print('--------------')
            self._union_states(left_id_end, right_id_end)

            # self.print(left_id_start)
            return (left_id_start, left_id_end)
            
        if self.tree.nodes[start_tree_id].state == 'CL':
            # print('CL')
            # print(self.tree.nodes[start_tree_id])
            if self.tree.nodes[start_tree_id].value == [None, None]:
                self._union_states(left_id_start, left_id_end)
                return (left_id_start, left_id_start)
            elif self.tree.nodes[start_tree_id].value[1] == None:
                # print('-----DEBUG----')
                prev = None
                new_lefts = []
                new_rights = []
                for i in range(self.tree.nodes[start_tree_id].value[0]):
                    l,r = self._copy_graph(left_id_start, left_id_end)
                    if not prev:
                        prev = r
                    new_lefts.append(l)
                    new_rights.append(r)
                new_lefts.append(left_id_start)
                new_rights.append(left_id_end)
                for i in range(len(new_lefts)-1):
                    self._union_states(new_rights[i], new_lefts[i+1])
                self._union_states(new_rights[-2], new_rights[-1])
                return (new_lefts[0], new_rights[-2])
            elif self.tree.nodes[start_tree_id].value[0] == None:
                if not self.states[left_id_start].output.get('EPS', None):
                    self.states[left_id_start].output['EPS'] = set()
                self.states[left_id_start].output['EPS'].add(left_id_end)
                if not self.states[left_id_end].input.get('EPS', None):
                    self.states[left_id_end].input['EPS'] = set()
                self.states[left_id_start].output['EPS'].add(left_id_end)
                self.states[left_id_end].input['EPS'].add(left_id_start)
                new_lefts = []
                new_rights = []
                for i in range(self.tree.nodes[start_tree_id].value[1] - 1):
                    l,r = self._copy_graph(left_id_start, left_id_end)
                    new_lefts.append(l)
                    new_rights.append(r)
                new_lefts.append(left_id_start)
                new_rights.append(left_id_end)
                # print(new_lefts)
                new_l, new_r = new_lefts[0], new_rights[0]
                for i in range(len(new_lefts)-1):
                    new_l, new_r = self._CON(new_lefts[0], new_rights[i], new_lefts[i+1], new_rights[i+1])
                return (new_l, new_r)
            else:
                new_lefts = []
                new_rights = []
                for i in range(self.tree.nodes[start_tree_id].value[0]):
                    l,r = self._copy_graph(left_id_start, left_id_end)
                    new_lefts.append(l)
                    new_rights.append(r)

                if self.tree.nodes[start_tree_id].value[0] < self.tree.nodes[start_tree_id].value[1]:
                    if not self.states[left_id_start].output.get('EPS', None):
                        self.states[left_id_start].output['EPS'] = set()
                    self.states[left_id_start].output['EPS'].add(left_id_end)
                    if not self.states[left_id_end].input.get('EPS', None):
                        self.states[left_id_end].input['EPS'] = set()
                    self.states[left_id_start].output['EPS'].add(left_id_end)
                    self.states[left_id_end].input['EPS'].add(left_id_start)
                
                for i in range(self.tree.nodes[start_tree_id].value[1] - self.tree.nodes[start_tree_id].value[0]):
                    l,r = self._copy_graph(left_id_start, left_id_end)
                    new_lefts.append(l)
                    new_rights.append(r)
                # new_lefts.append(left_id_start)
                # new_rights.append(left_id_end)
                new_l, new_r = new_lefts[0], new_rights[0]
                for i in range(len(new_lefts)-1):
                    new_l, new_r = self._CON(new_lefts[0], new_rights[i], new_lefts[i+1], new_rights[i+1])
                return (new_l, new_r)

    def compile(self) -> None:        
        self.is_compile = True
        self.start_id = self._deep_pass(self.tree.root)[0]
        # print('self.start_id', self.start_id)
        pass

    def _match(self, string: str, state_id, active_groups, groups):
        # print(state_id, string)
        if string == '':
            # print('ans', groups)
            return groups
        
        
        if self.states[state_id].type == '<':
            groups[f'<{self.states[state_id].value}>'] = ''
            active_groups[f'<{self.states[state_id].value}>'] = True
        if self.states[state_id].type == '>':
            active_groups[f'<{self.states[state_id].value}>'] = False

        if self.states[state_id].output.get('EPS', None):
            for next_state_id in self.states[state_id].output['EPS']:
                ans = self._match(string, next_state_id, active_groups.copy(), groups.copy())
                if ans != None:
                    return ans                
        
        # if string[0] == '#':
        #     if self.states[state_id].output.get('#', False):

        for key in self.states[state_id].output.keys():
            if key[0] == '<' and key[-1] == '>':
                if len(string) >= len(groups[key]):
                    if groups[key] == string[:len(groups[key])]:
                        # print('groups[key]', groups[key], key)
                        ans = self._match(string[len(groups[key]):], list(self.states[state_id].output[key])[0], active_groups.copy(), groups.copy())
                        if ans != None:
                            return ans 
    
        # print('state_id', state_id, 'next states by key', self.states[state_id].output.get(string[0], False))
        if self.states[state_id].output.get(string[0], False):
            for next_state_id in self.states[state_id].output[string[0]]:
                # print(next_state_id)
                new_groups = groups.copy()
                # print(active_groups)
                for group_name in active_groups.keys():
                    if active_groups[group_name]:
                        new_groups[group_name] += string[0]
                ans = self._match(string[1:], next_state_id, active_groups.copy(), new_groups)
                if ans != None:
                    return ans 
        
        
        return None

    def match(self, string: str) -> bool:
        if string == '':
            return None
        # ans = False
        # print('START MATCHING')
        string += '#'
        all_ids = set([self.start_id])
        stack = [self.start_id]
        active_groups = dict()
        groups = dict()
        ans = self._match(string, self.start_id, active_groups, groups)
        return ans

    def _minimize(self):
        all_ids_ = self._get_all_ids(self.start_id, set())
        for id in all_ids_:
            fl = True
            if lefts := self.states[id].output.get('EPS', None):
                for r in self.states[id].output['EPS']:
                    if self.states[r].type == '<':
                        for key in self.states[r].output:
                            if r in self.states[r].output[key]:
                                fl = False
                        for key in self.states[id].output:
                            if id in self.states[id].output[key]:
                                fl = False
                        if fl:
                            # print('START')
                            # print('id', id, 'r', r)
                            # print('start_id', self.start_id)
                            # self.print(self.start_id)
                            # print('-----<>----')
                            t1 = self._union_states(id, r)
                            # print(t1)
                            # print(self.states[t1])
                            self.states[t1].output['EPS'].remove(t1)
                            # self.print(t1)
                            # print('END')
                            return

    def minimize(self) -> None:
        all_ids = self._get_all_ids(self.start_id, set())
        for i in range(len(all_ids)):
            # print(i)
            self._minimize()
        return

    def __repr__(self) -> str:
        """code here"""
        pass

    def addition(self):
        """code here"""
        pass

    def crossing(self):
        """code here"""
        pass

    def print(self, id=-1):
        if id == -1:
            id = self.start_id

        all_ids = self._get_all_ids(id, set())
        print(id, all_ids)
        for i in all_ids:
            print(self.states[i])
        
    def get_re_from_graph(self):
        return 

    def visualize(self):
        self.tree.visualize()
        graph = graphviz.Digraph('graph')
        all_ids = self._get_all_ids(self.start_id, set())
        for id in all_ids:
            for key in self.states[id].output.keys():
                for out_id in self.states[id].output[key]:
                    state1 = self.states[id]
                    state2 = self.states[out_id]
                    t1 = '' if not state1.type else state1.type
                    t2 = '' if not state2.type else state2.type
                    v1 = '' if not state1.value else state1.value
                    v2 = '' if not state2.value else state2.value
                    graph.edge(f'{state1.id} \n{t1} \n{v1}', f'{state2.id} \n{t2} \n{v2}', label=key)
        graph.render()

if __name__ == '__main__':
    graph = Graph('a+(<qwe>ab|(ba){,2})<qwe>{1,3}')
    # graph = Graph('(<q>a+)')
    # graph = Graph('(ab|aa|b|ca|ddddd)(c|d|cd)')
    # graph = Graph(r'(ab){3,3}')
    # graph = Graph('(<q>q(<w>w)(<e>e))')
    # graph = Graph('a(<qwe>b+)c<qwe>')
    # graph = Graph('a|ab')
    # graph = Graph('(<a>a)')

    graph.compile()
    # graph.minimize()
    graph.visualize()
    graph.print()
    print(graph.match('aaaaabababab'))
    # print(list(graph._get_all_ids(graph.start_id, set())))
    # print(graph.match('aaaaa'))