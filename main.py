
from tournament.teams import register_team
from tournament.fixtures import generate_fixtures
from tournament.storage import save_tournament, load_tournament
from tournament.results import record_result
from tournament.standings import calculate_standings
from tournament.reports import get_champion

teams = []
fixtures = []
FILE_PATH = "data/tournament.json"

try:
    loaded_data = load_tournament(FILE_PATH)

    teams = loaded_data["teams"]
    fixtures = loaded_data["fixtures"]

    print("\nPrevious tournament loaded successfully!")
    print(f"Teams restored: {len(teams)}")
    print(f"Fixtures restored: {len(fixtures)}")

except FileNotFoundError:
    print("\nNo previous tournament found. Starting a new tournament.")

except (ValueError, OSError) as error:
    print(f"\nCould not load previous tournament: {error}")

def show_menu():
    print("\n===== TOURNAMENTLAB =====")
    print("1. Register Team")
    print("2. View Teams")
    print("3. Generate Fixtures")
    print("4. View Fixtures")
    print("5. Record Match Result")
    print("6. View Standings")
    print("7. Show Champion")
    print("8. Save Tournament")
    print("9. Load Tournament")
    print("0. Exit")

while True:
   show_menu()

   choice = input("Enter your choice")
   choice = choice.strip()

   if choice == "0":
        print("Thank you for using TournamentLab!")
        break

   elif choice == "1":
      if fixtures:
        print("\nTeam registration is locked.")
        print("Fixtures have already been generated.")
        print("You cannot add teams to an active tournament.")
        
      else:
        name = input("Enter team name: ")


   
   
      try:
        registered_team = register_team(teams, name)
        print("Team registered successfully!")
        print(f"Team ID: {registered_team['id']}")
        print(f"Team Name: {registered_team['name']}")

      except ValueError as error:
        print("Registration failed:", error)

   
   elif choice == "2":
        if not teams:
           print("No teams have been register yet.")
        else:
            print("\n======== REGISTER TEAMS========")

            for team in teams:
                print(f'{team["id"]} - {team["name"]}')
        

   elif choice == "3":
        try:
            if fixtures:
                print("Fixtures have already been generated.")
            else:
                fixtures = generate_fixtures(teams)
                print("Fixtures generated successfully!")

                save_tournament(teams, fixtures, FILE_PATH)
                print("Tournament saved to JSON successfully!")

            print("\n===== TOURNAMENT FIXTURES =====")

            for fixture in fixtures:
                home_team = next(
                    team for team in teams
                    if team["id"] == fixture["home_id"]
                )

                away_team = next(
                    team for team in teams
                    if team["id"] == fixture["away_id"]
                )

                print(
                    f'{fixture["id"]}: '
                    f'{home_team["name"]} vs {away_team["name"]}'
                )

            print(f"\nTotal fixtures: {len(fixtures)}")

        except ValueError as error:
            print("Fixture generation failed:", error)
            

   elif choice == "4":
        if not fixtures:
            print("No fixtures available. Please generate fixtures first.")
            print("Generating another schedule is not allowed.")
            print("Your existing fixtures and match results are protected.")

        else:
            print("\n===== TOURNAMENT FIXTURES =====")

            for fixture in fixtures:
                home_team = next(
                    team for team in teams
                    if team["id"] == fixture["home_id"]
                )

                away_team = next(
                    team for team in teams
                    if team["id"] == fixture["away_id"]
                )

                print(
                    f'{fixture["id"]}: '
                    f'{home_team["name"]} vs {away_team["name"]} '
                    f'[{fixture["status"].upper()}]'
                )

            print(f"\nTotal fixtures: {len(fixtures)}")

   elif choice == "5":
        if not fixtures:
            print("No fixtures available. Please generate fixtures first.")

        else:
            fixture_id = input("Enter fixture ID: ").strip()

            try:
                home_score = int(input("Enter home team score: "))
                away_score = int(input("Enter away team score: "))

                recorded_fixture = record_result(
                    fixtures,
                    fixture_id,
                    home_score,
                    away_score
                )

                save_tournament(teams, fixtures, FILE_PATH)

                print("\nMatch result recorded successfully!")

                home_team = next(
                    team for team in teams
                    if team["id"] == recorded_fixture["home_id"]
                )

                away_team = next(
                    team for team in teams
                    if team["id"] == recorded_fixture["away_id"]
                )

                print(
                  f'{recorded_fixture["id"]}: '
                  f'{home_team["name"]} '
                  f'{recorded_fixture["home_score"]} - '
                  f'{recorded_fixture["away_score"]} '
                  f'{away_team["name"]}'
)
                print("Updated tournament saved to JSON.")
            except ValueError as error:
            
                print("Could not record result:", error)

            except OSError as error:
            
                print("Could not save tournament:", error)

   elif choice == "6":
        if not fixtures:
            print("No fixtures available. Please generate fixtures first.")

        else:
            standings = calculate_standings(teams, fixtures)

            team_names = {
                team["id"]: team["name"]
                for team in teams
            }

            print("\n================ TOURNAMENT STANDINGS ================")

            print(
                f'{"POS":<5}'
                f'{"TEAM":<24}'
                f'{"P":<5}'
                f'{"W":<5}'
                f'{"D":<5}'
                f'{"L":<5}'
                f'{"GF":<5}'
                f'{"GA":<5}'
                f'{"GD":<6}'
                f'{"PTS":<5}'
            )

            print("-" * 79)

            for position, team in enumerate(standings, start=1):
                team_name = team_names[team["team_id"]]

                print(
                    f'{position:<5}'
                    f'{team_name:<24}'
                    f'{team["played"]:<5}'
                    f'{team["wins"]:<5}'
                    f'{team["draws"]:<5}'
                    f'{team["losses"]:<5}'
                    f'{team["goals_for"]:<5}'
                    f'{team["goals_against"]:<5}'
                    f'{team["goal_difference"]:<6}'
                    f'{team["points"]:<5}'
                )

  
    
   elif choice == "7":
        if not fixtures:
            print("No fixtures available. Please generate fixtures first.")

        else:
            champion = get_champion(teams, fixtures)

            if champion is None:
                pending_matches = sum(
                    1 for fixture in fixtures
                    if fixture["status"] == "pending"
                )

                print("\nThe tournament is not yet complete.")
                print(f"Matches remaining: {pending_matches}")
                print("A champion cannot be declared yet.")

            else:
                print("\n========== TOURNAMENT CHAMPION ==========")
                print(f'Champion: {champion["name"]}')
                print(f'Team ID: {champion["team_id"]}')
                print(f'Points: {champion["points"]}')
                print("Congratulations to the champions!")

   elif choice == "8":
    try:
        save_tournament(teams, fixtures, FILE_PATH)

        print("\nTournament saved successfully!")
        print(f"Teams saved: {len(teams)}")
        print(f"Fixtures saved: {len(fixtures)}")
        print(f"File location: {FILE_PATH}")

    except (ValueError, OSError) as error:
        print(f"Could not save tournament: {error}")

   elif choice == "9":
     try:
        loaded_data = load_tournament(FILE_PATH)

        teams = loaded_data["teams"]
        fixtures = loaded_data["fixtures"]

        print("\nTournament loaded successfully!")
        print(f"Teams loaded: {len(teams)}")
        print(f"Fixtures loaded: {len(fixtures)}")
        print(f"File location: {FILE_PATH}")

     except (ValueError, OSError) as error:
        print(f"Could not load tournament: {error}")
   else:

       print("Ivalid choice. Please try again.")