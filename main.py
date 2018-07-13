import sys
from player import Player
from player_xgb import PlayerXGB

server = "ws://pokerai.trendmicro.com.cn:80/"
# server = "ws://poker-dev.wrs.club:3001/"
# server = "ws://10.64.8.72:80/"

def doListen(player_name):
    try:
        if sys.argv[2] == 'xgb':
            player = PlayerXGB(server, player_name)
        else:
            player = Player(server, player_name)

        player.join_game()
        while 1:
            player.receive_data()
    except Exception as e:
        print("ERROR: "+e.message)
        doListen(sys.argv[1])

help_msg = """
Usage:
    python main.py player_name [xgb|rule]
"""

if __name__ == '__main__':
    player_name = sys.argv[1]
    print("Player Name: {}".format(player_name))
    doListen(player_name)
