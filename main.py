import sys
from player import Player

# server = "ws://pokerai.trendmicro.com.cn:80/"
# server = "ws://poker-dev.wrs.club:3001/"
server = "ws://10.64.8.72:80/"

def doListen(player_name):
    try:
        player = Player(server, player_name)
        player.join_game()
        while 1:
            player.receive_data()
    except Exception as e:
        print("ERROR: "+e.message)
        doListen(sys.argv[1])

if __name__ == '__main__':
    player_name = sys.argv[1]
    print("Player Name: {}".format(player_name))
    doListen(player_name)
