
import json


def save_tournament(teams, fixtures, filepath):
    data = {
        "schema_version": 1,
        "teams": teams,
        "fixtures": fixtures
    }

    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

def load_tournament(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    if data.get("schema_version") != 1:
        raise ValueError("Unsupported tournament data version.")

    return data