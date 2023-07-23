import requests
import json
import datetime
import os

# Twitch API credentials
client_id = "tutsn1l6t4l48gulpacyxee17122si"
bearer_token = "4htpc18wsghn2xl76cuergu3k2gdbh"

url = "https://api.twitch.tv/helix/games/top"

headers = {"Client-ID": client_id, "Authorization": f"Bearer {bearer_token}"}


def get_top_games():
    """
    Scrapes data about the top games from the Twitch API and saves it to a file.
    Returns the file path of the saved data.
    """
    response = requests.get(url, headers=headers)
    time = datetime.datetime.now()

    # Create directory if it doesn't exist
    if not os.path.exists("_top_games"):
        os.mkdir("_top_games")

    output_file = f"_top_games/top_games_{time.date()}.json"

    if response.status_code == 200:
        # Process response
        data = response.json()
        formatted_data = json.dumps(
            data, indent=4, separators=(", ", ": "), ensure_ascii=False
        )
        main_data = json.loads(formatted_data)
        main_data["scraping_time"] = {
            "time": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "weekday": str(time.strftime("%A")),
        }
        cursor = main_data["pagination"]["cursor"]

        with open(output_file, "w", encoding="utf-8") as file:
            for _ in range(50):
                response = requests.get(url, headers=headers, params={"after": cursor})
                data = response.json()
                formatted_data = json.dumps(
                    data, indent=4, separators=(", ", ": "), ensure_ascii=False
                )
                loaded_data = json.loads(formatted_data)
                main_data["data"] += loaded_data["data"]
                cursor = loaded_data["pagination"]["cursor"]

            # Save data to file
            file.write(
                json.dumps(
                    main_data, indent=4, separators=(", ", ": "), ensure_ascii=False
                )
            )
            print(f"Data has been saved to file: {output_file}")
        return output_file
    else:
        print(f"Request failed. Response code: {response.status_code}")
