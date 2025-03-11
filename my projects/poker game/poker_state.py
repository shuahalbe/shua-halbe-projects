import random
from itertools import combinations
import math
from collections import Counter


'''
1=clubs
2=diamonds
3=hearts
4=spades
'''
def game_state(num_players):
    game = [{} for row in range(num_players)]
    state = [{}]
    game,state = give_card(game,state)
    return game,state

def inital_money(game):
    for i in range(len(game)):
        game[i]['money'] = 1000
    return game

def give_card(game,state):
    cards = [i for i in range(1,53)]
    for i in range(len(game)):
        num = random.choice(cards)
        cards.remove(num)
        num_2 = random.choice(cards)
        cards.remove(num_2)
        game[i]['cards'] = (num,num_2)
    board = []
    for i in range(5):
        num = random.choice(cards)
        board.append(num)
        cards.remove(num)
    state[0]['board'] = board
    return game,state


def legal(choice,old_bet):
    if choice == 'check' and old_bet ==0:
        return True
    elif int(choice)>= old_bet and int(choice)%25 == 0:
        return True
    


'''
1=clubs
2=diamonds
3=hearts
4=spades

2 = two
14 = ace
''' 
def winner(game,folded_players,state):
    player_hands = []
    for i in range(len(game)):
        if i+1 not in folded_players:
            cards = state[0]['board'] + list(game[i]['cards'])
            player_hands.append(cards)
    return get_combos(player_hands)


def get_combos(player_hands):
    best_player_hands = []
    for hand in player_hands:
        best_hand_strength = 0
        best_hand_order = [0,0,0,0,0]
        five_card_combos = list(combinations(hand, 5))
        for hand in five_card_combos:
            strength,order = rankings(hand)
            if best_hand_strength<strength:
                best_hand_strength = strength
                best_hand_order = order
            elif best_hand_strength == strength:
                for i in range(5):
                    if best_hand_order[i] > order[i]:
                        break
                    elif order[i]> best_hand_order[i]:
                        best_hand_strength = strength
                        best_hand_order = order
                        break
        best_player_hands.append((best_hand_strength,best_hand_order))
    best_hand_strength_overall = 0
    best_hand_order_overall = [0,0,0,0,0]
    for strength,order in best_player_hands:
        if best_hand_strength_overall<strength:
            best_hand_strength_overall = strength
            best_hand_order_overall = order
        elif best_hand_strength_overall == strength:
            for i in range(5):
                if best_hand_order_overall[i] > order[i]:
                    break
                elif order[i]> best_hand_order_overall[i]:
                    best_hand_strength_overall = strength
                    best_hand_order_overall = order
                    break
    return best_player_hands.index((best_hand_strength_overall,best_hand_order_overall))+1

def check_suit(num):
    if num%4 == 0: return 'spades'
    elif (num+1)%4 == 0: return 'hearts'
    elif (num+2)%4 == 0: return 'diamonds'
    elif (num+3)%4 == 0: return 'clubs'

def check_number(num):
    num = math.ceil(num/4)
    if num == 1: num =14
    return num

def rankings(hand):
    sorted_hand = sorted(hand, reverse=True)
    numbers = []
    suits = []
    for num in sorted_hand:
        numbers.append(check_number(num))
        suits.append(check_suit(num))
    #straight flush 9 
    if in_a_row(numbers) and same_suit(suits): return 9,sorted_hand
    #4 of a kind 8
    elif quads(numbers): 
        new_order = order_strength(numbers)
        return 8,new_order
    #full house 7
    elif trips(numbers) and pair(numbers): 
        new_order = order_strength(numbers)
        return 7,new_order
    #flush 6
    elif same_suit(suits): return 6,sorted_hand
    #straight 5
    elif in_a_row(numbers): return 5,sorted_hand
    #trips 4
    elif trips(numbers):
        new_order = order_strength(numbers)  
        return 4,new_order
    #2 pair 3
    elif two_pair(numbers): 
        new_order = order_strength(numbers)       
        return 3,new_order
    #pair 2
    elif pair(numbers): 
        new_order = order_strength(numbers)
        return 2,new_order
    #high card 1
    else: return 1,sorted_hand
def order_strength(numbers):
    most_common = find_most_common(numbers)
    new_order = []
    for i in most_common:
        number,count = i
        for i in range(count):
            new_order.append(number)
    return new_order

def in_a_row(numbers):
    if all(numbers[i] == numbers[i+1]+1 for i in range(4)): return True
    elif (all(numbers[i+1] == numbers[i+2]+1 for i in range(3)) and numbers[0] == 14 and numbers[4]==2): return True
def same_suit(suits):
    if all(suits[i] == suits[i+1] for i in range(4)): return True
def find_most_common(numbers):
    count = Counter(numbers)
    most_common = count.most_common()
    return most_common
def quads(numbers):
    most_common = find_most_common(numbers)
    for i in most_common:
        number,count = i
        if count == 4: return True
def trips(numbers):
    most_common = find_most_common(numbers)
    for i in most_common:
        number,count = i
        if count == 3: return True
def two_pair(numbers):
    most_common = find_most_common(numbers)
    num_pairs = 0
    for i in most_common:
        number,count = i
        if count ==2:num_pairs +=1
    if num_pairs == 2: return True
def pair(numbers):
    most_common = find_most_common(numbers)
    num_pairs = 0
    for i in most_common:
        number ,count = i
        if count == 2: num_pairs+=1
    if num_pairs == 1: return True
    

    





    
