def getLetters(alphabet, cnf_formula):
    result = alphabet
    if cnf_formula == "true":
        return result
    conditions = cnf_formula.split('&')
    for c in conditions:
        c = c.replace('(', '').replace(')', '')
        props = c.split('|')
        temp = []
        for prop in props:
            prop = prop.strip()
            mustContaint = True
            if prop.startswith("~") or prop.startswith("!"):
                mustContaint = False
                prop = prop[1:]
            for a in result:
                contains = False
                for i in range(len(a)):
                    if a[i] == prop:
                        contains = True
                        break
                if contains == mustContaint:
                    if a not in temp:
                        temp.append(a)
        result = temp
    return result


def get_trapping_state(transitions, alphabet, states):
    print(f"alphabet: {alphabet}")
    for s in states:
        is_trapping = True
        if s not in transitions.keys():
            print("here")
            return s
        print(f"transitions[{s}]: {transitions[s]}")
        print(f"transitions[{s}].keys(): {transitions[s].keys()}")
        for a in alphabet:
            if tuple(a) not in transitions[s].keys():
                print(f"{a} not in transitions[{s}]")
                continue
            if transitions[s][a] != s:
                print(f"transitions[{s}][{a}]: {transitions[s][a]}")
                is_trapping = False
        if is_trapping:
            print("there")
            return s
    return None


def addMissingTransitions(transitions, alphabet, states, q_trap):
    for q in states:
        for a in alphabet:
            if a not in transitions[q].keys():
                transitions[q][a] = q_trap
    return transitions


def isComplete(transitions, alphabet, states):
    for q in states:
        for a in alphabet:
            if a not in transitions[q]:
                return False
    return True


def test_getLetters():
    alphabet = [tuple(), tuple('a'), tuple('b'), tuple(('a', 'b'))]
    cnf_formula = 'a|b'
    letters = getLetters(alphabet, cnf_formula)
    print(letters)


def createTreeAutomata(alphabet, height, doSelfLoopOnEmptySet=False, onlyASingleStateAtLastLevel=False):
    states = []
    transitions = {}
    queue = []
    queueHeights = []
    queue.append("q0")
    queueHeights.append(1)
    states.append("q0")
    emptySetLetter = None
    for a in alphabet:
        if set(a) == set():
            emptySetLetter = a

    singleLastLevelState = "end"

    while queue:
        q = queue.pop(0)
        h = queueHeights.pop(0)
        h += 1
        transitions[q] = {}
        for a in alphabet:
            if doSelfLoopOnEmptySet and a == emptySetLetter:
                transitions[q][a] = q
                continue
            aStr = ""
            for i in range(len(a)):
                aStr += a[i]
            q2 = q + "_" + aStr
            transitions[q][a] = q2
            states.append(q2)
            transitions[q2] = {}
            if h < height and not onlyASingleStateAtLastLevel:
                queue.append(q2)
                queueHeights.append(h)
            elif h < height - 1 and onlyASingleStateAtLastLevel:
                queue.append(q2)
                queueHeights.append(h)
            elif h == height - 1 and onlyASingleStateAtLastLevel:
                transitions[q2] = {}
                for c in alphabet:
                    transitions[q2][c] = singleLastLevelState
            elif h == height:
                for b in alphabet:
                    transitions[q2][b] = q2

    if onlyASingleStateAtLastLevel:
        states.append(singleLastLevelState)
        transitions[singleLastLevelState] = {}
        for a in alphabet:
            transitions[singleLastLevelState][a] = singleLastLevelState

    return (states, transitions)







