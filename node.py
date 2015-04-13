import math

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of player.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None):
        def WhoJustMoved(state):
            if state.get_whos_turn() == 'red':
                return 'blue'
            else:
                return 'red'
        
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.score = 0.0    # Note that in this case, score represents the sum total of scores for the subtree rooted at this node.
        self.visits = 0.0
        self.possibleMoves = state.get_moves() # future child nodes
        self.currentPlayer = state.get_whos_turn() # the only part of the state that the Node needs later
        
    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.score/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key = lambda c: float(c.score)/c.visits + math.sqrt(2*math.log(self.visits)/c.visits))[-1]
        return s
    
    def AddChild(self, m, s):
        """ Remove m from possibleMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.possibleMoves.remove(m)
        self.childNodes.append(n)
        return n
    
    def Update(self, result):
        """ Update this node - one additional visit and result additional score. result must be from the viewpoint of player.
        """
        self.visits += 1
        self.score += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.score) + "/" + str(self.visits) + " U:" + str(self.possibleMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s