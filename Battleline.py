import argparse
import sys
from battleline.engine.BattlelineEngine import BattlelineEngine
from battleline.player.BattlelinePlayer import SubprocessPlayer
from communcation.PlayerCommunication import PlayerCommunication
from battleline.view.Output import Output
from battleline.view.DatabaseOutput import DatabaseOutput


def main():
    args = _get_args()
    try:
        comm1 = PlayerCommunication(args.player1_cmd, args.player1_workdir)
        comm2 = PlayerCommunication(args.player2_cmd, args.player2_workdir)
        player1 = SubprocessPlayer(comm1)
        player2 = SubprocessPlayer(comm2)
        outputer = DatabaseOutput(args.host, int(
            args.port), args.database_name) if args.server else Output()
        engine = BattlelineEngine(player1, player2, outputer)
        engine.initialize()
        engine.run_until_game_end()
        print "PLAYER : {} -> {} HAS WON".format(engine.get_winning_player(), engine.get_winning_player_name())
    except:
        raise
    finally:
        comm1.close()
        comm2.close()


def _get_args():
    default_bot = "{} {}".format(sys.executable, "runStarterBot.py")
    parser = argparse.ArgumentParser(
        description="Run a Battleline Engine with two bots")
    parser.add_argument(
        "--player1-cmd", help="Command to run player 1", default=default_bot)
    parser.add_argument(
        "--player1-workdir", help="Set the working directory for player 1", default=None)
    parser.add_argument(
        "--player2-cmd", help="Command to run player 2", default=default_bot)
    parser.add_argument(
        "--player2-workdir", help="Set the working directory for player 2", default=None)
    parser.add_argument("--server", action='store_true',
                        help="Output to Database")
    parser.add_argument(
        "--host", help="database host ip address default is localhost", default="localhost")
    parser.add_argument(
        "--port", help="database host port default is 27017", default="27017")
    parser.add_argument(
        "--database_name", help="database name default is battleline", default="battleline")
    return parser.parse_args()

if __name__ == "__main__":
    main()
