import argparse
import sys
from dominion.engine.DominionEngine import DominionEngine

def main():
    args = _get_args()
    try:
        engine = DominionEngine()
        engine.initialize()
        engine.run_until_game_end()
    except:
        raise
    finally:
        pass


def _get_args():
    default_bot = "{} {}".format(sys.executable, "runStarterBot.py")
    parser = argparse.ArgumentParser(
        description="Run a Battleline Engine with two bots")
    parser.add_argument(
        "--num-players", help="Number of players (2-4)", default=2)
    parser.add_argument(
        "--player1-cmd", help="Command to run player 1", default=default_bot)
    parser.add_argument(
        "--player1-workdir", help="Set the working directory for player 1", default=None)
    parser.add_argument(
        "--player2-cmd", help="Command to run player 2", default=default_bot)
    parser.add_argument(
        "--player2-workdir", help="Set the working directory for player 2", default=None)

    parser.add_argument(
        "--player3-cmd", help="Command to run player 3", default=default_bot)
    parser.add_argument(
        "--player3-workdir", help="Set the working directory for player 3", default=None)
    parser.add_argument(
        "--player4-cmd", help="Command to run player 4", default=default_bot)
    parser.add_argument(
        "--player4-workdir", help="Set the working directory for player 4", default=None)

    parser.add_argument("--server", action='store_true',
                        help="Output to Database")
    parser.add_argument(
        "--host", help="database host ip address default is localhost", default="localhost")
    parser.add_argument(
        "--port", help="database host port default is 27017", default="27017")
    parser.add_argument(
        "--database_name", help="database name default is dominion", default="dominion")
    return parser.parse_args()

if __name__ == "__main__":
    main()
