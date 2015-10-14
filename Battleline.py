import sys
from battleline.engine.BattlelineEngine import BattlelineEngine
from battleline.player.BattlelinePlayer import SubprocessPlayer
from communcation.PlayerCommunication import PlayerCommunication


def main():
    try:
        player1_command, player2_command = sys.argv[1:3]
        comm1 = PlayerCommunication(player1_command)
        comm2 = PlayerCommunication(player2_command)
        player1 = SubprocessPlayer(comm1)
        player2 = SubprocessPlayer(comm2)
        engine = BattlelineEngine(player1, player2)
        engine.run_until_game_end()
        print "PLAYER : {} HAS WON".format(engine.get_winning_player())
    except:
        comm1.close()
        comm2.close()
        raise

if __name__ == "__main__":
    main()
