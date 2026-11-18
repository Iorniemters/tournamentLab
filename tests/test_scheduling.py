

import unittest
from datetime import date

from tournament.fixtures import generate_fixtures
from tournament.scheduling import edit_fixture_schedule


class TestFixtureScheduling(unittest.TestCase):

    def setUp(self):
        self.teams = [
            {"id": "TM001", "name": "Iorniem United"},
            {"id": "TM002", "name": "Tersoo FC"},
            {"id": "TM003", "name": "God Favourites Stars"},
            {"id": "TM004", "name": "Holy Ghost"}
        ]

        self.fixtures = generate_fixtures(
            self.teams,
            date(2027, 1, 2)
        )

    def test_edit_fixture_date_and_time(self):
        updated = edit_fixture_schedule(
            self.fixtures,
            "M001",
            date(2027, 1, 3),
            "14:00"
        )

        self.assertEqual(updated["date"], "2027-01-03")
        self.assertEqual(updated["kickoff_time"], "14:00")

    def test_weekday_fixture_date_is_rejected(self):
        with self.assertRaises(ValueError):
            edit_fixture_schedule(
                self.fixtures,
                "M001",
                date(2027, 1, 4),
                "14:00"
            )

    def test_kickoff_before_noon_is_rejected(self):
        with self.assertRaises(ValueError):
            edit_fixture_schedule(
                self.fixtures,
                "M001",
                date(2027, 1, 3),
                "10:00"
            )

    def test_kickoff_after_10pm_is_rejected(self):
        with self.assertRaises(ValueError):
            edit_fixture_schedule(
                self.fixtures,
                "M001",
                date(2027, 1, 3),
                "22:30"
            )

    def test_unknown_fixture_is_rejected(self):
        with self.assertRaises(ValueError):
            edit_fixture_schedule(
                self.fixtures,
                "M999",
                date(2027, 1, 3),
                "14:00"
            )

    def test_invalid_schedule_change_leaves_fixture_unchanged(self):
       original_fixture = self.fixtures[0].copy()

       with self.assertRaises(ValueError):
          edit_fixture_schedule(
            self.fixtures,
            "M001",
            date(2027, 1, 4),
            "14:00"
        )

          self.assertEqual(
          self.fixtures[0],
          original_fixture
        )


    def test_same_team_cannot_play_overlapping_matches(self):
       fixtures = [
        {
            "id": "M001",
            "home_id": "TM001",
            "away_id": "TM002",
            "status": "pending",
            "date": "2027-01-02",
            "kickoff_time": "12:00",
            "home_score": None,
            "away_score": None
        },
        {
            "id": "M002",
            "home_id": "TM001",
            "away_id": "TM003",
            "status": "pending",
            "date": "2027-01-02",
            "kickoff_time": "16:00",
            "home_score": None,
            "away_score": None
        }
    ]

       with self.assertRaises(ValueError):
         edit_fixture_schedule(
            fixtures,
            "M002",
            date(2027, 1, 2),
            "13:00"
        )

    def test_same_team_can_play_when_previous_match_ends(self):
       fixtures = [
        {
            "id": "M001",
            "home_id": "TM001",
            "away_id": "TM002",
            "status": "pending",
            "date": "2027-01-02",
            "kickoff_time": "12:00",
            "home_score": None,
            "away_score": None
        },
        {
            "id": "M002",
            "home_id": "TM001",
            "away_id": "TM003",
            "status": "pending",
            "date": "2027-01-02",
            "kickoff_time": "16:00",
            "home_score": None,
            "away_score": None
        }
    ]

       updated = edit_fixture_schedule(
        fixtures,
        "M002",
        date(2027, 1, 2),
        "14:00"
    )

       self.assertEqual(updated["kickoff_time"], "14:00")


if __name__ == "__main__":
    unittest.main()
