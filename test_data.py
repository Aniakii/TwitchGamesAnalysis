import os
import json
import random
from enum import Enum

file_name = "all_data.json"


class TypeOfData(Enum):
    ALL = 1
    RANDOM = 2
    TOP = 3


def get_test_data(type, max_amount=0):
    """
    Retrieve test data based on the maximum place from the top games statistics.
    """
    top_games_path = "_games_statistics/_top_games_stats.json"
    all_games_path = "_games_statistics/_all_games_stats.json"

    with open(top_games_path, "r", encoding="utf-8") as top_games_file:
        top_games_data = json.load(top_games_file)

        with open(all_games_path, "r", encoding="utf-8") as all_games_file:
            all_games_data = json.load(all_games_file)
            if type == TypeOfData.ALL:
                test_data = get_all_data(top_games_data, all_games_data)
            elif type == TypeOfData.RANDOM:
                test_data = get_random_data(max_amount, top_games_data, all_games_data)
            elif type == TypeOfData.TOP:
                test_data = get_top_data(max_amount, top_games_data, all_games_data)
    return test_data


def get_all_data(top_games_data, all_games_data):
    test_data = []
    for top_game in top_games_data:
        game_info = get_game_data(top_game, all_games_data)
        if game_info is not None:
            test_data.append(game_info)
    return test_data


def get_top_data(max_amount, top_games_data, all_games_data):
    test_data = []
    for top_game in top_games_data:
        if len(test_data) == max_amount:
            break
        game_info = get_game_data(top_game, all_games_data)
        if game_info is not None:
            test_data.append(game_info)
    return test_data


def get_random_data(max_amount, top_games_data, all_games_data):
    test_data = []
    used_numbers = []
    while len(test_data) < max_amount:
        random_number = random.randint(0, len(top_games_data) - 1)
        if random_number in used_numbers:
            continue
        else:
            used_numbers.append(random_number)
            top_game = top_games_data[random_number]
            game_info = get_game_data(top_game, all_games_data)
            if game_info is not None:
                test_data.append(game_info)
    return test_data


def get_game_data(game, all_games_data):
    game_info = {}
    for game_data in all_games_data:
        if game_data["id"] == game["id"]:
            game_info = game_data
            break
    if game_info == {}:
        print(f"brak danych: {game['name']}")
        return None
    if "hours sum" in game_info:
        game_info.pop("hours sum")
    if "viewers sum" in game_info:
        game_info.pop("viewers sum")
    game_info["average place"] = game["average place"]
    game_info["amount in top"] = game["amount in top"]
    return game_info


testing_data = get_test_data(TypeOfData.ALL)
test_data_file = os.path.join("_data", file_name)

# Save the test data to a file
with open(test_data_file, "w", encoding="utf-8") as f:
    json.dump(testing_data, f, indent=4)
