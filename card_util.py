from deuces import Card, Evaluator

def convert_to_deuces_card(card_string):
    deuces_card = card_string[0]
    deuces_card += card_string[1].lower()
    return deuces_card

def create_deuces_card(card):
    return Card.new(convert_to_deuces_card(card))

def print_deuces_card(cards):
    Card.print_pretty_cards(cards)

def get_rank_of_hand_cards(card1, card2):
    suit_1 = Card.get_suit_int(card1)
    suit_2 = Card.get_suit_int(card2)
    rank_1 = Card.get_rank_int(card1)
    rank_2 = Card.get_rank_int(card2)
    if suit_1 == suit_2: # same suit
        if rank_1 >= 8 and rank_2 >= 8: # pokers >= 10
            return 10
        elif (rank_1 >= 8 or rank_2 >= 8) and abs(rank_1 - rank_2) < 5: # |one of poker >= 10| and |gap < 5|
            return 9
        elif abs(rank_1 - rank_2) < 5: # gap < 5
            return 8
        else:
            return 6
    elif rank_1 == rank_2: # same rank
        if rank_1 >= 8:
            return 7
        elif rank_1 >= 5:
            return 5
        else:
            return 3
    else:
        if rank_1 >= 8 and rank_2 >= 8: # pokers >= 10
            return 4
        elif (rank_1 >= 8 or rank_2 >= 8) and abs(rank_1 - rank_2) < 5: # |one of poker >= 10| and |gap < 5|
            return 2
        elif (rank_1 >= 8 or rank_2 >= 8) or abs(rank_1 - rank_2) < 5: # gap < 5
            return 1
        else:
            return 0

