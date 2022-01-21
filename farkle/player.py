class Player(object):

    def __init__(self, is_ai: bool, score=0, name="Player", done=False):
        self.is_ai = is_ai
        self.score = score
        self.name = name
        self.done = done

    def __repr__(self):
        return self.name + " has " + str(self.score) + " scores" + "\n"
