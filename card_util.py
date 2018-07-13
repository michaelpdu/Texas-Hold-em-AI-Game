from __future__ import division
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
    rank = 0
    features = convert_card_to_feature(card1)
    features.update(convert_card_to_feature(card2))

    suit_1 = Card.get_suit_int(card1)
    suit_2 = Card.get_suit_int(card2)
    rank_1 = Card.get_rank_int(card1)
    rank_2 = Card.get_rank_int(card2)

    features[53] = 1 if suit_1 == suit_2 else 0
    features[54] = 1 if rank_1 == rank_2 else 0
    features[55] = rank_1 / 13
    features[56] = rank_2 / 13
    features[57] = abs(rank_1 - rank_2) / 12

    if suit_1 == suit_2: # same suit
        if rank_1 >= 8 and rank_2 >= 8: # pokers >= 10
            rank = 10
        elif (rank_1 >= 8 or rank_2 >= 8) and abs(rank_1 - rank_2) < 5: # |one of poker >= 10| and |gap < 5|
            rank = 9
        elif abs(rank_1 - rank_2) < 5: # gap < 5
            rank = 8
        else:
            rank = 6
    elif rank_1 == rank_2: # same rank
        if rank_1 >= 8:
            rank = 7
        elif rank_1 >= 5:
            rank = 5
        else:
            rank = 3
    else:
        if rank_1 >= 8 and rank_2 >= 8: # pokers >= 10
            rank = 4
        elif (rank_1 >= 8 or rank_2 >= 8) and abs(rank_1 - rank_2) < 5: # |one of poker >= 10| and |gap < 5|
            rank = 2
        elif rank_1 >= 8 or rank_2 >= 8 or abs(rank_1 - rank_2) < 5: # gap < 5
            rank = 1
        else:
            rank = 0

    features[58] = rank / 10
    return rank, features

def convert_card_to_feature(card):
    features = {}
    suit = Card.get_suit_int(card)
    # print(suit)
    rank = Card.get_rank_int(card)
    if suit == 1:
        index = rank
    elif suit == 2:
        index = rank+13
    elif suit == 4:
        index = rank+26
    elif suit == 8:
        index = rank+39
    features[index] = 1
    return features

def get_gap_between_hands_and_board(hands, board):
    evaluator = Evaluator()
    value = evaluator.evaluate(board, hands)
    if len(board) == 5:
        board_value = evaluator.evaluate(board, [])
        gap = abs(value - board_value)
        print("(5 Board Cards) Gap: {}".format(gap))
        return gap
    elif len(board) == 4:
        v1 = evaluator.evaluate(board, [hands[0]])
        v2 = evaluator.evaluate(board, [hands[1]])
        gap1 = abs(value - v1)
        gap2 = abs(value - v2)
        max_gap = max(gap1, gap2)
        print("(4 Board Cards) V1: {}, V2: {}, Gap1: {}, Gap2: {}, Max Gap: {}".format(v1, v2, gap1, gap2, max_gap))
        return max_gap
    else:
        return 0

if __name__ == "__main__":
    card = Card.new("Jc")
    print(convert_card_to_feature(card))
    Card.print_pretty_card(card)

    card = Card.new("Jd")
    print(convert_card_to_feature(card))
    Card.print_pretty_card(card)

    card = Card.new("Js")
    print(convert_card_to_feature(card))
    Card.print_pretty_card(card)

    card = Card.new("Jh")
    print(convert_card_to_feature(card))
    Card.print_pretty_card(card)