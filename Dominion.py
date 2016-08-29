import argparse
import sys
from dominion import Identifiers
from dominion.engine.DominionEngine import DominionEngine
from communication.DirectInvocationCommunication import *
from communication.PlayerCommunication import PlayerCommunication
from dominion.starterbot.starter_bot import *
from dominion.model.Player import *

def main():
    args = _get_args()
    try:
        player1 = get_player(args.player1_cmd, args.player1_workdir)
        player2 = get_player(args.player2_cmd, args.player2_workdir)
        players = [player1, player2]
        if int(args.num_players) >= 3:
            players.append(get_player(args.player3_cmd, args.player3_workdir))
        if int(args.num_players) == 4:
            players.append(get_player(args.player4_cmd, args.player4_workdir))
        engine = DominionEngine(players, Identifiers.FIRST_GAME)
        engine.run_until_game_end()
        print "Scores were: "
        for index, player in enumerate(players, start=1):

            print "Player {} : Score: {} Turns Taken: {}".format(player.name, player.get_score(), player.get_number_of_turns_taken())
    except:
        raise
    finally:
        pass

def get_player(cmd, workdir):
    player = Player()
    if cmd == "starter_bot":
        starter_bot = StarterBot()
        comm = DirectInvocationCommunication(lambda msg: starter_bot.send_message(msg), lambda: starter_bot.get_response())
        player.set_communication(comm)
    else:
        comm = PlayerCommunication(cmd, workdir)
        player.set_communication(comm)
    return player

def _get_args():
    default_bot = "starter_bot"
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
