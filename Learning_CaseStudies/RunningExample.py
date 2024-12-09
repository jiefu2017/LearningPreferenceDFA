from Learning import PreferenceDFA
from Learning.PreferenceSample import PreferenceSample
from Learning.RPNIMooreBased import RPNIMooreBased
from Learning.Graph import Graph
from Learning.PreferenceDFA import PreferenceDFA
from Learning import UGraph
import Utility.AutomataUtility as AU

class RunningExample():
    def __init__(self):
        self.type = "BeeRobot" # use different groundtruth DFA for generating samples. If only data available, use skip the step
        self.prefDFA = self.make_PrefDFA()
        self.prefDFA.compute_shortest_prefixes()
        self.prefDFA.compute_nuclues()

        self.prefSample = self.make_sample() # if no groundtruth DFA available, replace this line with a given sample of pairwise comparisons

        self.prefSample.compute_closure_using_graph()

        self.rpniMooreBased = RPNIMooreBased(preferenceSample=self.prefSample, generator_preferenceDFA=self.prefDFA)

        #print(f"is_nuclues_subset_of_prefixes: {self.rpniMooreBased.is_nuclues_subset_of_prefixes()}")
        #print(f"is_shortestprefixes_and_nuclues_reachingdifferentstates_distinguishable: {self.rpniMooreBased.is_shortestprefixes_and_nuclues_reachingdifferentstates_distinguishable()}")
        #print(f"are_comparisons_accurate: {self.rpniMooreBased.are_comparisons_accurate()}")
        print(f"is_sample_characteristic: {self.rpniMooreBased.is_sample_characterstic()}")
        self.rpniMooreBased.learn_preferenceDFA_By_Eq_graph_parition()

    def make_PrefDFA(self):
        """
        Construct the preference DFA for the running example. this is the ground truth DFA.
        """
        a = "a"
        b = "b"
        input_symbols = set()
        input_symbols.add(a)
        input_symbols.add(b)
        states = ["00", "10", "01", "11"]
        transitions = {}
        transitions["00"] = {}
        transitions["00"][a] = "10"
        transitions["00"][b] = "01"

        transitions["10"] = {}
        transitions["10"][a] = "00"
        transitions["10"][b] = "11"


        transitions["01"] = {}
        transitions["01"][a] = "11"
        transitions["01"][b] = "00"

        transitions["11"] = {}
        transitions["11"][a] = "01"
        transitions["11"][b] = "10"




        initial_state = "00"


        prefGraph = Graph()
        v0 = tuple({"11"})
        v1 = tuple({"00"})
        v2 = tuple({"01", "10"})
        prefGraph.addVertex(v0)
        prefGraph.addVertex(v1)
        prefGraph.addVertex(v2)
        e1 = tuple((v2, v0))
        e2 = tuple((v2, v1))
        prefGraph.addEdge(e1)
        prefGraph.addEdge(e2)

        pdfa = PreferenceDFA(states=set(states), input_symbols=input_symbols, transitions=transitions, initial_state=initial_state,
                             prefGraph=prefGraph)

        AU.printDFA(pdfa)
        print("Preference DFA is made")
        return pdfa


    def make_sample(self):
        sample = []
        sample.append((["b", "a"], ["a"], 1))
        sample.append((["a"], ["a", "b", "b"], 0))
        sample.append((["b", "a"], ["a", "b", "b", "b"], 0))
        sample.append((["b", "b"], ["a", "b", "b"], 1))
        sample.append((["a", "b", "b"], ["a", "b", "a"], 0))
        sample.append((["a", "b", "b"], ["b", "b", "b"], 0))
        sample.append((["b", "b"], ["a", "a"], 0))
        sample.append((["a", "a"], ["a", "b", "a", "a"], 2))
        sample.append((["a", "a"], ["a", "a", "b", "b"], 0))
        sample.append((["a", "b", "a"], ["b", "a", "a"], 0))
        sample.append((["a", "b", "b", "b"], ["a", "b", "a", "a"], 0))
        prefSample = PreferenceSample(sample)
        return prefSample


    def make_sample_2(self):
        sample = []
        sample.append((["a", "a"], ["a"], 1))
        sample.append((["b", "b"], ["b"], 1))
        sample.append((["b", "b"], ["b"], 1))

        prefSample = PreferenceSample(sample)
        return prefSample

    def learn_prefDFA_mooreBaseAlg(self):
        self.rpniMooreBased.learn_preferenceDFA_By_Eq_graph_parition()

