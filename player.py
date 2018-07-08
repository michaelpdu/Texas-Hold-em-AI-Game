#! /usr/bin/env python
# -*- coding:utf-8 -*-


import time
import sys
import json
import hashlib
from websocket import create_connection
from deuces import Card, Evaluator

# pip install websocket-client
ws = ""

current_md5 = ''
hand = []
board = []

def take_action_fold(player):
    print(">>> fold")
    ws.send(json.dumps({
        "eventName": "__action",
        "data": {
            "action": "fold",
            "playerName": player
        }
    }))

def convertToDeucesCard(card_string):
    deuces_card = card_string[0]
    deuces_card += card_string[1].lower()
    return deuces_card

def takeActionByDeuces(player, action, data):
    global hand
    global board

    board = []
    board_cards = data['game']['board']
    for card in board_cards:
        board.append(Card.new(convertToDeucesCard(card)))
    print("****** Cards Information ******")
    Card.print_pretty_cards(hand)
    Card.print_pretty_cards(board)
    print("*******************************")

    evaluator = Evaluator()
    value = evaluator.evaluate(board, hand)
    print("Evaluation: {}".format(value))

    # calculate value of hand cards
    if len(board) == 5:
        board_value = evaluator.evaluate(board, [])
        gap = abs(value - board_value)
        print("(5 Board Cards) Gap: {}".format(gap))
        if gap < 20:
            take_action_fold(player)
            return
    elif len(board) == 4:
        v1 = evaluator.evaluate(board, [hand[0]])
        v2 = evaluator.evaluate(board, [hand[1]])
        gap1 = abs(value - v1)
        gap2 = abs(value - v2)
        max_gap = max(gap1, gap2)
        print("(4 Board Cards) V1: {}, V2: {}, Gap1: {}, Gap2: {}, Max Gap: {}".format(v1, v2, gap1, gap2, max_gap))
        if max_gap < 20:
            take_action_fold(player)
            return

    if value < 1000:
        print(">>> bet: 1000")
        ws.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "bet",
                "playerName": player,
                "amount": 1000
            }
        }))
    elif value < 2000:
        print(">>> bet: 500")
        ws.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "bet",
                "playerName": player,
                "amount": 500
            }
        }))
    elif value < 3000:
        print(">>> bet: 300")
        ws.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "bet",
                "playerName": player,
                "amount": 300
            }
        }))
    elif value < 4000:
        print(">>> bet: 100")
        ws.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "bet",
                "playerName": player,
                "amount": 100
            }
        }))
    elif value < 5500:
        print(">>> bet: 50")
        ws.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "bet",
                "playerName": player,
                "amount": 50
            }
        }))
    elif value < 6800:
        print(">>> call")
        ws.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "call",
                "playerName": player
            }
        }))
    else:
        print(">>> fold")
        ws.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "fold",
                "playerName": player
            }
        }))

def takeActionByHand(player, action, data):
    print(">>> call")
    ws.send(json.dumps({
        "eventName": "__action",
        "data": {
            "action": "call",
            "playerName": player
        }
    }))

def takeAction(player, action, data):
    global current_md5
    global hand
    global board

    # print(action)
    # print(data)

    if action == "__new_peer":
        # calcuate md5 by player name
        # current_md5 = "70be3acc4a99a780e1b405e1ff7971c5"
        current_md5 = hashlib.md5(player).hexdigest()
        print('MD5 of Current User: ' + current_md5)
    elif action == "__game_prepare":
        print("Game prepare: {}".format(data))
    elif action == "__new_round":
        print("\n\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        hand = []
        board = []
        for player_info in data["players"]:
            if current_md5 == player_info['playerName']:
                card_list = player_info['cards']
                for card in card_list:
                    hand.append(Card.new(convertToDeucesCard(card)))
                print("****** My hand cards ******")
                Card.print_pretty_cards(hand)
                print("***************************")
    elif action == "__bet":
        takeActionByDeuces(player, action, data)
    elif action == "__action":
        if len(data['game']['board']) == 0:
            takeActionByHand(player, action, data)
        else:
            takeActionByDeuces(player, action, data)

def doListen(player):
    try:
        global ws
        ws = create_connection("ws://poker-dev.wrs.club:3001/")
        # ws = create_connection("ws://10.64.8.72:80/")
        ws.send(json.dumps({
            "eventName": "__join",
            "data": {
                "playerName": player
            }
        }))
        while 1:
            result = ws.recv()
            msg = json.loads(result)
            event_name = msg["eventName"]
            data = msg["data"]
            takeAction(player, event_name, data)
    except Exception as e:
        print(e.message)
        doListen(sys.argv[1])


if __name__ == '__main__':
    doListen(sys.argv[1])
