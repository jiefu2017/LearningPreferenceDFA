
from Learning import PreferenceSample

import time

import graphviz

class RPNIMooreBased():
    def __init__(self, preferenceSample, generator_preferenceDFA = None):
        self.preferenceSample = preferenceSample
        self.generator_preferenceDFA = generator_preferenceDFA

    def is_sample_characterstic(self):
        result = True
        print(f"Start checking if the sample is characteristic")
        start_time = time.time()

        is_nuclues_subset_of_prefixes_result = self.is_nuclues_subset_of_prefixes()
        if False == is_nuclues_subset_of_prefixes_result:
            print("The sample is not characteristic: The nuclues is not a subset of the sample's prefixes")
            result = False

        is_shortestprefixes_and_nuclues_reachingdifferentstates_distinguishable_result = self.is_shortestprefixes_and_nuclues_reachingdifferentstates_distinguishable()
        if False == is_shortestprefixes_and_nuclues_reachingdifferentstates_distinguishable_result:
            print("The sample is not characteristic: Some words within the short prefixes are indistinguishable from some words within the nuclues.")
            result = False

        are_all_vertices_of_prefGraph_covered_result = self.are_all_vertices_of_prefGraph_covered()
        if False == are_all_vertices_of_prefGraph_covered_result:
            print("Not all the verties of the preference graph are covered")
            result = False

        are_comparisons_accurate_result = self.are_comparisons_accurate()
        if False == are_comparisons_accurate_result:
            print("The sample is not characteristic: The sample does not compare some words that are not indifferent")
            result = False

        print(f"End checking if the sample is characteristic")
        elapsed_time = time.time()-start_time
        print(f"Time to check if the sample is characteristic: {elapsed_time}")
        return result, (is_nuclues_subset_of_prefixes_result, is_shortestprefixes_and_nuclues_reachingdifferentstates_distinguishable_result, are_all_vertices_of_prefGraph_covered_result, are_comparisons_accurate_result)



    def are_all_vertices_of_prefGraph_covered(self):
        words = self.preferenceSample.words
        vertices = []
        for w in words:
            q = self.generator_preferenceDFA.trace(w)
            vertex = self.generator_preferenceDFA.get_state_vertex_in_pref_graph(q)
            if vertex not in vertices:
                vertices.append(vertex)
            if len(vertices) == len(self.generator_preferenceDFA.prefGraph.vertices):
                return True

        if len(vertices) == len(self.generator_preferenceDFA.pref_graph.vertices):
            return True
        return False

    def is_nuclues_subset_of_prefixes(self):
        words = self.preferenceSample.words
        nuclues = self.generator_preferenceDFA.get_nuclues()

        not_started_with_list = nuclues.copy()
        found_list  = []

        for w in words:
            found_list = []
            for w2 in not_started_with_list:
                #print(f"w_string: {''.join(w)}")
                #print(f"w2_string: {''.join(w2)}")
                if "".join(w).startswith("".join(w2)):
                    found_list.append(w2)
            for w2 in found_list:
                not_started_with_list.remove(w2)

        if len(not_started_with_list) > 0:
            print(f"not_started_with_list: {not_started_with_list}")
            return False
        else:
            return True


    def is_shortestprefixes_and_nuclues_reachingdifferentstates_distinguishable(self):
        sp = self.generator_preferenceDFA.get_shortest_prefixes()
        nu = self.generator_preferenceDFA.get_nuclues()

        pairs_to_distinguish = []
        for w in sp:
            for u in nu:
                q = self.generator_preferenceDFA.trace(w)
                q2 = self.generator_preferenceDFA.trace(u)
                #print(f"q: {q}, q2: {q2}")
                if q != q2:
                    pairs_to_distinguish.append((w, u))

        #print(f"pairs_to_distinguish: {pairs_to_distinguish}")
        sample_closure = self.preferenceSample.get_closure()
        for (w1, w2, b) in sample_closure:
            dist_pairs = []
            if b == 1 or b == 2:
                for (w, u) in pairs_to_distinguish:
                    if len(w1) < len(w) or len(w2) < len(u):
                        continue
                    if ''.join(w1).startswith(''.join(w)) and ''.join(w2).startswith(''.join(u)) and ''.join(w1[len(''.join(w)):]) == ''.join(w2[len(''.join(u)):]):
                        dist_pairs.append((w, u))
                for (u, w) in pairs_to_distinguish:
                    if len(w1) < len(w) or len(w2) < len(u):
                        continue
                    if ''.join(w1).startswith(''.join(w)) and ''.join(w2).startswith(''.join(u)) and ''.join(w1[len(''.join(w)):]) == ''.join(w2[len(''.join(u)):]):
                        dist_pairs.append((u, w))

            for t in dist_pairs:
                if t in pairs_to_distinguish:
                    pairs_to_distinguish.remove(t)

        if len(pairs_to_distinguish) == 0:
            return True
        else:
            print(f"Pairs that are not distinguished by the sample: {pairs_to_distinguish}")
            return False




    def learn_preferenceDFA_By_Eq_graph_parition(self, visualize = True):
        #partition = self.preferenceSample.compute_closure_using_graph()

        start_time = time.time()



        graph = self.preferenceSample.compute_pref_graph()
        #partition = graph.vertices
        partition = graph.partition


        data = []
        for w in self.preferenceSample.words:
            B = None
            for b in partition:
                if w in b:
                    B = b
                    break
            #data.append((w, B))
            data.append((w, partition.index(B)))

        from aalpy.learning_algs import run_RPNI
        print(f"Start Moore_RPNI")
        start_time_2 = time.time()
        model = run_RPNI(data, automaton_type='moore')
        elapsed_time_2 = time.time()-start_time_2
        print(f"Time of Moore_RPNI: {elapsed_time_2}")

        elapsed_time = time.time() - start_time

        print(f"execution time: {elapsed_time}")



        if visualize:
            model.visualize()
            dot = graphviz.Digraph()
            for v in graph.vertices:
                dot.node(str(v), str(v))
            for e in graph.edges:
                B1 = graph.partition[e[0]]
                B2 = graph.partition[e[1]]
                dot.edge(str(e[0]), str(e[1]), "")
            dot.render('preference graph', view=True)


        return (model, graph)

        # for B in partition:
        #     dot.node(str(partition.index(B)), str(partition.index(B)))
        # for e in graph.edges:
        #     B1 = list(e[0])
        #     B2 = list(e[1])
        #     dot.edge(str(partition.index(B1)), str(partition.index(B2)), str(partition.index(B1))+"_"+str(partition.index(B2)))





    def are_comparisons_accurate(self):
        words = self.preferenceSample.words
        for w in words:
            for u in words:
                if w == u:
                    continue
                b = self.generator_preferenceDFA.compare(w, u)
                result = self.preferenceSample.get_tuples_in_closure(w, u)
                if len(result) == 0:
                    if b == 0 or b == 1:
                        print(f"{w} and {u} not compared by the sample")
                        return False
                    elif b == -1:
                        result = self.preferenceSample.get_tuples_in_closure(u, w)
                        if len(result) == 0:
                            print(f"{u} and {w} not compared by the sample")
                            return False
                        elif result[0][2] != 1:
                            print(f"{u} and {w} produced wrong comparison")
                            return  False

                else:
                    if (b == 0 or b == 1 or b == 2) and result[0][2] != b:
                        print(f"{w} and {u} produced wrong comparison")
                        return False
                    elif b == -1:
                        print(f"{w} and {u} produced wrong comparison")
                        return False
        return True

    def learn_preferenceDFA(self):
        print(f"Learning the preference DFA")
        closure = self.preferenceSample.get_closure()
        equiv_relation = []
        for (w, u, b) in closure:
            if b == 0:
                equiv_relation.append((w, u))
        partitions = self.get_partitions_of_equivRelation(equiv_relation)

        print(f"len(partitions): {len(partitions)}")

        data = []
        for w in self.preferenceSample.words:
            B = None
            for b in partitions:
                if w in b:
                    B = b
                    break
            data.append((w, B))

        from aalpy.learning_algs import run_RPNI
        model = run_RPNI(data, automaton_type='moore')
        model.visualize()

        return model

    def get_partitions_of_equivRelation(self, equiv_relation):
        partitions = []  # Found partitions
        for w in self.preferenceSample.words:
            found = False  # Note it is not yet part of a know partition
            for p in partitions:
                if (w, p[0]) in equiv_relation:  # Found a partition for it!
                    p.append(w)
                    found = True
                    break
            if not found:  # Make a new partition for it.
                partitions.append([w])
        return partitions









        



