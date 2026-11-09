

def register_team(teams, name):
    if not isinstance(name, str):
        raise ValueError("Team name must be text.")

    name = name.strip()

    if len(name) < 2 or len(name) > 30:
        raise ValueError("Team name must be between 2 and 30 characters.")
    
    if len(teams) >= 8:
        raise ValueError("A tournament cannot have more than 8 teams.")

    for team in teams:
        if team["name"].casefold() == name.casefold():
            raise ValueError("This team name already exists.")

    team_id = f"TM{len(teams) + 1:03d}"

    new_team = {
        "id": team_id,
        "name": name
    }

    teams.append(new_team)

    return new_team
