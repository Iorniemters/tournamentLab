

import unittest
from tournament.reports import get_champion, get_mathematical_champion


class TestChampion(unittest.TestCase):

    def setUp(self):
        self.teams = [
            {"id": "TM001", "name": "Iorniem United"},
            {"id": "TM002", "name": "Tersoo FC"},
            {"id": "TM003", "name": "Red Stars"},
            {"id": "TM004", "name": "Holy Ghost"}
        ]

        self.fixtures = [
            {
                "id": "M001",
                "home_id": "TM001",
                "away_id": "TM002",
                "status": "played",
                "home_score": 3,
                "away_score": 1
            },
            {
                "id": "M002",
                "home_id": "TM001",
                "away_id": "TM003",
                "status": "played",
                "home_score": 2,
                "away_score": 0
            },
            {
                "id": "M003",
                "home_id": "TM001",
                "away_id": "TM004",
                "status": "played",
                "home_score": 1,
                "away_score": 0
            },
            {
                "id": "M004",
                "home_id": "TM002",
                "away_id": "TM003",
                "status": "played",
                "home_score": 2,
                "away_score": 1
            },
            {
                "id": "M005",
                "home_id": "TM002",
                "away_id": "TM004",
                "status": "played",
                "home_score": 1,
                "away_score": 1
            },
            {
                "id": "M006",
                "home_id": "TM003",
                "away_id": "TM004",
                "status": "pending",
                "home_score": None,
                "away_score": None
            }
        ]

    def test_no_champion_when_fixture_is_pending(self):
        champion = get_champion(self.teams, self.fixtures)
        self.assertIsNone(champion)
    def test_champion_when_all_fixtures_are_played(self):
    
        self.fixtures[5]["status"] = "played"
        self.fixtures[5]["home_score"] = 2
        self.fixtures[5]["away_score"] = 0

        champion = get_champion(self.teams, self.fixtures)

        self.assertEqual(champion["name"], "Iorniem United")
        self.assertEqual(champion["points"], 9)

    def test_mathematical_champion_when_rivals_cannot_catch_up(self):
        
        self.fixtures[0].update({
            "home_score": 3,
            "away_score": 0
        })

        self.fixtures[1].update({
            "home_score": 3,
            "away_score": 0
        })

        self.fixtures[2].update({
            "home_score": 3,
            "away_score": 0
        })
        for fixture in self.fixtures[3:]:
            fixture["status"] = "pending"
            fixture["home_score"] = None
            fixture["away_score"] = None

        champion = get_mathematical_champion(self.teams, self.fixtures)

        self.assertEqual(champion["name"], "Iorniem United")
        self.assertEqual(champion["points"], 9)

if __name__ == "__main__":
    unittest.main()
