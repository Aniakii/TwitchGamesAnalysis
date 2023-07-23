import os
import json
from datetime import datetime
from re import search

# Create a directory for storing game statistics
if not os.path.exists("_games_statistics"):
    os.mkdir("_games_statistics")

all_games_data = []
games_in_top = []


def game_statistics(game_name):
    """
    Calculate statistics for a game based on its data files.
    Save the statistics to a file in the game statistics directory.
    """
    # print(f"game statistics for {game_name}")
    game_path = f"_games/{game_name}"
    if os.path.exists(game_path):
        # Parameters nedeed to describe statistics
        records = 0
        viewers_sum = 0
        hours_sum = 0
        languages = {}
        game_id = ""
        id_pattern = r"game_data_(\d+)_"
        for filename in os.listdir(game_path):
            with open(os.path.join(game_path, filename), "r", encoding="utf-8") as file:
                game_data = json.load(file)
                scraping_time = game_data["scraping_time"]["time"]
                date = datetime.strptime(scraping_time, "%Y-%m-%dT%H:%M:%S")
                if game_id == "":
                    match = search(id_pattern, filename)
                    if match:
                        game_id = match.group(1)
                if len(game_data["data"]) == 0:
                    # print(f"No data available for file {filename}")
                    continue
                else:
                    for item in game_data["data"]:
                        records += 1
                        viewers_sum += item["viewer_count"]

                        if item["language"] in languages:
                            languages[item["language"]] += 1
                        else:
                            languages[item["language"]] = 1

                        starting_time = item["started_at"]
                        time = datetime.strptime(starting_time, "%Y-%m-%dT%H:%M:%SZ")
                        diff = date - time
                        hours_sum += diff.total_seconds() / 3600

    if records != 0:
        data = {
            "game name": game_name,
            "records": records,
            "id": game_id,
            "hours sum": hours_sum,
            "viewers sum": viewers_sum,
            "languages": len(languages),
            "avg viewers": viewers_sum / records,
            "avg hours": hours_sum / records,
        }
        all_games_data.append(data)
        data_together = [data]

        # Combine game statistics with top games information
        for games in games_in_top:
            if games["id"] == game_id:
                data_together.append(games)

        output_file = os.path.join("_test", f"{game_name}_stats.json")

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data_together, file, indent=4)

    else:
        print(f"No data to save for game {game_name}.")


def top_games_statistics():
    """
    Calculate statistics for top games based on data files.
    Save the statistics to a file in the game statistics directory.
    """
    top_games_files = os.listdir("_top_games")

    for file in top_games_files:
        if file.endswith(".json"):
            with open(
                os.path.join("_top_games", file), "r", encoding="utf-8"
            ) as data_file:
                try:
                    top_data = json.load(data_file)
                    games_names = []

                    for item in top_data["data"]:
                        if item["name"] in games_names:
                            continue
                        else:
                            games_names.append(item["name"])

                        if_in_list = False

                        for game in games_in_top:
                            if game["name"] == item["name"]:
                                game["amount in top"] += 1
                                game["place in top"].append(
                                    top_data["data"].index(item) + 1
                                )
                                if_in_list = True
                                break

                        if not if_in_list:
                            games_in_top.append(
                                {
                                    "name": item["name"],
                                    "id": item["id"],
                                    "amount in top": 1,
                                    "place in top": [top_data["data"].index(item) + 1],
                                }
                            )

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON file {file}: {e}")

    for game in games_in_top:
        game["average place"] = sum(game["place in top"]) / game["amount in top"]

    games_in_top.sort(key=lambda x: x["average place"])

    output_file = os.path.join("_test", "_top_games_stats.json")

    with open(output_file, "w", encoding="utf-8") as data_file:
        json.dump(games_in_top, data_file, indent=4)


# top_games_statistics()

folders = os.listdir("_games")
# print(len(folders))
for folder in folders:
    if folder.startswith("_"):
        print("continue")
        continue
    game_statistics(folder)

all_games_file = os.path.join("_test", "_all_games_stats.json")
all_games_data.sort(key=lambda x: x["avg viewers"], reverse=True)

with open(all_games_file, "w", encoding="utf-8") as f:
    json.dump(all_games_data, f, indent=4)
