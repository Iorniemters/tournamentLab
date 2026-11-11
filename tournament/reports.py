
from tournament.standings import calculate_standings


def get_champion(teams, fixtures):

    if not fixtures:
        return None


    for fixture in fixtures:
        if fixture["status"] != "played":
            return None

    standings = calculate_standings(teams, fixtures)

    champion = standings[0]

    for team in teams:
        if team["id"] == champion["team_id"]:
            return {
                "team_id": champion["team_id"],
                "name": team["name"],
                "points": champion["points"]
            }

    return None


def get_mathematical_champion(teams, fixtures):

    if not fixtures:
        return None

    standings = calculate_standings(teams, fixtures)

    if not standings:
        return None

    leader = standings[0]
    leader_points = leader["points"]

    remaining_matches = {}

    for team in teams:
        remaining_matches[team["id"]] = 0

    for fixture in fixtures:
        if fixture["status"] == "pending":
            remaining_matches[fixture["home_id"]] += 1
            remaining_matches[fixture["away_id"]] += 1

    for team in standings[1:]:
        team_id = team["team_id"]
        current_points = team["points"]
        remaining = remaining_matches[team_id]

        maximum_points = current_points + (remaining * 3)

        if maximum_points >= leader_points:
            return None

    for team in teams:
        if team["id"] == leader["team_id"]:
            return {
                "team_id": leader["team_id"],
                "name": team["name"],
                "points": leader_points
            }

    return None
