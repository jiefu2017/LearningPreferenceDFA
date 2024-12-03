import random

import jsonpickle

import time

class PreferenceSample():
    def __init__(self, sample):
        self.sample = sample
        self.words = []
        for t in sample:
            w1 = t[0]
            w2 = t[1]
            if w1 not in self.words:
                self.words.append(w1)
            if w2 not in self.words:
                self.words.append(w2)

    def get_closure(self):
        if hasattr(self, "sample_closure") == False:
        #if self.sample_closure == None:
            self.compute_closure_using_graph()
        return self.sample_closure

    def compute_closure_dict(self):
        if hasattr(self, "sample_closure_dict") == True:
            return self.sample_closure_dict
        self.sample_closure_dict = {}
        for t in self.sample_closure:
            u = t[0]
            u_tuple = tuple(u)
            if u_tuple not in self.sample_closure_dict.keys():
                self.sample_closure_dict[u_tuple] = [t]
            else:
                self.sample_closure_dict[u_tuple].append(t)
        return self.sample_closure_dict


    def compute_closure_using_graph(self):
        print("start computing the closure using graph")
        start_time = time.time()

        graph = self.compute_pref_graph()
        partition = graph.partition

        old_edges = []
        while old_edges != graph.edges:
            old_edges = graph.edges
            for e in graph.edges:
                i = e[0]
                j = e[1]
                for k in range(len(partition)):
                    if (j, k) in graph.edges and (i, k) not in graph.edges:
                        graph.addEdge((i, k))

        closure = []
        for v in graph.vertices:
            B = graph.partition[v]
            for w in B:
                for u in B:
                    closure.append((w, u, 0))

        added = []
        for (w, u, b) in self.sample:
            if b == 1 or b == 2:
                B_w = graph.word_block[tuple(w)]
                B_u = graph.word_block[tuple(u)]
                if (B_w, B_u) not in added:
                    for w2 in B_w:
                        for u2 in B_u:
                            closure.append((w2, u2, b))
                    added.append((B_w, B_u))

        self.sample_closure = closure

        self.compute_closure_dict()

        print("end computing the closure using graph")

        elapsed_time = time.time() - start_time

        print(f"time to compute the closure: {elapsed_time}")

        return closure


    def compute_pref_graph(self):
        edges = []
        for (w, u, b) in self.sample:
            if b == 0 and w != u:
                edges.append((w, u))
        ugraph = UGraph(self.words, edges)
        ugraph.compute_SCCs()

        partition = []
        for scc in ugraph.SCCs:
            B = []
            for v in scc:
                B.append(list(v))
            partition.append(B)
        #return partition

        graph = Graph()
        print(f"partition: {partition}")
        graph.partition = partition
        graph.word_block = dict()
        for B in partition:
            graph.addVertex(partition.index(B))
            for w in B:
                graph.word_block[tuple(w)] = B

        for (w, u, b) in self.sample:
            if b == 1:
                w_B = None
                u_B = None
                for B in partition:
                    if w in B:
                        w_B = B
                    if u in B:
                        u_B = B
                e = (partition.index(u_B), partition.index(w_B))
                graph.addEdge(e)
        return graph



    def compute_closure(self):
        print(f"Computing the closure of the sample")
        print(f"len(self.words: {len(self.words)})")
        print(f"len(self.sample: {len(self.sample)})")
        self.sample_closure = self.sample.copy()
        not_checked_tuples = []
        # for t in self.sample:
        #     print(f"t: {t}, type: {type(t)}")
        #     self.sample_closure.add(t)
            #not_checked_tuples.append(t)
        changed = True

        for w in self.words:
            if tuple((w, w, 0)) not in self.sample_closure:
                self.sample_closure.append(tuple((w, w, 0)))

        sample_closure_temp = []
        loop = 1
        while len(sample_closure_temp) != len(self.sample_closure):
            changed = False
            print(f"loop: {loop}")
            loop += 1
            #for t in self.sample_closure:
            sample_closure_temp = self.sample_closure.copy()
            #for k in range(len(self.sample_closure)):
            for k in range(len(sample_closure_temp)):
                t = sample_closure_temp[k]
                w1 = t[0]
                w2 = t[1]
                b  = t[2]
                if b == 0 or b == 2:
                    if (w2, w1, b) not in self.sample_closure:
                    #if self.sample_closure.index((w2, w1, b)) < 0:
                        print(f"(w2, w1, b) : {(w2, w1, b)}")
                        self.sample_closure.append((w2, w1, b))
                        changed = True
                if b == 0 or b == 1:
                    for w3 in self.words:
                        if (w2, w3, b) in self.sample_closure and (w1, w3, b) not in self.sample_closure:
                            self.sample_closure.append((w1, w3, b))
                            changed = True
                if b == 0:
                    for w3 in self.words:
                        for b2 in [1, 2]:
                            if (w2, w3, b2) in self.sample_closure and (w1, w3, b2) not in self.sample_closure:
                                self.sample_closure.append((w1, w3, b2))
                                changed = True

                if b == 1 or b == 2:
                    for w3 in self.words:
                        if (w2, w3, 0) in self.sample_closure and (w1, w3, b) not in self.sample_closure:
                            self.sample_closure.append((w1, w3, b))
                            changed = True
            #changed = False

        #print(f"sample_closure: {self.sample_closure}")
        print(f"len(sample_closure): {len(self.sample_closure)}")
        return self.sample_closure

    def get_tuples_in_closure(self, w1, w2):
        closure_dict = self.sample_closure_dict
        result = []
        w1_tuple = tuple(w1)
        if w1_tuple in closure_dict.keys():
            for (u1, u2, b) in closure_dict[w1_tuple]:
                if w2 == u2:
                    result.append((u1, u2, b))
        return result

        closure = self.get_closure()
        result = []
        for (u1, u2, b) in closure:
            if w1 == u1 and w2 == u2:
                result.append((u1, u2, b))
        return result


    def save_words_to_file(words, file_name="Garden_mdp.json"):
        f = open(file_name, "w")
        json_str = jsonpickle.encode(words)
        f.write(json_str)
        f.close()

    def load_words_from_file(file_name="Garden_mdp.json"):
        f = open(file_name, "r")
        json_str = f.read()
        words = jsonpickle.decode(json_str)
        f.close()
        return words

    def learn_preferenceDFA(self):
        closure = self.get_closure()
        equiv_relation = set()
        for (w, u, b) in closure:
            if b == 0:
                equiv_relation.add((w, u))
        paritions = self.get_partitions_of_equivRelation(equiv_relation)





    def get_partitions_of_equivRelation(self, equiv_relation):
        partitions = []  # Found partitions
        for w in self.words:
            found = False  # Note it is not yet part of a know partition
            for p in partitions:
                if (w, p[0]) in equiv_relation:  # Found a partition for it!
                    p.append(w)
                    found = True
                    break
            if not found:  # Make a new partition for it.
                partitions.append([w])


        data = []
        for w in self.words:
            B = None
            for b in partitions:
                if w in b:
                    B = b
                    break
            data.append((w, B))

        from aalpy.learning_algs import run_RPNI
        model = run_RPNI(data, automaton_type='moore')
        model.visualize()

        return partitions


    def create_sample(words, prefDFA, sampling_type, tuples_sampled_portion, comparisons_per_item):
        print("Making the preference sample from the words")
        start_time = time.time()
        tuples = []
        for i in range(len(words)):
            for j in range(i):
                w = words[i]
                u = words[j]
                tuples.append((w, u))
        # for w in words:
        #     for u in words:
        #         if w == u:
        #             continue
        #         if (u, w) in tuples:
        #             continue
        #         tuples.append((w, u))
        sampled_tuples = []

        # for w in words:
        #     t_w = tuple(w)
        #     while len(sampled_pairs[t_w]) < number_of_comps_per_word:
        #         u = random.choice(words)
        #         if u == w:
        #             continue
        #         if u in sampled_pairs[t_w]:
        #             continue
        #         if w in sampled_pairs[tuple(u)]:
        #             continue
        #         sampled_pairs[t_w].append(u)
        #         sampled_tuples.append((w, u))
        if sampling_type == 1:
            sampled_tuples = random.sample(tuples, len(tuples)//tuples_sampled_portion)
        elif sampling_type == 2:
            dict = {}
            for w in words:
                w_t = tuple(w)
                dict[w_t] = []
                i = 0
                while i < comparisons_per_item:
                    u = random.choice(words)
                    if u == w:
                        continue
                    u_t = tuple(u)
                    if u_t not in dict.keys() or w not in dict[u_t]:
                        dict[w_t].append(u)
                        sampled_tuples.append((w, u))
                        i += 1
            #sampled_tuples = random.sample(tuples, len(tuples)//tuples_sampled_portion)
        #sampled_tuples = tuples
        sample = []
        for w, u in sampled_tuples:
            b = prefDFA.compare(w, u)
            if b == -1:
                sample.append((u, w, 1))
            else:
                sample.append((w, u, b))

        pref_sample = PreferenceSample(sample)
        print("End making the preference sample from the words")
        elapsed_time = time.time()-start_time
        print(f"Time to make the preference sample from the words: {elapsed_time}")
        return pref_sample
                