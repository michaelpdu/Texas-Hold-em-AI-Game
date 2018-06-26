#! /usr/bin/env python
# -*- coding:utf-8 -*-


import time
import sys
import json
from websocket import create_connection

# pip install websocket-client
ws = ""

def takeAction(player, action, data):
    if action == "__bet":
        #time.sleep(2)
        ws.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "bet",
                "playerName": player,
                "amount": 100
            }
        }))
    elif action == "__action":
        #time.sleep(2)
        ws.send(json.dumps({
            "eventName": "__action",
            "data": {
                "action": "call",
                "playerName": player
            }
        }))


def doListen(player):
    try:
        global ws
        ws = create_connection("ws://poker-dev.wrs.club:3001/")
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
            print event_name
            print data
            takeAction(player, event_name, data)
    except Exception, e:
        print e.message
        doListen()


if __name__ == '__main__':
    doListen(sys.argv[1])
