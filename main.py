
from tournament.teams import register_team

teams = []

team_names = [
    "Iorniem United",
    "Tersoo FC",
    "God Favourites Stars",
    "Holy Ghost",
    "Corner Stones",
    "The Saints",
    "Kenneth Warriors",
    "Red Stars"
]

for name in team_names:
    registered_team = register_team(teams, name)
    print(registered_team)
