import random

import  time


class Sampler():
    def __init__(self):
        self.name = "Sampler"


    def sample_words(self, alphabet, count):
        print(f"Start sampling {count} words")
        start_time = time.time()
        result = []
        actions = []
        for a in alphabet:
            actions.append(a)
        actions.append("STOP")
        i = 0
        while i < count:
            word = []
            stop = False
            while not stop:
                a = random.choice(actions)
                if a != "STOP":
                    word.append(a)
                else:
                    stop = True
            if word not in result:
                result.append(word)
                i += 1
        print(f"End sampling {count} words")
        elapsed_time = time.time() - start_time
        print(f"Time to sample the words: {elapsed_time}")
        return result


