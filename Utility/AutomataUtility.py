from automata.fa.dfa import DFA
from automata.fa.nfa import NFA

"""
Create the powerset of a given set of alphabet
"""
from builtins import str
from automata.fa import dfa


# from _ast import Str
def createPowerSet(alphabet):
    sets = [set([])]

    for n in alphabet:
        sets.extend([s | {n} for s in sets])

    # sets[0] = set()

    return sets


def are_DFAs_equal(dfa1, dfa2):
    equal_to_state_dict = dict()
    queue = []
    queue.append((dfa1.initial_state, dfa2.initial_state))
    visited = []
    equal_to_state_dict[dfa1.initial_state] = dfa2.initial_state
    equal_to_state_dict[dfa2.initial_state] = dfa1.initial_state
    while queue:
        t = queue.pop(0)
        q, q2 = t
        visited.append(t)
        for a in dfa1.input_symbols:
            q_next = dfa1.transitions[q][a]
            q2_next = dfa2.transitions[q2][a]
            if q_next not in equal_to_state_dict.keys():
                equal_to_state_dict[q_next] = q2_next
            elif equal_to_state_dict[q_next] != q2_next:
                print(f"States {q_next} and {q2_next} are not equal")
                return False
            if q2_next not in equal_to_state_dict.keys():
                equal_to_state_dict[q2_next] = q_next
            elif equal_to_state_dict[q2_next] != q_next:
                print(f"States {q_next} and {q2_next} are not equal")
                return False
            t2 = (q_next, q2_next)
            if t2 not in visited:
                queue.append(t2)

        t = (q, q2)
        if t not in visited:
            visited.append(t)
    return True


"""
Create the dfa that accepts over a given alphabet, the language that consists of all strings 
that contain all letters of the alphabet
"""


def dfaToSeeAllLetters(alphabet, additionalLetters, changeStateNames):
    pwset = createPowerSet(alphabet)

    sets = []
    states = []

    index = 0

    for st in pwset:
        sets.append(st)
        s = str(st)
        if changeStateNames == True:
            s = "q" + str(index)
        states.append(s)
        index += 1
        # print(s)

    initial_state = states[0]
    final_states = set()
    final_states.add(states[len(states) - 1])

    transitions = {}

    for i in range(len(states)):
        s = states[i]
        st1 = sets[i]
        transitions[s] = {}
        for a in alphabet:
            newSt = st1.copy()
            # print(type(newSt))
            if not (a in newSt):
                newSt.add(a)
            i = sets.index(newSt)
            transitions[s][a] = states[i]
        for b in additionalLetters:
            transitions[s][b] = s

    for c in additionalLetters:
        alphabet.add(c)

    dfa = DFA(states=set(states), input_symbols=alphabet, transitions=transitions, initial_state=initial_state,
              final_states=final_states)

    return dfa


"""
Creates a DFA whose language is the set of all words containing each letter of alphabet once.
"""


def dfaToSeeAllLettersEachOnce(alphabet, additionalLetters, changeStateNames):
    pwset = createPowerSet(alphabet)

    sets = []
    states = []

    index = 0

    for st in pwset:
        sets.append(st)
        s = str(st)
        if changeStateNames == True:
            s = "q" + str(index)
        states.append(s)
        index += 1
        # print(s)

    initial_state = states[0]
    final_states = set()
    final_states.add(states[len(states) - 1])

    transitions = {}

    trp = "trp"
    transitions[trp] = {}

    for i in range(len(states)):
        s = states[i]
        st1 = sets[i]
        transitions[s] = {}
        for a in alphabet:
            if a in st1:
                transitions[s][a] = trp
                continue
            newSt = st1.copy()
            # print(type(newSt))
            if not (a in newSt):
                newSt.add(a)
            i = sets.index(newSt)
            transitions[s][a] = states[i]
        for b in additionalLetters:
            transitions[s][b] = s

    trp = "trp"
    transitions[trp] = {}

    for a in alphabet:
        transitions[trp][a] = trp
    for a in additionalLetters:
        transitions[trp][a] = trp

    states.append(trp)

    for c in additionalLetters:
        alphabet.add(c)

    dfa = DFA(states=set(states), input_symbols=alphabet, transitions=transitions, initial_state=initial_state,
              final_states=final_states)

    return dfa


def dfaAcceptingASequence(sequence, alphabet):
    states = []

    transitions = {}
    currState = "q0"
    prevState = currState
    states.append(currState)

    q_trap = "q_trap"
    states.append(q_trap)

    i = 1

    for a in sequence:
        currState = "q_" + a + "_" + str(i)
        states.append(currState)
        transitions[prevState] = {}
        transitions[prevState][a] = currState
        for b in alphabet:
            if b != a:
                transitions[prevState][b] = q_trap
        prevState = currState
        i = i + 1

    q_final = prevState
    transitions[q_trap] = {}
    transitions[q_final] = {}

    for a in alphabet:
        transitions[q_trap][a] = q_trap
        transitions[q_final][a] = q_trap

    initial_state = states[0]
    final_states = set()
    final_states.add(q_final)

    dfa = DFA(states=set(states), input_symbols=alphabet, transitions=transitions, initial_state=initial_state,
              final_states=final_states)

    return dfa


"""
def dfaAcceptingASeq1PlusSeq2(seq1,  seq2, alphabet):

    states = []

    transitions = {}
    currState = "q0"
    prevState = currState
    states.append(currState)

    q_trap = "q_trap"
    states.append(q_trap)

    i = 1

    for a in seq1:
        currState = "q_"+a+"_"+str(i)+"_1"
        states.append(currState)
        transitions[prevState] = {}
        transitions[prevState][a] = currState
        for b in alphabet:
            if b != a:
                transitions[prevState][b] = q_trap
        prevState = currState
        i = i + 1

    q_final1 = prevState
    transitions[q_trap] = {}
    transitions[q_final1] = {}

    for a in alphabet:
        transitions[q_trap][a] = q_trap
        if a != seq1[1]:        
            transitions[q_final1][a] = "q0"
        else:
            transitions[q_final1][a] = "q0"



    initial_state = states[0]
    final_states = set()
    final_states.add(q_final)

    dfa = DFA(states=set(states), input_symbols=alphabet, transitions=transitions, initial_state=initial_state, final_states=final_states)

    return dfa
"""


def dfaToSeeAllLettersInOrder(orderedAlphabet, additionalLetters, changeStateNames):
    states = []

    index = 0

    transitions = {}
    currState = "q0"
    prevState = currState
    states.append(currState)

    for a in orderedAlphabet:
        currState = "q_" + a
        states.append(currState)
        transitions[prevState] = {}
        transitions[prevState][a] = currState
        prevState = currState

    q_final = prevState
    currState = "q_trap"
    q_trap = currState
    transitions[q_trap] = {}
    states.append(currState)
    transitions[prevState] = {}
    transitions[prevState][a] = currState

    initial_state = states[0]
    final_states = set()
    final_states.add(q_final)

    for i in range(len(states) - 1):
        for k in range(i):
            transitions[states[i]][orderedAlphabet[k]] = states[i]
        for j in range(i + 1, len(orderedAlphabet)):
            transitions[states[i]][orderedAlphabet[j]] = q_trap

    for a in orderedAlphabet:
        transitions[q_trap][a] = q_trap

    for c in additionalLetters:
        orderedAlphabet.append(c)
        for i in range(len(states)):
            transitions[states[i]][c] = states[i]

    dfa = DFA(states=set(states), input_symbols=orderedAlphabet, transitions=transitions, initial_state=initial_state,
              final_states=final_states)

    return dfa


def nfaToSeeAllLettersInOrder(orderedAlphabet, additionalLetters, changeStateNames):
    states = []

    index = 0

    transitions = {}
    currState = "q0"
    prevState = currState
    states.append(currState)

    for a in orderedAlphabet:
        currState = "q_" + a
        states.append(currState)
        transitions[prevState] = {}
        transitions[prevState][a] = {prevState, currState}
        for b in orderedAlphabet:
            if b != a:
                transitions[prevState][b] = {prevState}
        for c in additionalLetters:
            transitions[prevState][c] = {prevState}
        prevState = currState

    q_final = prevState
    transitions[prevState] = {}
    for b in orderedAlphabet:
        transitions[prevState][b] = {prevState}
    for c in additionalLetters:
        transitions[prevState][c] = {prevState}

    initial_state = states[0]
    final_states = set()
    final_states.add(q_final)

    for c in additionalLetters:
        orderedAlphabet.append(c)

    nfa = NFA(states=set(states), input_symbols=orderedAlphabet, transitions=transitions, initial_state=initial_state,
              final_states=final_states)

    return nfa


def levenshtein_automaton_for_a_term(term, k, alphabet):
    n = len(term)

    states = []
    transitions = {}
    final_states = set()
    for i in range(n + 1):
        for j in range(k + 1):
            s = str(i) + "_" + str(j)
            states.append(s)
            transitions[s] = {}
            for a in alphabet:
                transitions[s][a] = set()
                transitions[s][''] = set()

            """ Add the transition for getting the next character of the term"""
            if i < n:
                transitions[s][term[i]].add(str(i + 1) + "_" + str(j))
                # print("t for next of ("+s+", "+term[i]+")="+str(transitions[s][term[i]]))

            """ Add the transitions for inserting a character """
            if j < k:
                for a in alphabet:
                    transitions[s][a].add(str(i) + "_" + str(j + 1))
                    # print("t for next of ("+s+", "+a+")="+str(i)+"_"+str(j+1))

            """ Add the transitions for getting a wrong character """
            if i < n and j < k:
                for a in alphabet:
                    transitions[s][a].add(str(i + 1) + "_" + str(j + 1))
                    # print("t for next of ("+s+", "+a+")="+str(i+1)+"_"+str(j+1))

            """ Add the transitions for skipping a character """
            if i < n and j < k:
                for a in alphabet:
                    transitions[s][''].add(str(i + 1) + "_" + str(j + 1))
                    # print("t for next of ("+s+", '')="+str(i+1)+"_"+str(j+1))

            if i == n:
                final_states.add(str(i) + "_" + str(j))

    initial_state = states[0]

    nfa = NFA(states=set(states), input_symbols=alphabet, transitions=transitions, initial_state=initial_state,
              final_states=final_states)
    dfa = DFA.from_nfa(nfa)
    return dfa


def levenshtein_automaton_for_a_dfa(dfa, k, alphabet):
    n = len(dfa.states)

    S = []
    for s in dfa.states:
        S.append(s)

    states = []
    transitions = {}
    final_states = set()
    for i in range(n):
        for j in range(k + 1):
            s = S[i] + "_" + str(j)
            states.append(s)
            transitions[s] = {}
            for a in alphabet:
                transitions[s][a] = set()
                transitions[s][''] = set()

            """ Add the transitions of the same level """
            for a in alphabet:
                transitions[s][a].add(dfa.transitions[S[i]][a] + "_" + str(j))
                # print("("+s+", "+a+")="+dfa.transitions[S[i]][a])

            """ Add the transitions for inserting a character """
            if j < k:
                for a in alphabet:
                    transitions[s][a].add(S[i] + "_" + str(j + 1))
                    # print("("+s+", "+a+")="+S[i]+"_"+str(j+1))

            """ Add the transitions for getting a wrong character """
            if j < k:
                for a in alphabet:
                    for b in alphabet:
                        transitions[s][b].add(dfa.transitions[S[i]][a] + "_" + str(j + 1))
                        # print("("+s+", "+b+")="+dfa.transitions[S[i]][a]+"_"+str(j+1))

            """ Add the transitions for skipping a character """
            if j < k:
                for a in alphabet:
                    transitions[s][''].add(dfa.transitions[S[i]][a] + "_" + str(j + 1))
                    # print("("+s+", '')="+dfa.transitions[S[i]][a]+"_"+str(j+1))

    initial_state = dfa.initial_state + "_0"
    for s in dfa.final_states:
        for j in range(k + 1):
            final_states.add(s + "_" + str(j))

    nfa = NFA(states=set(states), input_symbols=alphabet, transitions=transitions, initial_state=initial_state,
              final_states=final_states)
    dfa = DFA.from_nfa(nfa)

    return nfa


def union(dfa1, dfa2):
    states = []
    s0 = "q0"
    states.append(s0)
    for s in dfa1.states:
        states.append(s + "_1")
    for s in dfa2.states:
        states.append(s + "_2")
    alphabet = dfa1.input_symbols
    transitions = {}
    for s in dfa1.states:
        transitions[s + "_1"] = {}
        for a in alphabet:
            transitions[s + "_1"][a] = set()
            transitions[s + "_1"][a].add(dfa1.transitions[s][a] + "_1")
    for s in dfa2.states:
        transitions[s + "_2"] = {}
        for a in alphabet:
            transitions[s + "_2"][a] = set()
            transitions[s + "_2"][a].add(dfa2.transitions[s][a] + "_2")
    transitions[s0] = {}
    transitions[s0][''] = set()
    transitions[s0][''].add(dfa1.initial_state + "_1")
    transitions[s0][''].add(dfa2.initial_state + "_2")

    final_states = set()
    for s in dfa1.final_states:
        final_states.add(s + "_1")
    for s in dfa2.final_states:
        final_states.add(s + "_2")

    nfa = NFA(states=set(states), input_symbols=alphabet, transitions=transitions, initial_state=s0,
              final_states=final_states)
    dfa = DFA.from_nfa(nfa)
    return dfa


def intersection(dfa1, dfa2):
    states = []
    transitions = {}
    alphabet = dfa1.input_symbols
    for q1 in dfa1.states:
        for q2 in dfa2.states:
            s = q1 + "_" + q2
            states.append(s)
            transitions[s] = {}
            for a in alphabet:
                transitions[s][a] = dfa1.transitions[q1][a] + "_" + dfa2.transitions[q2][a]
    initial_state = dfa1.initial_state + "_" + dfa2.initial_state
    final_states = set()
    for q1 in dfa1.final_states:
        for q2 in dfa2.final_states:
            final_states.add(q1 + "_" + q2)
    dfa = DFA(states=set(states), input_symbols=alphabet, transitions=transitions, initial_state=initial_state,
              final_states=final_states)
    return dfa


def superSequence(dfa):
    states = dfa.states.copy()
    input_symbols = dfa.input_symbols.copy()
    transitions = dfa.transitions
    initial_state = dfa.initial_state
    final_states = dfa.final_states.copy()
    nfa_transitions = {}
    for q in states:
        nfa_transitions[q] = {}
        for a in input_symbols:
            nfa_transitions[q][a] = {transitions[q][a], q}

    nfa = NFA(states=set(states), input_symbols=input_symbols, transitions=nfa_transitions, initial_state=initial_state,
              final_states=final_states)

    superSeqDFA = DFA.from_nfa(nfa)

    return superSeqDFA


def closurePlus(dfa):
    states = dfa.states.copy()
    input_symbols = dfa.input_symbols.copy()
    transitions = dfa.transitions
    initial_state = dfa.initial_state
    final_states = dfa.final_states.copy()
    nfa_transitions = {}
    for q in states:
        nfa_transitions[q] = {}
        for a in input_symbols:
            nfa_transitions[q][a] = {transitions[q][a]}
        if q in final_states:
            nfa_transitions[q][''] = {initial_state}

    nfa = NFA(states=set(states), input_symbols=input_symbols, transitions=nfa_transitions, initial_state=initial_state,
              final_states=final_states)

    superSeqDFA = DFA.from_nfa(nfa)

    return superSeqDFA


def concatenate(dfa1, dfa2):
    states = dfa1.states.copy()
    input_symbols = dfa1.input_symbols.copy()
    transitions = dfa1.transitions
    initial_state = dfa1.initial_state

    transitions2 = dfa2.transitions.copy()

    initial_state2 = dfa1.initial_state

    final_states = dfa1.final_states.copy()
    nfa_transitions = {}
    for q in states:
        nfa_transitions[q] = {}
        for a in input_symbols:
            nfa_transitions[q][a] = {transitions[q][a]}
        if q in final_states:
            nfa_transitions[q][''] = {initial_state2}

    newStates = []
    dictNewStates = {}

    for q in dfa2.states:
        s = q
        while s in states:
            s = s + "_2"
        newStates.append((s, q))
        dictNewStates[q] = s
        states.add(s)

    for t in newStates:
        s = t[0]
        q = t[1]
        nfa_transitions[s] = {}
        for a in input_symbols:
            nfa_transitions[s][a] = {dictNewStates[transitions2[q][a]]}

    for q in states:
        if q in final_states:
            nfa_transitions[q][''] = {dictNewStates[dfa2.initial_state]}

    final_states2 = set()
    for q in dfa2.final_states:
        final_states2.add(dictNewStates[q])

    nfa = NFA(states=set(states), input_symbols=input_symbols, transitions=nfa_transitions, initial_state=initial_state,
              final_states=final_states2)

    superSeqDFA = DFA.from_nfa(nfa)

    return superSeqDFA


def newStateNames(dfa):
    states = dfa.states.copy()
    input_symbols = dfa.input_symbols.copy()
    transitions = dfa.transitions

    newStates = set()

    pairs = []
    dictOldNew = {}
    i = 0
    for q in dfa.states:
        s = str(i)
        pairs.append((s, q))
        dictOldNew[q] = s
        newStates.add(s)
        i = i + 1

    newTransitios = {}
    for q in dfa.states:
        newTransitios[dictOldNew[q]] = {}
        for a in input_symbols:
            newTransitios[dictOldNew[q]][a] = dictOldNew[transitions[q][a]]

    final_states = set()

    for q in dfa.final_states:
        if q in dictOldNew.keys():
            final_states.add(dictOldNew[q])
        else:
            print("Key " + q + " was not found in the dictionary 'dictOldNew'")

    initial_state = dictOldNew[dfa.initial_state]

    dfa = DFA(states=set(newStates), input_symbols=input_symbols, transitions=newTransitios,
              initial_state=initial_state, final_states=final_states)

    return dfa


def makeFinalStatesAbsorbing(dfa):
    for q in dfa.final_states:
        for a in dfa.input_symbols:
            dfa.transitions[q][a] = q


def printDFA(dfa):
    print("------------------------------------- print DFA ------------------------------------------------")
    print("Initial State: " + dfa.initial_state)
    print("States and Transitions:")
    for t in dfa.transitions.items():
        print(t)
    print("Final States:")
    for f in dfa.final_states:
        print(f)
    print("-------------------------------------------------------------------------------------------------")


def printNFA(nfa):
    print("------------------------------------- print DFA ------------------------------------------------")
    print("Initial State: " + nfa.initial_state)
    print("States and Transitions:")
    for t in nfa.transitions.items():
        print(t)
    print("Final States:")
    for f in nfa.final_states:
        print(f)
    print("-------------------------------------------------------------------------------------------------")


def getNonSelfLoopLetters(dfa, state):
    result = []
    for a in dfa.input_symbols:
        if dfa.transitions[state][a] != state:
            result.append(a)
    return result

