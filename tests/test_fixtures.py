

import unittest
from datetime import date

from tournament.fixtures import generate_fixtures


class TestFixtureGeneration(unittest.TestCase):

    def setUp(self):
        self.teams = [
            {"id": "TM001", "name": "Iorniem United"},
            {"id": "TM002", "name": "Tersoo FC"},
            {"id": "TM003", "name": "God Favourites Stars"},
            {"id": "TM004", "name": "Holy Ghost"},
            {"id": "TM005", "name": "Corner Stones"},
            {"id": "TM006", "name": "The Saints"},
            {"id": "TM007", "name": "Kenneth Warriors"},
            {"id": "TM008", "name": "Red Stars"}
        ]

    def test_eight_teams_generate_28_fixtures(self):
        fixtures = generate_fixtures(self.teams)
        self.assertEqual(len(fixtures), 28)

    def test_fixture_ids_are_unique(self):
        fixtures = generate_fixtures(self.teams)
        fixture_ids = [fixture["id"] for fixture in fixtures]

        self.assertEqual(len(fixture_ids), len(set(fixture_ids)))

    def test_no_team_plays_itself(self):
        fixtures = generate_fixtures(self.teams)

        for fixture in fixtures:
            self.assertNotEqual(
                fixture["home_id"],
                fixture["away_id"]
            )

    def test_four_teams_generate_six_fixtures(self):
        fixtures = generate_fixtures(self.teams[:4])
        self.assertEqual(len(fixtures), 6)

    def test_less_than_four_teams_rejected(self):
        with self.assertRaises(ValueError):
            generate_fixtures(self.teams[:3])
            
    def test_no_duplicate_team_pairings(self):
        fixtures = generate_fixtures(self.teams)

        pairings = []

        for fixture in fixtures:
            pair = frozenset([
                fixture["home_id"],
                fixture["away_id"]
            ])

            pairings.append(pair)

        self.assertEqual(len(pairings), len(set(pairings))) 


         
    def test_eight_teams_generate_seven_rounds(self):
        fixtures = generate_fixtures(self.teams)

        rounds = {fixture["round"] for fixture in fixtures}

        self.assertEqual(len(rounds), 7)

    def test_each_round_has_four_matches(self):
        fixtures = generate_fixtures(self.teams)

        for round_number in range(1, 8):
            round_fixtures = [
                fixture for fixture in fixtures
                if fixture["round"] == round_number
            ]

            self.assertEqual(len(round_fixtures), 4)

    def test_no_team_plays_twice_in_same_round(self):
        fixtures = generate_fixtures(self.teams)

        for round_number in range(1, 8):
            round_fixtures = [
                fixture for fixture in fixtures
                if fixture["round"] == round_number
            ]

            participating_teams = []

            for fixture in round_fixtures:
                participating_teams.append(fixture["home_id"])
                participating_teams.append(fixture["away_id"])

            self.assertEqual(
                len(participating_teams),
                len(set(participating_teams))
            )
            
    def test_six_teams_generate_15_fixtures(self):
       fixtures = generate_fixtures(self.teams[:6])
       self.assertEqual(len(fixtures), 15)


    def test_five_teams_are_rejected(self):
      with self.assertRaises(ValueError):
        generate_fixtures(self.teams[:5])


    def test_seven_teams_are_rejected(self):
      with self.assertRaises(ValueError):
        generate_fixtures(self.teams[:7])

    def test_fixture_dates_are_on_weekends(self):
        fixtures = generate_fixtures(
            self.teams[:4],
            date(2027, 1, 2)
        )

        for fixture in fixtures:
            fixture_date = date.fromisoformat(fixture["date"])

            self.assertIn(fixture_date.weekday(), (5, 6))

    def test_each_round_is_seven_days_apart(self):
        fixtures = generate_fixtures(
            self.teams[:4],
            date(2027, 1, 2)
        )

        round_dates = {}

        for fixture in fixtures:
            round_number = fixture["round"]
            fixture_date = date.fromisoformat(fixture["date"])

            round_dates[round_number] = fixture_date

        self.assertEqual(
            (round_dates[2] - round_dates[1]).days,
            7
        )

    def test_non_saturday_start_date_is_rejected(self):
        with self.assertRaises(ValueError):
            generate_fixtures(
                self.teams[:4],
                date(2027, 1, 3)
            )

    def test_every_fixture_has_a_kickoff_time(self):
        fixtures = generate_fixtures(
            self.teams,
            date(2027, 1, 2)
        )

        for fixture in fixtures:
            self.assertIn("kickoff_time", fixture)

    def test_kickoff_times_are_between_noon_and_10pm(self):
        fixtures = generate_fixtures(
            self.teams,
            date(2027, 1, 2)
        )

        for fixture in fixtures:
            kickoff_time = fixture["kickoff_time"]

            self.assertIn(
                kickoff_time,
                ("12:00", "18:00")
            )
            
    def test_eight_team_round_uses_both_weekend_days(self):
        fixtures = generate_fixtures(
            self.teams,
            date(2027, 1, 2)
        )

        first_round_dates = {
            fixture["date"]
            for fixture in fixtures
            if fixture["round"] == 1
        }

        self.assertEqual(
            len(first_round_dates),
            2
        )       
    


if __name__ == "__main__":
    unittest.main()
