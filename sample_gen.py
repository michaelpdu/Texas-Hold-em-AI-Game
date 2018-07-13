import sys
import copy
from deuces import Deck, Evaluator
from card_util import *
from feature_util import *


def get_winner(board, hands):
    for hand in hands:
        assert len(hand) == 2, "Inavlid hand length"

    best_rank = 7463  # rank one worse than worst hand
    winners = []
    evaluator = Evaluator()
    for player, hand in enumerate(hands):
        # evaluate current board position
        rank = evaluator.evaluate(hand, board)
        percentage = 1.0 - evaluator.get_five_card_rank_percentage(rank)  # higher better here
        # print "Player %d, percentage rank among all hands = %f" % (player + 1, percentage)

        # detect winner
        if rank == best_rank:
            winners.append(player+1)
            best_rank = rank
        elif rank < best_rank:
            winners = [player+1]
            best_rank = rank
    return winners

def main():
    count = int(sys.argv[1])
    name = sys.argv[2]
    verbose = True

    samples_for_hand = open('{}_hand.txt'.format(name), 'w')
    samples_for_board3 = open('{}_board3.txt'.format(name), 'w')
    samples_for_board4 = open('{}_board4.txt'.format(name), 'w')
    samples_for_board5 = open('{}_board5.txt'.format(name), 'w')

    index = 0
    while index < count:
        #
        player_number = 5
        hands = []
        hands_features = []
        board3_features = []
        board4_features = []
        board5_features = []

        deck = Deck()
        for i in range(0, player_number):
            hands.append(deck.draw(2))
            if verbose:
                print("Player {}:".format(i+1))
                print_deuces_card(hands[i])
            # pf0 = convert_card_to_feature(hands[i][0])
            # pf1 = convert_card_to_feature(hands[i][1])

            rank, features = get_rank_of_hand_cards(hands[i][0], hands[i][1])
            print(features)
            hands_features.append(features)

        board = deck.draw(3)
        if verbose:
            print("Board 3 (FLOP):")
            print_deuces_card(board)
        bf0 = convert_card_to_feature(board[0])
        bf1 = convert_card_to_feature(board[1])
        bf2 = convert_card_to_feature(board[2])

        evaluator = Evaluator()

        board3_features = copy.deepcopy(hands_features)
        assert len(hands) == len(board3_features), "ERROR: length of hand and features does not match!"
        for i in range(0, len(hands)):
            board3_features[i].update(bf0)
            board3_features[i].update(bf1)
            board3_features[i].update(bf2)

            rank = evaluator.evaluate(board, hands[i])
            percentage = 1.0 - evaluator.get_five_card_rank_percentage(rank)
            board3_features[i][100] = percentage
            # print("Board3 percentage: {}".format(percentage))


        # -----------
        board.append(deck.draw(1))
        if verbose:
            print("Board 4 (TURN):")
            print_deuces_card(board)
        bf0 = convert_card_to_feature(board[0])
        bf1 = convert_card_to_feature(board[1])
        bf2 = convert_card_to_feature(board[2])
        bf3 = convert_card_to_feature(board[3])

        board4_features = copy.deepcopy(board3_features)
        for i in range(0, len(hands)):
            board4_features[i].update(bf3)

            rank = evaluator.evaluate(board, hands[i])
            percentage = 1.0 - evaluator.get_five_card_rank_percentage(rank)
            board4_features[i][101] = percentage

            gap_board_4 = get_gap_between_hands_and_board(hands[i], board)
            board4_features[i][110] = gap_board_4 / 2000


        # -----------
        board.append(deck.draw(1))
        if verbose:
            print("Board 5 (RIVER):")
            print_deuces_card(board)
        bf0 = convert_card_to_feature(board[0])
        bf1 = convert_card_to_feature(board[1])
        bf2 = convert_card_to_feature(board[2])
        bf3 = convert_card_to_feature(board[3])
        bf4 = convert_card_to_feature(board[4])

        board5_features = copy.deepcopy(board4_features)
        for i in range(0, len(hands)):
            board5_features[i].update(bf4)

            rank = evaluator.evaluate(board, hands[i])
            percentage = 1.0 - evaluator.get_five_card_rank_percentage(rank)
            board5_features[i][102] = percentage

            gap_board_5 = get_gap_between_hands_and_board(hands[i], board)
            board5_features[i][111] = gap_board_5 / 2000

        #
        print("\n")
        evaluator = Evaluator()
        if verbose:
            evaluator.hand_summary(board, hands)

        winners = get_winner(board, hands)
        print("Winner: {}".format(winners))

        # dump hands_features into file
        for i in range(0, len(hands_features)):
            if i+1 in winners:
                libsvm_feature = convert_to_libsvm_format(1, hands_features[i])
            else:
                libsvm_feature = convert_to_libsvm_format(0, hands_features[i])
            samples_for_hand.write(libsvm_feature)

        # dump board3_features
        for i in range(0, len(board3_features)):
            if i+1 in winners:
                libsvm_feature = convert_to_libsvm_format(1, board3_features[i])
            else:
                libsvm_feature = convert_to_libsvm_format(0, board3_features[i])
            samples_for_board3.write(libsvm_feature)

        # dump board4_features
        for i in range(0, len(board4_features)):
            if i+1 in winners:
                libsvm_feature = convert_to_libsvm_format(1, board4_features[i])
            else:
                libsvm_feature = convert_to_libsvm_format(0, board4_features[i])
            samples_for_board4.write(libsvm_feature)

        # dump board5_features
        for i in range(0, len(board5_features)):
            if i+1 in winners:
                libsvm_feature = convert_to_libsvm_format(1, board5_features[i])
            else:
                libsvm_feature = convert_to_libsvm_format(0, board5_features[i])
            samples_for_board5.write(libsvm_feature)



        index += 1

    #
    samples_for_hand.close()
    samples_for_board3.close()
    samples_for_board4.close()
    samples_for_board5.close()

if __name__ == "__main__":
    main()
