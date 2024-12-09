# Given a set of pairwise comparison
samples = [(['b', 'a'], ['a'], 1), (['a'], ['a', 'b', 'b'], 0), (['b', 'a'], ['a', 'b', 'b', 'b'], 0), (['b', 'b'], ['a', 'b', 'b'], 1), (['a', 'b', 'b'], ['a', 'b', 'a'], 0), (['a', 'b', 'b'], ['b', 'b', 'b'], 0), (['b', 'b'], ['a', 'a'], 0), (['a', 'a'], ['a', 'b', 'a', 'a'], 2), (['a', 'a'], ['a', 'a', 'b', 'b'], 0), (['a', 'b', 'a'], ['b', 'a', 'a'], 0), (['a', 'b', 'b', 'b'], ['a', 'b', 'a', 'a'], 0)]
from Learning import PreferenceDFA
from Learning.PreferenceSample import PreferenceSample
from Learning.RPNIMooreBased import RPNIMooreBased
from Learning.Graph import Graph
from Learning.PreferenceDFA import PreferenceDFA
from Learning import UGraph
import Utility.AutomataUtility as AU
# The goal is to learn a preference DFA from the samples

# first, construct the words from samples.
words = []
for sample in samples:
    w, u, b = sample
    words.append(w)
    words.append(u)

# remove duplicates
words = list(set([tuple(w) for w in words]))

# compute the closure of the comparison:
from Learning.PreferenceSample import PreferenceSample
preferenceSample = PreferenceSample(samples)
closure = preferenceSample.get_closure()

pdfa_learned = RPNIMooreBased(preferenceSample) # only providing the sample, but no ground truth.
pdfa_learned.learn_preferenceDFA_By_Eq_graph_parition()