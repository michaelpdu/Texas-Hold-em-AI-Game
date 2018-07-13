import json
import hashlib
from websocket import create_connection
from card_util import *

class Player:
    """"""

    def __init__(self, server, name):
        self.ws_ = create_connection(server)
        self.name_ = name
        self.md5_ = hashlib.md5(name).hexdigest()
        self.hand_cards_ = []
        self.board_cards_ = []

    def join_game(self):
        self.ws_.send(json.dumps({
            "eventName": "__join",
            "data": {
                "playerName": self.name_
            }
        }))

    def receive_data(self):
        result = self.ws_.recv()
        msg = json.loads(result)
        event_name = msg["eventName"]
        data = msg["data"]
        self.process_data(event_name, data)

    def calc_pre_max_bet(self, data):
        # maximum bet
        self.pre_max_bet_ = 0
        for player in data['game']['players']:
            if player['bet'] > self.pre_max_bet_:
                self.pre_max_bet_ = player['bet']
        print("Previous Max Bet: {}".format(self.pre_max_bet_))

    def get_big_blind(self, data):
        big_blind = data['game']['bigBlind']['amount']
        return big_blind

    def process_data(self, event_name, data):
        print("Event Name: " + event_name)

        if event_name == "__new_peer":
            print(data)
        elif event_name == "__game_prepare":
            print(data)
        elif event_name == "__new_round":
            self.hand_cards_ = []
            print("\n\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            for player_info in data["players"]:
                if self.md5_ == player_info['playerName']:
                    card_list = player_info['cards']
                    for card in card_list:
                        self.hand_cards_.append(create_deuces_card(card))
                    print("****** My hand cards ******")
                    print_deuces_card(self.hand_cards_)
                    print("***************************")
        elif event_name == "__bet" or event_name == "__action":
            self.calc_pre_max_bet(data)
            if len(data['game']['board']) == 0:
                self.take_action_by_hand(event_name, data)
            else:
                self.take_action_by_deuces(event_name, data)
        else:
            pass

    def get_board_cards(self, data):
        self.board_cards_ = []
        board_cards = data['game']['board']
        board_cards_count = len(board_cards)
        if board_cards_count == 0:
            return 0
        for card in board_cards:
            self.board_cards_.append(create_deuces_card(card))
        print("****** Cards Information ******")
        print_deuces_card(self.hand_cards_)
        print_deuces_card(self.board_cards_)
        print("*******************************")
        return board_cards_count

    #
    def take_action_by_deuces(self, event_name, data):
        board_cards_count = self.get_board_cards(data)
        assert(board_cards_count >= 3)
        big_blind = self.get_big_blind(data)

        evaluator = Evaluator()
        value = evaluator.evaluate(self.board_cards_, self.hand_cards_)
        print("Evaluation: {}".format(value))

        # calculate value of hand cards
        if len(self.board_cards_) > 3:
            gap = get_gap_between_hands_and_board(self.hand_cards_, self.board_cards_)
            if gap < 20:
                self.take_action_fold()
                return
        elif len(self.board_cards_) == 3:
            pass
        else:
            pass

        if value < 500:
            self.tak_action_allin()
        elif value < 1000:
            self.take_action_bet(5*big_blind)
        elif value < 2000:
            self.take_action_bet(3*big_blind)
        elif value < 3000:
            self.take_action_bet(2*big_blind)
        elif value < 4000:
            if self.pre_max_bet_-big_blind < 300:
                self.take_action_call()
            else:
                self.take_action_fold()
        elif value < 5000:
            if self.pre_max_bet_-big_blind < 200:
                self.take_action_call()
            else:
                self.take_action_fold()
        elif value < 6000:
            if self.pre_max_bet_-big_blind < 100:
                self.take_action_call()
            else:
                self.take_action_fold()
        else:
            self.take_action_fold()

    def take_action_by_hand(self, event_name, data):
        print("Take action by hand cards")
        print(data)
        big_blind = self.get_big_blind(data)

        rank, features = get_rank_of_hand_cards(self.hand_cards_[0], self.hand_cards_[1])
        print("Rank of hand cards: {}".format(rank))
        if rank > 6:
            self.take_action_call()
        elif rank > 3 and (self.pre_max_bet_ - big_blind) < 200:
            self.take_action_call()
        elif rank >= 1 and (self.pre_max_bet_ - big_blind) < 100:
            self.take_action_call()
        else:
            self.take_action_fold()

    # action list
    def take_action_check(self):
        print(">>> Take Action: check")
        self.ws_.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "check",
                "playerName": self.name_
            }
        }))

    def take_action_bet(self, amount):
        print(">>> Take Action: bet, amount: {}".format(amount))
        self.ws_.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "bet",
                "playerName": self.name_,
                "amount": amount
            }
        }))

    def take_action_call(self):
        print(">>> Take Action: call")
        self.ws_.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "call",
                "playerName": self.name_
            }
        }))

    def take_action_raise(self):
        print(">>> Take Action: raise")
        self.ws_.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "raise",
                "playerName": self.name_
            }
        }))

    def take_action_fold(self):
        print(">>> Take Action: fold")
        self.ws_.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "fold",
                "playerName": self.name_
            }
        }))

    def tak_action_allin(self):
        print(">>> Take Action: allin")
        self.ws_.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "allin",
                "playerName": self.name_
            }
        }))

    #