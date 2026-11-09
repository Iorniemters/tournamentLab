

import unittest

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


if __name__ == "__main__":
    unittest.main()
