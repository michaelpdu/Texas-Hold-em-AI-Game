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

        evaluator = Evaluator()
        value = evaluator.evaluate(self.board_cards_, self.hand_cards_)
        print("Evaluation: {}".format(value))

        # calculate value of hand cards
        if len(self.board_cards_) == 5:
            board_value = evaluator.evaluate(self.board_cards_, [])
            gap = abs(value - board_value)
            print("(5 Board Cards) Gap: {}".format(gap))
            if gap < 20:
                self.take_action_fold()
                return
        elif len(self.board_cards_) == 4:
            v1 = evaluator.evaluate(self.board_cards_, [self.hand_cards_[0]])
            v2 = evaluator.evaluate(self.board_cards_, [self.hand_cards_[1]])
            gap1 = abs(value - v1)
            gap2 = abs(value - v2)
            max_gap = max(gap1, gap2)
            print("(4 Board Cards) V1: {}, V2: {}, Gap1: {}, Gap2: {}, Max Gap: {}".format(v1, v2, gap1, gap2, max_gap))
            if max_gap < 20:
                self.take_action_fold()
                return
        elif len(self.board_cards_) == 3:
            pass
        else:
            pass

        if value < 1000:
            self.take_action_bet(1000)
        elif value < 2000:
            self.take_action_bet(500)
        elif value < 3000:
            self.take_action_bet(300)
        elif value < 4000:
            self.take_action_bet(100)
        elif value < 5500:
            self.take_action_bet(50)
        elif value < 6800:
            self.take_action_call()
        else:
            self.take_action_fold()

    def take_action_by_hand(self, event_name, data):
        print("Take action by hand cards")
        print(data)

        # maximum bet
        max_bet = 0
        for player in data['game']['players']:
            if player['bet'] > max_bet:
                max_bet = player['bet']
        print("Max bet in hand cards: {}".format(max_bet))
        rank = get_rank_of_hand_cards(self.hand_cards_[0], self.hand_cards_[1])
        print("Rank of hand cards: {}".format(rank))
        if rank > 6:
            self.take_action_call()
        elif rank > 3 and max_bet < 500:
            self.take_action_call()
        elif rank > 1 and max_bet < 200:
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