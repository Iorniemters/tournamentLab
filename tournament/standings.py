

def calculate_standings(teams, fixtures):


    standings = {}

    team_names = {}

    for team in teams:
       team_names[team["id"]] = team["name"]

    for team in teams:
        standings[team["id"]] = {
            "team_id": team["id"],
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0
        }

    for fixture in fixtures:

        if fixture["status"] != "played":
            continue

        home = standings[fixture["home_id"]]
        away = standings[fixture["away_id"]]

        home_score = fixture["home_score"]
        away_score = fixture["away_score"]

        # Update matches played
        home["played"] += 1
        away["played"] += 1

        # Update goals
        home["goals_for"] += home_score
        home["goals_against"] += away_score

        away["goals_for"] += away_score
        away["goals_against"] += home_score

        # Calculate match outcome
        if home_score > away_score:
            home["wins"] += 1
            away["losses"] += 1
            home["points"] += 3

        elif home_score < away_score:
            away["wins"] += 1
            home["losses"] += 1
            away["points"] += 3

        else:
            home["draws"] += 1
            away["draws"] += 1
            home["points"] += 1
            away["points"] += 1

    for team_stats in standings.values():
        team_stats["goal_difference"] = (
            team_stats["goals_for"] - team_stats["goals_against"]
        )

    
    standings_list = list(standings.values())


    ranked_standings = sorted(
       standings_list,
       key=lambda team: (
         -team["points"],
         -team["goal_difference"],
         -team["goals_for"],
         team["goals_against"],
         team_names[team["team_id"]].casefold()
    )
)

    return ranked_standings