

from datetime import date, datetime,timedelta


def has_team_overlap(fixtures, selected_fixture, new_date, new_time):
    new_start = datetime.combine(
        new_date,
        datetime.strptime(new_time, "%H:%M").time()
    )

    new_end = new_start + timedelta(hours=2)

    selected_teams = {
        selected_fixture["home_id"],
        selected_fixture["away_id"]
    }

    for fixture in fixtures:
        if fixture["id"] == selected_fixture["id"]:
            continue

        if fixture["status"] == "postponed":
            continue

        if fixture["date"] != new_date.isoformat():
            continue

        existing_teams = {
            fixture["home_id"],
            fixture["away_id"]
        }

        if not selected_teams.intersection(existing_teams):
            continue

        existing_start = datetime.combine(
            new_date,
            datetime.strptime(
                fixture["kickoff_time"],
                "%H:%M"
            ).time()
        )

        existing_end = existing_start + timedelta(hours=2)

        if new_start < existing_end and existing_start < new_end:
            return True

    return False


def edit_fixture_schedule(fixtures, fixture_id, new_date, new_time):
    selected_fixture = None

    for fixture in fixtures:
        if fixture["id"] == fixture_id:
            selected_fixture = fixture
            break

    if selected_fixture is None:
        raise ValueError("Fixture not found.")

    if selected_fixture["status"] == "played":
        raise ValueError("A played fixture cannot be rescheduled.")

    if not isinstance(new_date, date) or isinstance(new_date, datetime):
        raise ValueError("Fixture date must be a valid date.")

    if new_date.weekday() not in (5, 6):
        raise ValueError("Fixtures must be scheduled on weekends.")

    if not isinstance(new_time, str):
        raise ValueError("Kickoff time must be text.")

    try:
        parsed_time = datetime.strptime(new_time, "%H:%M").time()
    except ValueError:
        raise ValueError("Kickoff time must use HH:MM format.")

    earliest_time = datetime.strptime("12:00", "%H:%M").time()
    latest_time = datetime.strptime("22:00", "%H:%M").time()

    if not earliest_time <= parsed_time <= latest_time:
        raise ValueError("Kickoff must be between 12:00 and 22:00.")

    if has_team_overlap(fixtures, selected_fixture, new_date, new_time):
       raise ValueError(
         "This team already has another match during that time."
    )

    selected_fixture["date"] = new_date.isoformat()
    selected_fixture["kickoff_time"] = new_time

    return selected_fixture
 
