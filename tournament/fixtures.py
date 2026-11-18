
from datetime import date, timedelta


def generate_fixtures(teams, start_date=None):

    if len(teams) not in (4, 6, 8):
        raise ValueError(
            "A tournament requires exactly 4, 6, or 8 teams."
        )

    if start_date is not None:
        if not isinstance(start_date, date):
            raise ValueError("Start date must be a valid date.")

        if start_date.weekday() != 5:
            raise ValueError("Tournament must start on a Saturday.")

    rotating_teams = list(teams)

    total_rounds = len(rotating_teams) - 1
    matches_per_round = len(rotating_teams) // 2

    fixtures = []
    fixture_number = 1

    for round_number in range(1, total_rounds + 1):

        round_start_date = None

        if start_date is not None:
            round_start_date = start_date + timedelta(
                days=(round_number - 1) * 7
            )

        for match_number in range(matches_per_round):

            home_team = rotating_teams[match_number]
            away_team = rotating_teams[-(match_number + 1)]

            fixture_date = None

            if start_date is not None:
                if match_number < 2:
                    fixture_date = round_start_date
                else:
                    fixture_date = round_start_date + timedelta(days=1)

            kickoff_times = ("12:00", "18:00")
            kickoff_time = kickoff_times[match_number % 2]    

            fixture = {
                "id": f"M{fixture_number:03d}",
                "round": round_number,
                "date": (
                    fixture_date.isoformat()
                    if fixture_date is not None
                    else None
                ),
                "kickoff_time": kickoff_time,
                "home_id": home_team["id"],
                "away_id": away_team["id"],
                "status": "pending",
                "home_score": None,
                "away_score": None
            }

            fixtures.append(fixture)
            fixture_number += 1

        rotating_teams = [
            rotating_teams[0],
            rotating_teams[-1],
            *rotating_teams[1:-1]
        ]

    return fixtures
