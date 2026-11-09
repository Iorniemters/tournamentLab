

def generate_fixtures(teams):
    
    if len(teams) < 4:
        raise ValueError("At least 4 teams are required.")

    if len(teams) > 8:
        raise ValueError("A maximum of 8 teams is allowed.")

    fixtures = []
    fixture_number = 1

    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):

            fixture = {
                "id": f"M{fixture_number:03d}",
                "home_id": teams[i]["id"],
                "away_id": teams[j]["id"],
                "status": "pending",
                "home_score": None,
                "away_score": None
            }

            fixtures.append(fixture)
            fixture_number += 1

    return fixtures
