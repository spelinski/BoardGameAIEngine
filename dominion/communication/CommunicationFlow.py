from CommandGenerator import *
from dominion.CardInfo import *
from dominion.model.Supply import *
from dominion.Identifiers import *
import json
import itertools


def broadcast_message(players, message):
    for player in players:
        player.send_message(json.dumps(message))

def send_player_info(player, player_number, version):
    player_info_request = CommandGenerator().create_player_info_request(player_number, version)
    json_response = player.send_message_and_await_response(json.dumps(player_info_request))
    response = __get_json_message(json_response)
    __assert_message_type_is_correct(response, "player-name-reply")
    __assert_field_is_correct(response, "version", lambda v: v >= version, "Version mismatch")
    __assert_field_is_correct(response, "player_number", lambda p: p == player_info_request["player_number"], "Player Number Mismatch")
    player.name = response.get("name", player_info_request["player_number"].upper())

def send_supply_info(player, supply):
    supply_info_message = CommandGenerator().create_supply_info_message(supply.supply)
    player.send_message(json.dumps(supply_info_message))

def send_turn_request(player, supply, actions=1, buys=1, extra_money=0, gained_cards=None, other_players=[]):
    gained_cards = gained_cards if gained_cards else []
    play_turn_request = CommandGenerator().create_play_turn_request(actions, buys, extra_money, player.get_hand(), player.get_played_cards(), gained_cards)
    json_response = player.send_message_and_await_response(json.dumps(play_turn_request))
    try:
        response = __get_json_message(json_response)
        __assert_message_type_is_correct(response, "play-reply")
        __assert_field_is_correct(response, "phase", lambda p: p in ["action", "buy", "cleanup"], "Invalid Phase")
        if response["phase"] == "cleanup":
            top_discard = response.get("top_discard", "")
            __process_cleanup(top_discard, player)
        if response["phase"] == "buy":
            cards_to_buy = response.get("cards_to_buy", [])
            played_treasures = response.get("played_treasures", [])
            __process_buy(cards_to_buy, played_treasures, player, supply, buys, extra_money, gained_cards)
        if response["phase"] == "action":
            card = response.get("card", "")
            additional_parameters = response.get("additional_parameters", {})
            if type(additional_parameters) != dict: additional_parameters = {}
            __process_action(player, supply, actions, buys, extra_money, card, additional_parameters, gained_cards, other_players)
    except Exception as e:
        __process_cleanup(None, player)
        raise

def __process_cleanup(top_discard, player):
    player.cleanup(top_discard)
    player.draw_cards(5)

def __process_buy(cards_to_buy, played_treasures, player, supply, buys, extra_money, gained_cards):
    if not buys: raise Exception("Player did not have any more buys")
    try:
        money = __play_treasures(player, played_treasures) + extra_money
        for card in cards_to_buy[:buys]:
            if get_cost(card) > money:
                break
            money -= get_cost(card)
            supply.take(card)
            player.gain_card(card)
            gained_cards.append(card)
    except:
        pass

    send_turn_request(player, supply, 0, 0, 0, gained_cards)

def __play_treasures(player, played_treasures):
    money = 0
    for treasure in played_treasures:
        if not is_treasure(treasure):
            raise Exception("{} is not a treasure".format(treasure))
        player.play_card(treasure)
        money += get_worth(treasure)
    return money


def __sanitize_and_verify_parameters(player,supply, param, card):
    if card == CELLAR:
        if "cards" not in param or type(param["cards"]) != list:
            param["cards"] = []
    elif card == MINE:
        if "card_to_trash" not in param or not is_treasure(param["card_to_trash"]):
            raise Exception("Player must supply trashed treasure card")
        if "desired_card" not in param:
            param["desired_card"] = ""
        if not player.is_in_hand(param["card_to_trash"]):
            raise Exception("Card was not in player's hand")

        filters = [lambda card,_: get_cost(card) <= get_cost(param["card_to_trash"]) + 3,
                   lambda card,_: is_treasure(card),
                   lambda _,num: num > 0]
        available_supply_cards = supply.filter(filters).get_cards()
        if available_supply_cards and  param["desired_card"] not in available_supply_cards:
            raise Exception("Card was not able to be gained")
    elif card == REMODEL:
        if "card_to_trash" not in param or "desired_card" not in param:
            raise Exception("Player must supply trashed card and desired card")
        if not player.is_in_hand(param["card_to_trash"]):
            raise Exception("Card was not in player's hand")
        filters = [lambda card,_: get_cost(card) <= get_cost(param["card_to_trash"]) + 2,
                   lambda _,num: num > 0]
        if param["desired_card"] not in supply.filter(filters).get_cards():
                raise Exception("Card was not able to be gained")
    elif card == WORKSHOP:
        if get_cost(param["desired_card"]) > 4:
            raise Exception("Workshop card must cost 4 or less")
        if supply.get_number_of_cards(param["desired_card"] ) == 0:
            raise Exception("card not in supply")


def __process_action(player, supply, actions, buys, extra_money, card, parameters, gained_cards, other_players = []):
    if not actions: raise Exception("Player did not have any more actions")
    try:
        if not is_action_card(card):
            raise Exception("Player did not play an action card")
        if card not in player.get_hand():
            raise Exception("Player did not have the card")
        __sanitize_and_verify_parameters(player,supply, parameters, card)
    except Exception as e:
        send_turn_request(player, supply, actions-1, buys, extra_money, gained_cards, other_players)
        return

    def take_from_supply(card):
        supply.take(card)
        gained_cards.append(card)
        player.gain_card(card)

    player.draw_cards(get_extra_cards(card))
    if card == CELLAR:
        discards = list(itertools.takewhile(player.is_in_hand, parameters["cards"]))
        player.discard_multiple(discards)
        player.draw_cards(len(discards))
    elif card == MILITIA:
        for other_player in other_players:
            num_to_discard = len(other_player.get_hand()) - 3
            if num_to_discard <=0:
                break
            __send_discard_request(other_player, num_to_discard)
    elif card == MINE:
        player.trash(parameters["card_to_trash"])
        desired_card = parameters["desired_card"]
        if desired_card:
            supply.take(desired_card)
            gained_cards.append(desired_card)
            player.add_to_hand(desired_card)
    elif card == REMODEL:
        player.trash(parameters["card_to_trash"])
        take_from_supply(parameters["desired_card"])
    elif card == WORKSHOP:
        take_from_supply(parameters["desired_card"])
    actions += get_extra_actions(card)
    buys += get_extra_buys(card)
    extra_money += get_extra_treasure(card)
    player.play_card(card)

    send_turn_request(player, supply, actions-1, buys, extra_money, gained_cards, other_players)

def __send_discard_request(player, num_to_discard):
    discard_request = CommandGenerator().create_attack_request_discard(num_to_discard, player.get_hand())
    json_response = player.send_message_and_await_response(json.dumps(discard_request))
    try:
        response = __get_json_message(json_response)
        if __is_valid_moat_response(response, player):
            return
        __assert_message_type_is_correct(response, "attack-reply")
        __assert_field_is_correct(response, "discard", lambda d: type(d) == list and len(d) == num_to_discard and all(discard in player.get_hand() for discard in d ), "Invalid discards")
        for discard in response["discard"]:
            player.discard(discard)
    except:
        for discard in player.get_hand()[:num_to_discard]:
            player.discard(discard)

def __is_valid_moat_response(response, player):
    return response.get("type", "") == "attack-reply-reaction" and response.get("reaction", "") == MOAT and MOAT in player.get_hand()


def __get_json_message(json_response):
    try:
        return json.loads(json_response)
    except:
        raise Exception("Message was not JSON: {}".format(json_response))

def __assert_message_type_is_correct(response, expected):
    __assert_field_is_correct(response, "type", lambda t: t == expected, "Message was not correct type")

def __assert_field_is_correct(response, field, matcher_func, exception_text):
    value = response[field] if field in response else "Not Present"
    if not matcher_func(value) or value == "Not Present":
        raise Exception("{}: {}".format(exception_text, value))
