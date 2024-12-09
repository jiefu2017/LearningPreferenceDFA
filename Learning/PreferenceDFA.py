from automata.fa.dfa import DFA
from Learning import PreferenceDFA
from itertools import permutations
import Utility.MathUtility as MU


import Utility.AutomataUtility as AU

import Utility.AlphabetUtility as ALU
import copy
import jsonpickle
from Learning.Graph import Graph
# import simplejson as json
import Utility.ioutils as ioutils

import ast


class PreferenceDFA:

    epsilon = ""

    def __new__(DFA, *args, **kwargs):

        instance = super().__new__(DFA)
        return instance


    def __init__(self, states, input_symbols, transitions, initial_state, prefGraph):
        self.states = states
        self.input_symbols = input_symbols
        self.transitions= transitions
        self.initial_state = initial_state
        self.final_states = set()
        self.prefGraph = prefGraph
        '''
        The preference graph. It is an object of type Graph
        Each vertex v of this graph is a subset of states of the DFA
        An ege e=(v1, v2) means that v1 is preferred over v2.
        '''




        '''
        The mapping from a state of the DFA to a vertex of the preference graph
        '''
        self.state_vertex_in_pref_graph = {}

        self.nuclues = None
        self.shortest_prefixes = None


    def set_prefGraph(self, prefGraph):
        self.prefGraph = prefGraph
        self.state_vertex_in_pref_graph = {}

    def read_from_json_file(input_symbols, path="PDFA_JSON/icra2022.json"):
        base_dict = ioutils.from_json(path)
        # base_dict["states"] = {int(k): v for k, v in base_dict["states"].items()}
        base_dict["states"] = {k for k, v in base_dict["states"].items()}
        # base_dict["transitions"] = {int(k): v for k, v in base_dict["transitions"].items()}
        base_dict["transitions"] = {k: v for k, v in base_dict["transitions"].items()}
        base_dict["pref_graph"]["nodes"] = {ast.literal_eval(k): v for k, v in base_dict["pref_graph"]["nodes"].items()}
        base_dict["pref_graph"]["edges"] = {
            ast.literal_eval(k): {ast.literal_eval(kk) for kk in v}
            for k, v in base_dict["pref_graph"]["edges"].items()
        }

        if input_symbols == None:
            alphabet = base_dict['alphabet']
            input_symbols_sets = MU.powerset_of_set(alphabet)
            input_symbols = set()
            for s in input_symbols_sets:
                input_symbols.add(tuple(s))

        #print(f"input_symbols: {input_symbols}")
        #return

        states = base_dict["states"]

        transitions = {}
        for state in states:
            transitions[state] = {}

        for state in states:
            #print(f"{state}: {base_dict['transitions'][state]}")
            for key in base_dict['transitions'][state].keys():
                # print(f"key: {key}")
                # print(f"base_dict['transitions'][state][key]]: {base_dict['transitions'][state][key]}")
                key_letters = ALU.getLetters(input_symbols, key)
                print(f"key: {key}, key_letters: {key_letters}")
                # print(f"key_letter: {key_letter}")
                for key_letter in key_letters:
                    transitions[state][key_letter] = str(base_dict['transitions'][state][key])
        initial_state = str(base_dict['init_state'])
        #print(f"type: {type(initial_state)}")

        pgraph_nodes = []

        node_tuple_dict = {}

        for key in base_dict['pref_graph']['nodes'].keys():
            nodes = base_dict['pref_graph']['nodes'][key]
            st = set()
            for node in nodes:
                st.add(str(node))
            tple = tuple(st)
            pgraph_nodes.append(tple)
            node_tuple_dict[key] = tple

        # print(f"pgraph_nodes: {pgraph_nodes}")

        pgraph_edges = []
        for key in base_dict['pref_graph']['edges'].keys():
            edge = base_dict['pref_graph']['edges'][key]
            e1 = node_tuple_dict[key]
            for dest in edge:
                if dest == key:
                    continue
                e2 = node_tuple_dict[dest]
                pgraph_edges.append((e1, e2))
        # print(f"pgraph_edges: {pgraph_edges}")

        prefGraph = Graph()
        for node in pgraph_nodes:
            prefGraph.addVertex(node)
        for edge in pgraph_edges:
            prefGraph.addEdge(edge)

        # print(f"states: {base_dict['states']}")
        # print(f"transitions: {base_dict['transitions']}")
        # print(f"pref_nodes: {base_dict['pref_graph']['nodes']}")
        # print(f"{type(base_dict['pref_graph']['nodes'])}")
        # print(f"pref_edges: {base_dict['pref_graph']['edges']}")

        print(f"states: {states}")
        print(f"transitions: {transitions}")
        print(f"initial_state: {initial_state}")

        if not ALU.isComplete(transitions=transitions, alphabet=input_symbols, states=states):
            q_trap = ALU.get_trapping_state(transitions=transitions, alphabet=input_symbols, states=states)
            print(f"q_trap: {q_trap}")
            if q_trap == None:
                q_trap = "q_trap"
                states.append(q_trap)
            ALU.addMissingTransitions(transitions=transitions, alphabet=input_symbols, states=states, q_trap=q_trap)

        pdfa = PreferenceDFA(states=states, input_symbols=input_symbols, transitions=transitions, initial_state=initial_state, prefGraph=prefGraph)

        pdfa.set_prefGraph(prefGraph)

        pdfa.printToFile("pdfa.txt")

        return pdfa

    def save_to_file(self, file_name="Garden_prefDFA.json"):
        f = open(file_name, "w")
        json_str = jsonpickle.encode(self)
        f.write(json_str)
        f.close()

    def load_from_file(file_name="Garden_prefDFA.json"):
        f = open(file_name, "r")
        json_str = f.read()
        prefDFA = jsonpickle.decode(json_str)
        f.close()
        return prefDFA

    def get_state_vertex_in_pref_graph(self, state):
        #print(f"len(self.state_vertex_in_pref_graph.keys()): {len(self.state_vertex_in_pref_graph.keys())}")
        if len(self.state_vertex_in_pref_graph.keys()) == 0:
            self.compute_state_vertex_in_pref_graph()
        return self.state_vertex_in_pref_graph[state]

    def compute_state_vertex_in_pref_graph(self):
        for vertex in self.prefGraph.vertices:
            for state in vertex:
                #print(f"State {state} in vertex {vertex}")
                self.state_vertex_in_pref_graph[state] = vertex

    def is_isomorphic(self, preferenceDFA):
        if len(preferenceDFA.states) != len(self.states):
            return False
        if len(preferenceDFA.prefGraph.vertices) != len(self.prefGraph.vertices):
            return False
        dict = {}
        queue = []
        R = []
        t = (self.initial_state, preferenceDFA.initial_state)
        R.append(t)
        queue.append(t)
        i = 0
        while i<= len(queue):
            t = queue[i]
            q = t[0]
            p = t[1]
            if q not in dict:
                dict[q] = p
            elif dict[q] != p:
                return False
            for a in self.input_symbols:
                q2 = self.transitions[q][a]
                p2 = preferenceDFA.transitions[p][a]
                if (q2, p2) not in queue:
                    queue.append((q2, p2))






    def compute_bisimilairty_realtion(self):
        self.prefGraph.compute_connectivity_matrix()
        print(self.prefGraph.connectivity_matrx)
        if len(self.state_vertex_in_pref_graph.keys()) == 0:
            self.compute_state_vertex_in_pref_graph()

        # if isPrefGraphAcyclic:
        #     for v in self.prefGraph.vertices:
        #         v_states = list(v)
        #         for s1 in v_states:
        #             for s2 in v_states:
        #                 R.append((s1, s2))

        R = []
        for s1 in self.states:
            for s2 in self.states:
                v1 = self.state_vertex_in_pref_graph[s1]
                v2 = self.state_vertex_in_pref_graph[s2]
                if self.prefGraph.connectivity_matrx[v1][v2] and self.prefGraph.connectivity_matrx[v2][v1]:
                    addToRelation = True
                    for a in self.input_symbols:
                        s1_a = self.transitions[s1][a]
                        s2_a = self.transitions[s2][a]
                        v1_2 = self.state_vertex_in_pref_graph[s1_a]
                        v2_2 = self.state_vertex_in_pref_graph[s2_a]
                        if (not self.prefGraph.connectivity_matrx[v1_2][v2_2]) or (
                        not self.prefGraph.connectivity_matrx[v2_2][v1_2]):
                            addToRelation = False
                            break
                    if addToRelation:
                        R.append((s1, s2))

        changed = True
        i = 0
        while changed:
            changed = False
            i += 1
            print(f"i = {i}")
            print(f"size of R = {len(R)}")
            toRemove = set()
            j = 0
            for t in R:
                j += 1
                # print(f"j = {j}, |R|={len(R)}")
                print(f"j = {j}, |R|={len(R)}, |toRemove|={len(toRemove)}")
                remove = False
                for a in self.input_symbols:
                    if ((self.transitions[t[0]][a], self.transitions[t[1]][a]) not in R) or (
                            (self.transitions[t[0]][a], self.transitions[t[1]][a]) in toRemove):
                        remove = True
                        # R = list(set(R).difference({t}))
                        toRemove.add(t)
                        break
                if len(toRemove) > 100:
                    break

                # if remove:
                #     R = list(set(R).difference({t}))
                #     changed = True
            lastSize = len(R)
            R = list(set(R).difference(toRemove))
            if lastSize != len(R):
                changed = True
        return R

        print(f"Bisimilarity relation: {R}")

    def minimize(self):
        R = self.compute_bisimilairty_realtion()
        paritioning = MU.equivalence_partition_as_list_of_list(self.states, R)
        state_class = {}
        for p in paritioning:
            for s in p:
                state_class[s] = p

        print(f"Equivalence classes of the bisimilarity relation: {paritioning}")

        new_states = []
        for p in paritioning:
            new_states.append(str(p))

        new_transitions = {}
        for i in range(len(new_states)):
            s = new_states[i]
            p = paritioning[i]
            new_transitions[s] = {}
            for a in self.input_symbols:
                q2 = self.transitions[p[0]][a]
                new_transitions[s][a] = str(state_class[q2])

        new_initial_state = str(state_class[self.initial_state])

        new_pref_graph = Graph()
        for p in paritioning:
            vertex = tuple(p)
            new_pref_graph.addVertex(vertex)

        for e in self.prefGraph.edges:
            src = tuple(state_class[e[0][0]])  # e[0] is the source vertex of the graph
            # e[0][0] is the first element in the tuple t[0]
            # each vertex of the graph is a tuple reperesntign a list of states of the DFA
            dst = tuple(state_class[e[1][0]])
            newEdge = (src, dst)
            new_pref_graph.addEdge(newEdge)

        # print(f"------------------old preference garph-----------------")
        # self.prefGraph.printAll()
        # print(f"------------------new preference graph-----------------")
        # new_pref_graph.printAll()

        new_pref_dfa = PreferenceDFA(states=set(new_states), input_symbols=self.input_symbols,
                                     transitions=new_transitions, initial_state=new_initial_state,
                                     prefGraph=new_pref_graph)

        # print(f"--------------------Old Preference DFA----------------------")
        # AU.printDFA(self)

        # print(f"---------------------New Preference DFA--------------------")
        # AU.printDFA(new_pref_dfa)

        return new_pref_dfa


    def get_shortest_prefixes(self):
        if self.shortest_prefixes == None:
            self.compute_shortest_prefixes()
        return self.shortest_prefixes_all

    '''
    The state reached by tracing a word from the initial state.
    '''
    def compute_shortest_prefixes(self):
        self.shortest_prefixes = {}
        unvisited_states = []
        for q in self.states:
            unvisited_states.append(q)
        ordered_symbols =  sorted(self.input_symbols)
        self.shortest_prefixes[self.initial_state] = []
        print(self.shortest_prefixes[self.initial_state])
        unvisited_states.remove(self.initial_state)
        queue = []
        queue.append(self.initial_state)
        while queue:
            q = queue.pop(0)
            for a in ordered_symbols:
                q2 = self.transitions[q][a]
                if q2 in unvisited_states:
                    #print(f"q2: {q2}, self.shortest_prefixes[{q}]: {self.shortest_prefixes[q]}")
                    if q != self.initial_state:
                        sp = self.shortest_prefixes[q].copy()
                        sp.append(str(a))
                    else:
                        sp = [str(a)]
                    self.shortest_prefixes[q2] = sp
                    unvisited_states.remove(q2)
                    queue.append(q2)

        # while unvisited_states:
        #     for q in self.states:
        #         if q in self.shortest_prefixes.keys():
        #             for a in ordered_symbols:
        #                 q2 = self.transitions[q][a]
        #                 if q2 not in self.shortest_prefixes.keys():
        #                     print(f"q2: {q2}, self.shortest_prefixes[{q}]: {self.shortest_prefixes[q]}")
        #                     if q != self.initial_state:
        #                         sp =self.shortest_prefixes[q].copy()
        #                         sp.append(str(a))
        #                     else:
        #                         sp = [str(a)]
        #                     self.shortest_prefixes[q2] = sp
        #                     unvisited_states.remove(q2)
        print(self.shortest_prefixes)

        self.shortest_prefixes_all = []
        for q in self.states:
            self.shortest_prefixes_all.append(self.shortest_prefixes[q])



    def get_nuclues(self):
        if self.nuclues == None:
            self.compute_nuclues()
        return self.nuclues


    def compute_nuclues(self):
        self.nuclues = []
        self.nuclues.append([])
        ordered_input_symbols = sorted(self.input_symbols)
        self.get_shortest_prefixes()
        for w in self.shortest_prefixes_all:
            for a in ordered_input_symbols:
                if w == []:
                    nu = [str(a)]
                    self.nuclues.append(nu)
                else:
                    nu = w.copy()
                    nu.append(str(a))
                    self.nuclues.append(nu)
        print(self.nuclues)




    def compare(self, w1, w2):
        q1 = self.trace(w1)
        q2 = self.trace(w2)
        v1 = self.get_state_vertex_in_pref_graph(q1)
        v2 = self.get_state_vertex_in_pref_graph(q2)
        if v1 == v2:
            return 0
        elif v2 in self.prefGraph.getVerticesPreferredBy(v1):
            return 1
        elif v2 in self.prefGraph.getVerticesPreferredTo(v1):
            return -1
        else:
            return 2


    def trace(self, word=[]):
        q = self.initial_state

        for i in range(len(word)):
            # q = self.transitions[q][tuple(word[i])]
            # q = self.transitions[q][str(word[i])]
            q = self.transitions[q][word[i]]
        return q

        elem_type = type(list(self.input_symbols))
        if len(word)>0 and elem_type != type(word[0]):
            for i in range(len(word)):
                q = self.transitions[q][elem_type(word[i])]
        else:
            for i in range(len(word)):
                #q = self.transitions[q][tuple(word[i])]
                #q = self.transitions[q][str(word[i])]
                q = self.transitions[q][word[i]]

        return q

    '''
    The set of all states to which the DFA reaches by tracing all the words 
    generated from permuations of a list of letters.

    Example: The list of all words generated from permutations of letters [a, b, c] are
            abc, acb, bac, bca, cab, cba.
    '''

    def statesReachableByPermuationsOfLetters(self, letters):
        reachableStates = []
        for word in list(permutations(letters)):
            reachableStates.append(self.trace(word))
        return reachableStates

    '''
    Return all states that are within a specific distance of the initial state
    '''

    def getStatesAt(self, level):
        queue = []
        queueLevel = []
        queue.append(self.initial_state)
        queueLevel.append(1)

        result = []
        while queue:
            q = queue.pop(0)
            l = queueLevel.pop(0)
            if l > level:
                continue
            if l == level:
                result.append(q)
            else:
                for a in self.input_symbols:
                    if (self.transitions[q][a] not in queue) and (self.transitions[q][a] not in result):
                        queue.append(self.transitions[q][a])
                        queueLevel.append(l + 1)
        return result

    def printToFile(self, filepath):
        f = open(filepath, "w")
        f.write(f"The preference DFA has {len(self.states)} states. \n")
        f.write(
            f"Its preference graph has {len(self.prefGraph.vertices)} vertices and {len(self.prefGraph.edges)} edges. \n")
        f.write(f"input_symbols={self.input_symbols} \n")
        f.write(f"initial_state={self.initial_state} \n")
        f.write(f"states={self.states} \n")
        f.write(f"transitions={self.transitions} \n")
        f.write(f"vertices={self.prefGraph.vertices} \n")
        f.write(f"edges = {self.prefGraph.edges} \n")
        #f.write(f"type of a state: {type(self.states[0])}")
        f.close()



