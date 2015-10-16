import argparse
from battleline.engine.BattlelineEngine import BattlelineEngine
from battleline.player.BattlelinePlayer import SubprocessPlayer
from communcation.PlayerCommunication import PlayerCommunication


def main():
    args = _get_args()
    try:
        comm1 = PlayerCommunication(args.player1)
        comm2 = PlayerCommunication(args.player2)
        player1 = SubprocessPlayer(comm1)
        player2 = SubprocessPlayer(comm2)
        engine = BattlelineEngine(player1, player2)
        engine.initialize()
        engine.run_until_game_end()
        print "PLAYER : {} HAS WON".format(engine.get_winning_player())
    except:
        raise
    finally:
        comm1.close()
        comm2.close()


def _get_args():
    parser = argparse.ArgumentParser(
        description="Run a Battleline Engine with two bots")
    parser.add_argument("player1", help="Command to run player 1")
    parser.add_argument("player2", help="Command to run player 2")
    return parser.parse_args()

if __name__ == "__main__":
    main()
