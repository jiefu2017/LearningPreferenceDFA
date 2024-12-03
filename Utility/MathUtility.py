import random
from collections import defaultdict

from itertools import chain, combinations


def powerset_of_set(input_set):
    s = list(input_set)
    ite = chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))
    result = []
    for i in ite:
        result.append(set(i))
    return result


def equivalence_partition(iterable, relation):
    classes = defaultdict(set)
    for element in iterable:
        for sample, known in classes.items():
            if (sample, element) in relation:
                known.add(element)
                break
        else:
            classes[element].add(element)
    return list(classes.values())

def equivalence_partition_as_list_of_list(iterable, relation):
    classes = equivalence_partition(iterable, relation)
    newClasses = []
    for c in classes:
        newClasses.append(list(c))
    return newClasses


def get_random_weight_vector(dimensions=4):
    upper_bound = 1
    result = []
    indices = set()
    for j in range(dimensions):
        result.append(0)
        indices.add(j)
    i = 1
    while i < dimensions:
        val = random.uniform(0, upper_bound)
        index = random.choice(list(indices))
        indices = indices.difference({index})
        result[index] = val
        upper_bound -= val
        i += 1
    indices_list = list(indices)
    result[indices_list[0]] = upper_bound
    return result

def get_random_weight_vector_using_uniform(dimensions=4):
    upper_bound = 1
    result = []
    indices = set()
    j = 0
    total = 0
    for j in range(dimensions):
        val = random.uniform(0, upper_bound)
        total += val
        result.append(val)
    sum = 0
    for j in range(dimensions-1):
        sum += result[j]/total
        result[j] = result[j]/total
    result[dimensions-1] = 1-sum
    return result

