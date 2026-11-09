
import unittest
from tournament.standings import calculate_standings


class TestStandings(unittest.TestCase):

    def setUp(self):
    
        self.teams = [
            {"id": "TM001", "name": "Iorniem United"},
            {"id": "TM002", "name": "Tersoo FC"},
            {"id": "TM003", "name": "Red Stars"}
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
                "away_score": 2
            },
            {
                "id": "M003",
                "home_id": "TM002",
                "away_id": "TM003",
                "status": "pending",
                "home_score": None,
                "away_score": None
            }
        ]

    def test_win_awards_three_points(self):
        standings = calculate_standings(self.teams, self.fixtures)

        team = next(
            item for item in standings
            if item["team_id"] == "TM001"
        )

        self.assertEqual(team["wins"], 1)
        self.assertEqual(team["points"], 4)

    def test_draw_awards_one_point_each(self):
        standings = calculate_standings(self.teams, self.fixtures)

        team = next(
            item for item in standings
            if item["team_id"] == "TM003"
        )

        self.assertEqual(team["draws"], 1)
        self.assertEqual(team["points"], 1)

    def test_pending_fixture_is_not_counted(self):
        standings = calculate_standings(self.teams, self.fixtures)

        team = next(
            item for item in standings
            if item["team_id"] == "TM002"
        )

        self.assertEqual(team["played"], 1)

    def test_goal_difference_is_calculated(self):
        standings = calculate_standings(self.teams, self.fixtures)

        team = next(
            item for item in standings
            if item["team_id"] == "TM001"
        )

        self.assertEqual(team["goals_for"], 5)
        self.assertEqual(team["goals_against"], 3)
        self.assertEqual(team["goal_difference"], 2)

    def test_loss_is_counted(self):
        standings = calculate_standings(self.teams, self.fixtures)

        team = next(
            item for item in standings
            if item["team_id"] == "TM002"
        )

        self.assertEqual(team["losses"], 1)
        self.assertEqual(team["points"], 0)


if __name__ == "__main__":
    unittest.main()
