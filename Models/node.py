class Node:
    def __init__(self, state, parent=None, action=None, weight=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight
