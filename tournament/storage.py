
import json


def validate_teams(teams):
    team_ids = set()
    team_names = set()

    for team in teams:

        if not isinstance(team, dict):
            raise ValueError("Each team must be a dictionary.")

        if "id" not in team or "name" not in team:
            raise ValueError("Each team must have an ID and name.")

        team_id = team["id"]
        team_name = team["name"]

        if not isinstance(team_id, str) or not team_id.strip():
            raise ValueError("Team ID must be non-empty text.")
        if team_id != team_id.strip():
           raise ValueError("Team ID cannot have surrounding spaces.")

        if not isinstance(team_name, str):
            raise ValueError("Team name must be text.")

        team_name = team_name.strip()

        if len(team_name) < 2 or len(team_name) > 30:
            raise ValueError("Team name must be between 2 and 30 characters.")

        if team_id in team_ids:
            raise ValueError("Duplicate team ID found.")

        if team_name.casefold() in team_names:
            raise ValueError("Duplicate team name found.")

        team_ids.add(team_id)
        team_names.add(team_name.casefold())

        
def validate_fixtures(fixtures, teams):
    team_ids = {team["id"] for team in teams}

    fixture_ids = set()
    pairings = set()

    for fixture in fixtures:

        if not isinstance(fixture, dict):
            raise ValueError("Each fixture must be a dictionary.")

        required_fields = [
            "id", "home_id", "away_id",
            "status", "home_score", "away_score"
        ]

        for field in required_fields:
            if field not in fixture:
                raise ValueError(f"Fixture is missing {field}.")

        fixture_id = fixture["id"]
        home_id = fixture["home_id"]
        away_id = fixture["away_id"]
        status = fixture["status"]
        home_score = fixture["home_score"]
        away_score = fixture["away_score"]

        if not isinstance(fixture_id, str) or not fixture_id.strip():
            raise ValueError("Fixture ID must be non-empty text.")

        if fixture_id != fixture_id.strip():
         raise ValueError("Fixture ID cannot have surrounding spaces.")

        if not isinstance(home_id, str) or not isinstance(away_id, str):
         raise ValueError("Team IDs in fixtures must be text.")

        if fixture_id in fixture_ids:
            raise ValueError("Duplicate fixture ID found.")

        if home_id not in team_ids or away_id not in team_ids:
            raise ValueError("Fixture references an unknown team.")

        if home_id == away_id:
            raise ValueError("A team cannot play against itself.")

        pairing = frozenset([home_id, away_id])

        if pairing in pairings:
            raise ValueError("Duplicate fixture pairing found.")

        if status not in ("pending", "played"):
            raise ValueError("Invalid fixture status.")

        if status == "pending":
            if home_score is not None or away_score is not None:
                raise ValueError("Pending fixtures cannot have scores.")

        if status == "played":
            for score in (home_score, away_score):
                if not isinstance(score, int) or isinstance(score, bool):
                    raise ValueError("Scores must be whole numbers.")

                if score < 0:
                    raise ValueError("Scores cannot be negative.")

        fixture_ids.add(fixture_id)
        pairings.add(pairing)



def save_tournament(teams, fixtures, filepath):
    validate_teams(teams)
    validate_fixtures(fixtures, teams)

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

    if not isinstance(data, dict):
        raise ValueError("Tournament data must be a dictionary.")

    if "schema_version" not in data:
        raise ValueError("Missing schema version.")

    if "teams" not in data or "fixtures" not in data:
        raise ValueError("Tournament data is missing required fields.")

    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ValueError("Unsupported tournament data version.")

    if not isinstance(data["teams"], list):
        raise ValueError("Teams must be stored as a list.")

    if not isinstance(data["fixtures"], list):
        raise ValueError("Fixtures must be stored as a list.")
    validate_teams(data["teams"])
    validate_fixtures(data["fixtures"], data["teams"])

    return data




