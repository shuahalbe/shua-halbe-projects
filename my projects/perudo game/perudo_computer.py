import copy
import time
import math

def get_move(num_dice,game,bet,turn,previous_bets):
    state = get_state(num_dice,game,bet,turn,previous_bets)
    best_move = get_best_move(state)
    return best_move

def get_state(num_dice,game,bet,turn,previous_bets):
    num_players = 0
    for i in range(len(game)):
        num_players+=1
    dice_left = 0
    for i in range(len(num_dice)):
        dice_left += num_dice[i]
    state = {
        'my_dice': game[turn-1],
        'current_bet': bet ,
        'turn': turn,
        'my_turn':turn,
        'num_players': num_players,
        'num_dice': dice_left,  
        'previous_bets': previous_bets    
    }
    return state

def get_legal_moves(state):
    moves = []
    number , amount = state['current_bet']
    if len(state['previous_bets']) !=0:
        if number !=1:
            for i in range(1,7):
                if i != 1:
                    moves.append((i,amount+1))
                    moves.append((i,amount+2))
                else:
                    moves.append((i,round((amount/2)+0.5)))
                    moves.append((i,round((amount/2)+1.5)))
        else:
            for i in range(1,7):
                if i!=1:
                    moves.append((i,(amount*2)+1))
                    moves.append((i,(amount*2)+2))
                else:
                    moves.append((i,amount+1))
                    moves.append((i,amount+2))
        moves.append('liar')
    else:
        for i in range(2,7):
            moves.append((i,1))
            moves.append((i,2))
    return moves

def evaluate(state):
    my_dice = state['my_dice']
    num_players = state['num_players']
    total_dice = state['num_dice']
    if state['current_bet'] == 'liar':
        bid_quantity,bid_face = state['previous_bets'][0]
    else:
        bid_quantity, bid_face = state['current_bet']
    my_turn = state['my_turn']
    turn = state['turn']

    bid_risk = probability_of_move(state,number=bid_face,amount=bid_quantity)

    turns_until_me = (my_turn - turn) % num_players  
    bluff_factor = 1 - (0.1 * turns_until_me)  
    adjusted_bid_risk = bid_risk * bluff_factor  

    return adjusted_bid_risk

def probability_of_move(state,number,amount):
    num_in_mine = 0
    for i in range(len(state['my_dice'])):
        if i == number or i== 1:
            num_in_mine +=1
    remaining_opponent_dice = state['num_dice'] - len(state['my_dice'])
    needed_dice = amount - num_in_mine
    if needed_dice< 1: return 1
    elif needed_dice> remaining_opponent_dice: return 0
    return mathy_function(number,needed_dice,remaining_opponent_dice)

def mathy_function(number,needed_dice,remaining_opponent_dice):
    probability = 0.0
    if number !=1:
        for k in range(needed_dice, remaining_opponent_dice + 1):
            combination = math.comb(remaining_opponent_dice, k)
            probability += combination * (1/3)**k * (2/3)**(remaining_opponent_dice - k)
    else:
        for k in range(needed_dice, remaining_opponent_dice + 1):
            combination = math.comb(remaining_opponent_dice, k)
            probability += combination * (1/6)**k * (5/6)**(remaining_opponent_dice - k)
    return probability

def apply_move(state,move):
    state['turn'] = (state['turn'] + 1) % state['num_players']
    if move != 'liar':
        state['previous_bets'].insert(0,move)
    state['current_bet'] = move
    return state


def get_probability(state,move):
    if move == 'liar':
        number ,amount = state['previous_bets'][0]
    else: number,amount = move
    prob = mathy_function(number,needed_dice=amount,remaining_opponent_dice=state['num_dice'])
    return prob

def expectimax(state, depth):
    if depth == 0 or state['current_bet'] == 'liar':
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
            prob = get_probability(state, move)
            total_value += prob * expectimax(new_state, depth - 1)
        return total_value
    
    
def get_best_move(state):
    depth = 4
    best_move = None
    best_value = float('-inf')

    legal_moves = get_legal_moves(state)

    for move in legal_moves:
        new_state = copy.deepcopy(state)
        new_state = apply_move(new_state, move)
        value = expectimax(new_state, depth - 1)
        if value > best_value:
            best_value = value
            best_move = move

    return best_move
