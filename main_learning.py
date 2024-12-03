from Learning_CaseStudies.BeeRobot import BeeRobot
from Learning_CaseStudies.RunningExample import RunningExample
from Learning import *
import time


RunningExample = RunningExample()
RunningExample.learn_prefDFA_mooreBaseAlg()

# vertices = [1, 2, 3, 4, 5, 6]
# edges = [(1, 2), (2, 1), (2, 3), (4, 5), (5, 4)]
# uGraph = UGraph(vertices, edges)
# uGraph.compute_SCCs()
# print(f"SCCs: {uGraph.SCCs}")
# exit()

#start_time = time.time()
# your code

#runningExample = RunningExample()

beeRobot = BeeRobot()
beeRobot.random_words_experiment()
beeRobot.single_experiment()

#elapsed_time = time.time() - start_time

#rint(f"execution time: {elapsed_time}")

# data = [(('a', 'a', 'a'), True),
#             (('a', 'a', 'b', 'a'), True),
#             (('b', 'b', 'a'), True),
#             (('b', 'b', 'a', 'b', 'a'), True),
#             (('a',), False),
#             (('b', 'b'), False),
#             (('a', 'a', 'b'), False),
#             (('a', 'b', 'a'), False)]
#
# from aalpy.learning_algs import run_RPNI
# model = run_RPNI(data, automaton_type='dfa')
# model.visualize()
