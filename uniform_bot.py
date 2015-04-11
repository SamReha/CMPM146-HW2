import random

def think(state, quip):
    move = random.choice(state.get_moves())
    return move