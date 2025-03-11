import random
import copy

def starting_state(pot,game,turn,state,round,bet,folded_players):
    board_cards = state[0]['board']
    money = game[turn-1]['money']
    cards = game[turn-1]['cards']
    if round == 0: amount = 0
    elif round == 1: amount = 3
    elif round ==2: amount =4
    elif round ==3: amount = 5
    revealed = []
    for i in range(amount):
        revealed.append(board_cards[i])
    current_state = {
        'my_money': money,
        'my_cards': cards,
        'revealed_cards': revealed,
        'num_players':len(game)-len(folded_players),
        'turn':turn,
        'my_turn':turn,
        'pot':pot,
        'current_bet':bet,
        'fold': False,
        'currently_placed':game[turn-1]['already_placed']
    }
    best_move = get_best_move(current_state)
    return best_move
def get_legal_moves(state):
    legal = []
    legal.extend(('call','fold','raise'))
    return legal

def expectimax(state, depth):
    """Runs Expectimax search for Poker AI."""
    if depth == 0 or state['fold']:
        return evaluate(state)

    legal_moves = get_legal_moves(state)

    if state['my_turn'] == state['turn']:
        best_value = float('-inf')
        for move in legal_moves:
            new_state = copy.deepcopy(state)
            new_state = apply_move(new_state, move)
            value = expectimax(new_state, depth - 1)
            best_value = max(best_value, value)
        return best_value
    else:
        total_value = 0
        for move in legal_moves:
            new_state = copy.deepcopy(state)
            new_state = apply_move(new_state, move)
            prob = get_opponent_move_prob(new_state, move)
            total_value += prob * expectimax(new_state, depth - 1)
        return total_value

def get_best_move(state):
    """Selects the best move for AI."""
    depth = 3
    legal_moves = get_legal_moves(state)
    best_move = None
    best_value = float('-inf')

    for move in legal_moves:
        new_state = copy.deepcopy(state)
        new_state = apply_move(new_state, move)
        value = expectimax(new_state, depth - 1)
        if value > best_value:
            best_value = value
            best_move = move

    return best_move

def apply_move(state,move):
    if move == 'fold': 
        state['fold'] = True
    elif move == 'call':
        state['my_money'] = state['my_money'] -(state['current_bet']-state['currently_placed'])
        state['currently_placed'] = state['current_bet']
    elif move == 'raise':
        state['current_bet']+50
        state['my_money'] = state['my_money'] -(state['current_bet']-state['currently_placed'])
        state['currently_placed'] = state['current_bet']
    if state['turn']<state['num_players']: state['turn'] +=1
    else: state['turn'] =1
    return state

def get_opponent_move_prob(state, move):
    """Estimates the probability of an opponent making a move."""
    if move == "fold":
        return 0.2  # Example probability
    elif move == "call":
        return 0.5
    elif move == "raise":
        return 0.3
    
def evaluate(state):
    return random.randint(1,10)



    
    