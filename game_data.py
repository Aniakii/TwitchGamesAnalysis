import requests
import datetime
import json
import os
from top_games import get_top_games

# Twitch API credentials
client_id = "tutsn1l6t4l48gulpacyxee17122si"
client_secret = "4htpc18wsghn2xl76cuergu3k2gdbh"
url = "https://api.twitch.tv/helix/streams"


def get_game_data(game_id, game_name):
    """
    Scrapes data about the current game streams from the Twitch API and saves it to a file.
    """

    # Set query parameters
    params = {"game_id": game_id}

    # Set request headers
    headers = {"Client-ID": client_id, "Authorization": f"Bearer {client_secret}"}

    # Process game name to ensure it can be used as a folder/file name
    game_name = (
        game_name.replace(":", "")
        .replace("/", " ")
        .replace("é", "e")
        .replace(".", "")
        .replace("?", "")
        .replace('"', "")
        .replace("'", "")
    )

    # Create directory if it doesn't exist
    if not os.path.exists(f"_games/{game_name}"):
        os.mkdir(f"_games/{game_name}")

    # Send request to Twitch API
    response = requests.get(url, params=params, headers=headers)
    time = datetime.datetime.now()
    output_file = f"_games/{game_name}/game_data_{game_id}_{time.date()}.json"

    # Process response
    if response.status_code == 200:
        # Extract data from response
        data = response.json()
        formatted_data = json.dumps(
            data, indent=4, separators=(", ", ": "), ensure_ascii=False
        )
        loaded_data = json.loads(formatted_data)

        # Add scraping time information
        loaded_data["scraping_time"] = {
            "time": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "weekday": str(time.strftime("%A")),
        }

        # Save data to file
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(
                json.dumps(
                    loaded_data, indent=4, separators=(", ", ": "), ensure_ascii=False
                )
            )
            print(f"Data has been saved to file: {output_file}")
    else:
        print(f"Request failed. Response code: {response.status_code}")


# Get file path for top games data
top_games_file = get_top_games()

# Read top games data from file
with open(top_games_file, "r", encoding="utf-8") as f:
    if os.stat(top_games_file).st_size == 0:
        games_data = []
    else:
        games_data = json.load(f)

# Scrape data for each game
for item in games_data["data"]:
    get_game_data(item["id"], item["name"])
