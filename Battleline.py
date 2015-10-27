import argparse
import sys
from battleline.engine.BattlelineEngine import BattlelineEngine
from battleline.player.BattlelinePlayer import SubprocessPlayer
from communcation.PlayerCommunication import PlayerCommunication


def main():
    args = _get_args()
    try:
        comm1 = PlayerCommunication(args.player1_cmd, args.player1_workdir)
        comm2 = PlayerCommunication(args.player2_cmd, args.player2_workdir)
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
    default_bot = "{} {}".format(sys.executable, "runStarterBot.py")
    parser = argparse.ArgumentParser(
        description="Run a Battleline Engine with two bots")
    parser.add_argument("--player1-cmd", help="Command to run player 1", default=default_bot)
    parser.add_argument("--player1-workdir", help="Set the working directory for player 1", default=None)
    parser.add_argument("--player2-cmd", help="Command to run player 2", default=default_bot)
    parser.add_argument("--player2-workdir", help="Set the working directory for player 2", default=None)
    return parser.parse_args()

if __name__ == "__main__":
    main()
