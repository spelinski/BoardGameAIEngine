from CommandGenerator import *
from dominion.CardInfo import *
from dominion.model.Supply import *
import json

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
        for treasure in played_treasures:
            if not is_treasure(treasure):
                raise Exception("{} is not a treasure".format(treasure))
            player.play_card(treasure)
        money = sum([get_worth(card) for card in player.get_played_cards()]) + extra_money
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

def __process_action(player, supply, actions, buys, extra_money, card, additional_parameters, gained_cards, other_players = []):
    if not actions: raise Exception("Player did not have any more actions")
    try:
        if card not in player.get_hand():
            raise Exception("Player did not have the card")
        if card == Identifiers.CELLAR:
            actions += 1
            discards = additional_parameters.get("cards", [])
            for discard in discards:
                if discard not in player.get_hand():
                    break
                player.discard(discard)
                player.draw_cards(1)
        if card == Identifiers.MOAT:
            player.draw_cards(2)
        if card == Identifiers.MARKET:
            player.draw_cards(1)
            actions += 1
            buys += 1
            extra_money += 1
        if card == Identifiers.MILITIA:
            extra_money += 2
            for other_player in other_players:
                num_to_discard = len(other_player.get_hand()) - 3
                if num_to_discard <=0:
                    break
                discard_request = CommandGenerator().create_attack_request_discard(num_to_discard, other_player.get_hand())
                json_response = other_player.send_message_and_await_response(json.dumps(discard_request))
                try:
                    response = __get_json_message(json_response)
                    if response.get("type", "") == "attack-reply-reaction" and response.get("reaction", "") == Identifiers.MOAT and Identifiers.MOAT in other_player.get_hand():
                        break
                    __assert_message_type_is_correct(response, "attack-reply")
                    __assert_field_is_correct(response, "discard", lambda d: type(d) == list and len(d) == num_to_discard and all(discard in other_player.get_hand() for discard in d ), "Invalid discards")
                    for discard in response["discard"]:
                        other_player.discard(discard)
                except:
                    for discard in other_player.get_hand()[:num_to_discard]:
                        other_player.discard(discard)
        if card == Identifiers.MINE:
            trashed_card = additional_parameters["card_to_trash"]
            desired_card = additional_parameters.get("desired_card", "")
            available_supply_cards = [supply_card for supply_card in supply.get_cards() if get_cost(supply_card) <= get_cost(trashed_card) + 3 and is_treasure(supply_card) and supply.get_number_of_cards(supply_card) > 0]
            if available_supply_cards:
                if desired_card not in available_supply_cards:
                    raise Exception("Card was too expensive to gain in remodel or not a treasure")
                if supply.get_number_of_cards(desired_card) == 0:
                    raise Exception("Card not in supply")
            if not is_treasure(trashed_card):
                raise Exception("Card is not a treasure")
            player.trash(trashed_card)
            if available_supply_cards:
                supply.take(desired_card)
                gained_cards.append(desired_card)
                player.add_to_hand(desired_card)
        if card == Identifiers.REMODEL:
            trashed_card = additional_parameters["card_to_trash"]
            desired_card = additional_parameters["desired_card"]
            available_supply_cards = [supply_card for supply_card in supply.get_cards() if get_cost(supply_card) <= get_cost(trashed_card) + 2]
            if desired_card not in available_supply_cards:
                raise Exception("Card was too expensive to gain in remodel")
            if supply.get_number_of_cards(desired_card) == 0:
                raise Exception("Card not in supply")
            player.trash(trashed_card)
            supply.take(desired_card)
            gained_cards.append(desired_card)
            player.gain_card(desired_card)
        if card == Identifiers.SMITHY:
            player.draw_cards(3)
        if card == Identifiers.VILLAGE:
            player.draw_cards(1)
            actions += 2
        if card == Identifiers.WOODCUTTER:
            buys += 1
            extra_money += 2
        if card == Identifiers.WORKSHOP:
            desired_card = additional_parameters["desired_card"]
            if get_cost(desired_card) > 4:
                raise Exception("Workshop card must be 4 or less")
            supply.take(desired_card)
            gained_cards.append(desired_card)
            player.gain_card(desired_card)
        player.play_card(card)
    except:
        pass

    send_turn_request(player, supply, actions-1, buys, extra_money, gained_cards, other_players)

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
