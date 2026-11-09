
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

    standings = calculate_standings(teams, fixtures)

    if not standings:
        return None
    
    leader = standings[0]

    
    leader_points = leader["points"]

        # No rival can catch the leader
        
    for team in teams:
        if team["id"] == leader["team_id"]:
            return {
                "team_id": leader["team_id"],
                "name": team["name"],
                "points": leader_points
            }

    return None