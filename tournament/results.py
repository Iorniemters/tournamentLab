
def record_result(fixtures, fixture_id, home_score, away_score):

    selected_fixture = None

    for fixture in fixtures:
        if fixture["id"] == fixture_id:
            selected_fixture = fixture
            break

    if selected_fixture is None:
        raise ValueError("Fixture not found.")

    if selected_fixture["status"] == "played":
        raise ValueError("This fixture already has a result.")

    
    if not isinstance(home_score, int) or isinstance(home_score, bool):
        raise ValueError("Home score must be a whole number.")

    if home_score < 0:
        raise ValueError("Home score cannot be negative.")

    if not isinstance(away_score, int) or isinstance(away_score, bool):
        raise ValueError("Away score must be a whole number.")

    if away_score < 0:
        raise ValueError("Away score cannot be negative.")

    selected_fixture["home_score"] = home_score
    selected_fixture["away_score"] = away_score
    selected_fixture["status"] = "played"

    return selected_fixture
