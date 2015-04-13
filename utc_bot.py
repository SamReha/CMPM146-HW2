import time
import random
import node as Node

def think(rootstate, quip):
    # Returns a float representing the difference between the score of me and the other player
    def result(scoreDict, me):
        if me == 'red':
            return float(scoreDict['red'] - scoreDict['blue'])
        else: # me == 'blue'
            return float(scoreDict['blue'] - scoreDict['red'])
    
    """ Conduct a UCT search for at most 1 second starting from rootstate.
        Return the best move from the rootstate.
        Never rolls out beyond the MAX_DEPTH"""
    rootnode = Node.Node(state = rootstate)
    me = rootstate.get_whos_turn()
    rollouts = 0
    startTime = time.clock()

    while time.clock() - startTime <= 1.0:
        node = rootnode
        state = rootstate.copy()

        # Select
        while node.possibleMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.apply_move(node.move)

        # Expand
        if node.possibleMoves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.possibleMoves) 
            state.apply_move(m)
            node = node.AddChild(m,state) # add child and descend tree

        # Rollout
        while state.get_moves() != []: # while state is non-terminal
            state.apply_move(random.choice(state.get_moves()))
            rollouts = rollouts+1

        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            node.Update(result(state.get_score(), me)) # state is terminal. Update node with result from POV of me.
            node = node.parentNode
    bestChild = sorted(rootnode.childNodes, key = lambda c: c.visits)[-1] # Get the child that was most visited
    
    # Output some information about my thought process.
    quip("I think the best move is " + str(bestChild.move) + ' with an expected score: ' + str(bestChild.score))
    quip("In less than 1 second, I preformed " + str(rollouts) + " rollouts.")
    quip(rootnode.ChildrenToString())

    return bestChild.move