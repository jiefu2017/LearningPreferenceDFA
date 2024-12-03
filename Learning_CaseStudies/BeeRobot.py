from Learning.Graph import Graph
from Learning.PreferenceDFA import PreferenceDFA
from Learning.PreferenceSample import PreferenceSample
from Learning.RPNIMooreBased import RPNIMooreBased

from Learning.Sampler import Sampler

import Utility.AutomataUtility as AU
import time

class BeeRobot():
    def __init__(self):
        self.type = "BeeRobot"
        self.record_blank = False
        self.prefDFA = self.make_PrefDFA2()
        self.prefDFA.compute_shortest_prefixes()
        self.prefDFA.compute_nuclues()

        #self.mdp = TermMDP.load_from_file("garden_mdp.json")
        # garden = Garden()
        # self.mdp = garden.mdp
        # self.mdp.save_to_file("garden_mdp.json")
        #words = PreferenceSample.load_words_from_file("garden_sample_words.json")
        #words = self.mdp.get_all_traces(record_empty_label = self.record_blank)
        #PreferenceSample.save_words_to_file(words, "garden_sample_words.json")
        #words = self.convert_words_to_another_alphabet(words)




    def single_experiment(self):
        sampler = Sampler()
        words = sampler.sample_words(self.prefDFA.input_symbols, 500)
        self.pref_sample = PreferenceSample.create_sample(words, self.prefDFA, 80)

        rpniMooreBased = RPNIMooreBased(preferenceSample=self.pref_sample, generator_preferenceDFA=self.prefDFA)
        self.pref_sample.compute_closure_using_graph()
        print(f"is characterstici: {rpniMooreBased.is_sample_characterstic()}")
        #rpniMooreBased.learn_preferenceDFA()
        moore_aut, pref_graph = rpniMooreBased.learn_preferenceDFA_By_Eq_graph_parition(visualize=True)
        print(f"accurately_learned: {self.is_learned_pdfa_accurate(moore_aut, pref_graph)}")


    def random_words_experiment(self):
        sizes = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        times = 10
        st = "<table>\n"
        st += "<tr>\n"
        st += "<th>Words</th>\n"
        st += "<th>Samples</th>"
        st += "<th>IsCharacteristic</th>\n"
        st += "<th>Cond_NU_Subset</th>\n"
        st += "<th>Cond_NU_SP</th>\n"
        st += "<th>Cond_Pref_Vertices_Covered</th>\n"
        st += "<th>Cond_Correct_Comps</th>\n"
        st += "<th>States</th>\n"
        st += "<th>Preference_Partitions</th>\n"
        st += "<th>Correct</th>\n"
        st += "<th>Time</th>\n"
        st += "</tr>\n"

        st2 = "<table>\n"
        st2 += "<tr>\n"
        st2 += "<th>Words</th>\n"
        st2 += "<th>Samples</th>\n"
        st2 += "<th>Characteristic_Count</th>\n"
        st2 += "<th>Cond_NU_Subset</th>\n"
        st2 += "<th>Cond_NU_SP</th>\n"
        st2 += "<th>Cond_Pref_Vertices_Covered</th>\n"
        st2 += "<th>Cond_Correct_Comps</th>\n"
        st2 += "<th>Correct</th>\n"
        st2 += "<th>Time</th>\n"
        st2 += "</tr>\n"


        for size in sizes:
            isCharacterstic_count = 0
            Cond_NU_Subset_Count = 0
            Cond_NU_SP_Count = 0
            Cond_Pref_Vertices_Covered_Count = 0
            Cond_Correct_Comps_Count = 0
            Correct_Count = 0
            Time_Sum = 0
            for i in range(times):
                start_time = time.time()
                st += "<tr>\n"
                st += "<td>"+str(size)+"</td>\n"
                sample = Sampler()
                words = sample.sample_words(self.prefDFA.input_symbols, size)
                self.pref_sample = PreferenceSample.create_sample(words, self.prefDFA, sampling_type=2, tuples_sampled_portion=2, comparisons_per_item=size//3)
                rpniMooreBased = RPNIMooreBased(preferenceSample=self.pref_sample, generator_preferenceDFA=self.prefDFA)
                self.pref_sample.compute_closure_using_graph()
                is_characterstic, conditions_satisfications = rpniMooreBased.is_sample_characterstic()
                print(f"is characterstici: {is_characterstic}")
                st += "<td>" + str(len(self.pref_sample.sample)) + "</td>\n"
                st += "<td>" + str(is_characterstic) + "</td>\n"
                st += "<td>" + str(conditions_satisfications[0]) + "</td>\n"
                st += "<td>" + str(conditions_satisfications[1]) + "</td>\n"
                st += "<td>" + str(conditions_satisfications[2]) + "</td>\n"
                st += "<td>" + str(conditions_satisfications[3]) + "</td>\n"
                model, pref_grap = rpniMooreBased.learn_preferenceDFA_By_Eq_graph_parition(visualize=False)
                st += "<td>"+str(len(model.states))+"</td>\n"
                st += "<td>" + str(len(pref_grap.vertices)) + "</td>\n"
                # if len(model.states) == 6 and len(paritions)==4:
                #     st += "<td>" + str(True) + "</td>\n"
                # else:
                #     st += "<td>" + str(False) + "</td>\n"
                accurate_learned =self.is_learned_pdfa_accurate(model, pref_grap)
                st += "<td>"+str(accurate_learned)+"</td>\n"
                elapsed_time = time.time()-start_time
                st += "<td>"+str(elapsed_time)+"</td>\n"
                st += "</tr>\n"

                f = open("beeRobot_experiment_results_details.html", "w+")
                f.write(st)
                f.close()

                if is_characterstic:
                    isCharacterstic_count += 1
                if conditions_satisfications[0] == False:
                    Cond_NU_Subset_Count += 1
                if conditions_satisfications[1] == False:
                    Cond_NU_SP_Count += 1
                if conditions_satisfications[2] == False:
                    Cond_Pref_Vertices_Covered_Count += 1
                if conditions_satisfications[3] == False:
                    Cond_Correct_Comps_Count += 1
                if accurate_learned:
                    Correct_Count += 1
                Time_Sum += elapsed_time
            Time_Avg = Time_Sum/10
            st2 += "<tr>\n"
            st2 += "<td>"+str(size)+"</td>\n"
            st2 += "<td>" + str(len(self.pref_sample.sample)) + "</td>\n"
            st2 += "<td>"+str(isCharacterstic_count)+"</td>\n"
            st2 += "<td>"+str(Cond_NU_Subset_Count)+"</td>\n"
            st2 += "<td>"+str(Cond_NU_SP_Count)+"</td>\n"
            st2 += "<td>"+str(Cond_Pref_Vertices_Covered_Count)+"</td>\n"
            st2 += "<td>"+str(Cond_Correct_Comps_Count)+"</td>\n"
            st2 += "<td>"+str(Correct_Count)+"</td>\n"
            st2 += "<td>"+str(Time_Avg)+"</td>\n"
            st2 += "</tr>\n"

            f = open("beeRobot_experiment_results_summary.html", "w+")
            f.write(st2)
            f.close()

        st += "</table>\n"

        f = open("beeRobot_experiment_results.html", "w+")
        f.write(st)
        f.close()

        f = open("beeRobot_experiment_results_summary.html", "w+")
        f.write(st2)
        f.close()





    def make_PrefDFA(self):
        p = ""
        t = "t"
        c = "o"
        d = "d"
        input_symbols = set()
        input_symbols.add(p)
        input_symbols.add(t)
        input_symbols.add(c)
        input_symbols.add(d)
        states = ["q0", "q1", "q2", "q3", "q4", "q5"]
        transitions = {}
        transitions["q0"] = {}
        transitions["q0"][t] = "q1"
        transitions["q0"][p] = "q0"
        transitions["q0"][c] = "q3"
        transitions["q0"][d] = "q5"

        transitions["q1"] = {}
        transitions["q1"][p] = "q1"
        transitions["q1"][t] = "q1"
        transitions["q1"][c] = "q2"
        transitions["q1"][d] = "q2"

        transitions["q2"] = {}
        transitions["q2"][p] = "q2"
        transitions["q2"][t] = "q2"
        transitions["q2"][c] = "q2"
        transitions["q2"][d] = "q2"

        transitions["q3"] = {}
        transitions["q3"][p] = "q3"
        transitions["q3"][t] = "q4"
        transitions["q3"][c] = "q3"
        transitions["q3"][d] = "q4"

        transitions["q4"] = {}
        transitions["q4"][p] = "q4"
        transitions["q4"][t] = "q4"
        transitions["q4"][c] = "q4"
        transitions["q4"][d] = "q4"

        transitions["q5"] = {}
        transitions["q5"][p] = "q5"
        transitions["q5"][t] = "q4"
        transitions["q5"][c] = "q4"
        transitions["q5"][d] = "q5"


        initial_state = "q0"


        prefGraph = Graph()
        v0 = tuple({"q2"})
        v1 = tuple({"q4"})
        v2 = tuple({"q1"})
        v3 = tuple({"q0", "q3", "q5"})
        prefGraph.addVertex(v0)
        prefGraph.addVertex(v1)
        prefGraph.addVertex(v2)
        prefGraph.addVertex(v3)
        # e1 = tuple((v0, v1))
        # e2 = tuple((v0, v2))
        # e3 = tuple((v1, v3))
        # e4 = tuple((v2, v3))
        e1 = tuple((v1, v0))
        e2 = tuple((v2, v0))
        e3 = tuple((v3, v1))
        e4 = tuple((v3, v2))
        prefGraph.addEdge(e1)
        prefGraph.addEdge(e2)
        prefGraph.addEdge(e3)
        prefGraph.addEdge(e4)

        pdfa = PreferenceDFA(states=set(states), input_symbols=input_symbols, transitions=transitions, initial_state=initial_state,
                  prefGraph=prefGraph)

        AU.printDFA(pdfa)
        print("Preference DFA is made")
        return pdfa


    def convert_word_to_another_alphabet(self, word):
        result = []
        for i in range(len(word)):
            if word[i] == set() and self.record_blank:
                result.append("B")
            elif word[i] == {'t'}:
                result.append("t")
            elif word[i] == {'o'}:
                result.append("o")
            elif word[i] == {'d'}:
                result.append("d")
        return result
    def convert_words_to_another_alphabet(self, words):
        result = []
        for word in words:
            result.append(self.convert_word_to_another_alphabet(word))
        return result

    def is_learned_pdfa_accurate(self, moore_aut, pref_graph):
        if len(moore_aut.states) != 6:
            return False
        t = "t"
        o = "o"
        d = "d"
        s0 = moore_aut.initial_state
        s1 = moore_aut.states[1]
        s2 = moore_aut.states[2]
        s3 = moore_aut.states[3]
        s4 = moore_aut.states[4]
        s5 = moore_aut.states[5]

        if s0.transitions[d] != s1:
            return False
        if s0.transitions[o] != s2:
            return False
        if s0.transitions[t] != s3:
            return False

        if s1.transitions[d] != s1:
            return False
        if s1.transitions[o] != s4:
            return False
        if s1.transitions[t] != s4:
            return False

        if s2.transitions[d] != s4:
            return False
        if s2.transitions[o] != s2:
            return False
        if s2.transitions[t] != s4:
            return False

        if s3.transitions[d] != s5:
            return False
        if s3.transitions[o] != s5:
            return False
        if s3.transitions[t] != s3:
            return False

        if s4.transitions[d] != s4:
            return False
        if s4.transitions[o] != s4:
            return False
        if s4.transitions[t] != s4:
            return False

        if s5.transitions[d] != s5:
            return False
        if s5.transitions[o] != s5:
            return False
        if s5.transitions[t] != s5:
            return False

        print(pref_graph.vertices)
        print(pref_graph.edges)

        s0_output = s0.output
        s3_output = s3.output
        s4_output = s4.output
        s5_output = s5.output

        if (s0_output, s5_output) not in pref_graph.edges:
            print(f"{(s0_output, s5_output)} not in edges")
            return False

        if (s3_output, s5_output) not in pref_graph.edges:
            print(f"{(s3_output, s5_output)} not in edges")
            return False

        if (s4_output, s5_output) not in pref_graph.edges:
            print(f"{(s4_output, s5_output)} not in edges")
            return False

        if (s0_output, s3_output) not in pref_graph.edges:
            print(f"{(s0_output, s3_output)} not in edges")
            return False

        if (s0_output, s4_output) not in pref_graph.edges:
            print(f"{(s0_output, s4_output)} not in edges")
            return False

        return True


    def make_PrefDFA2(self):
        p = "B"
        t = "t"
        c = "o"
        d = "d"
        input_symbols = set()
        if self.record_blank:
            input_symbols.add(p)
        input_symbols.add(t)
        input_symbols.add(c)
        input_symbols.add(d)
        states = ["q0", "q1", "q2", "q3", "q4", "q5"]
        transitions = {}
        transitions["q0"] = {}
        transitions["q0"][t] = "q1"
        if self.record_blank:
            transitions["q0"][p] = "q0"
        transitions["q0"][c] = "q3"
        transitions["q0"][d] = "q5"

        transitions["q1"] = {}
        if self.record_blank:
            transitions["q1"][p] = "q1"
        transitions["q1"][t] = "q1"
        transitions["q1"][c] = "q2"
        transitions["q1"][d] = "q2"

        transitions["q2"] = {}
        if self.record_blank:
            transitions["q2"][p] = "q2"
        transitions["q2"][t] = "q2"
        transitions["q2"][c] = "q2"
        transitions["q2"][d] = "q2"

        transitions["q3"] = {}
        if self.record_blank:
            transitions["q3"][p] = "q3"
        transitions["q3"][t] = "q4"
        transitions["q3"][c] = "q3"
        transitions["q3"][d] = "q4"

        transitions["q4"] = {}
        if self.record_blank:
            transitions["q4"][p] = "q4"
        transitions["q4"][t] = "q4"
        transitions["q4"][c] = "q4"
        transitions["q4"][d] = "q4"

        transitions["q5"] = {}
        if self.record_blank:
            transitions["q5"][p] = "q5"
        transitions["q5"][t] = "q4"
        transitions["q5"][c] = "q4"
        transitions["q5"][d] = "q5"


        initial_state = "q0"


        prefGraph = Graph()
        v0 = tuple({"q2"})
        v1 = tuple({"q4"})
        v2 = tuple({"q1"})
        v3 = tuple({"q0", "q3", "q5"})
        prefGraph.addVertex(v0)
        prefGraph.addVertex(v1)
        prefGraph.addVertex(v2)
        prefGraph.addVertex(v3)
        # e1 = tuple((v0, v1))
        # e2 = tuple((v0, v2))
        # e3 = tuple((v1, v3))
        # e4 = tuple((v2, v3))
        e1 = tuple((v1, v0))
        e2 = tuple((v2, v0))
        e3 = tuple((v3, v1))
        e4 = tuple((v3, v2))
        prefGraph.addEdge(e1)
        prefGraph.addEdge(e2)
        prefGraph.addEdge(e3)
        prefGraph.addEdge(e4)

        pdfa = PreferenceDFA(states=set(states), input_symbols=input_symbols, transitions=transitions, initial_state=initial_state,
                  prefGraph=prefGraph)

        AU.printDFA(pdfa)
        print("Preference DFA is made")
        return pdfa

