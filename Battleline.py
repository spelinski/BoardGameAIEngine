import sys
from battleline.engine.BattlelineEngine import BattlelineEngine
from battleline.player.BattlelinePlayer import SubprocessPlayer
from communcation.PlayerCommunication import PlayerCommunication

def main():
    player1_command, player2_command = sys.argv[1:3]
    player1 = SubprocessPlayer(PlayerCommunication(player1_command))
    player2 = SubprocessPlayer(PlayerCommunication(player2_command))
    engine = BattlelineEngine(player1, player2)
    engine.run_until_game_end()
    print "PLAYER : {} HAS WON".format(engine.get_winning_player())

if __name__ == "__main__":
    main()
