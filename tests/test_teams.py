

import unittest

from tournament.teams import register_team


class TestTeamRegistration(unittest.TestCase):

    def setUp(self):
        self.teams = []

    def test_register_valid_team(self):
        team = register_team(self.teams, "Iorniem United")

        self.assertEqual(team["id"], "TM001")
        self.assertEqual(team["name"], "Iorniem United")
        self.assertEqual(len(self.teams), 1)

    def test_duplicate_team_name(self):
        register_team(self.teams, "Iorniem United")

        with self.assertRaises(ValueError):
            register_team(self.teams, "IORNIEM UNITED")

    def test_invalid_short_name(self):
        with self.assertRaises(ValueError):
            register_team(self.teams, "A")

    def test_invalid_long_name(self):
        with self.assertRaises(ValueError):
            register_team(self.teams, "A" * 31)

    def test_ninth_team_rejected(self):
        for number in range(8):
            register_team(self.teams, f"Team {number + 1}")

        with self.assertRaises(ValueError):
            register_team(self.teams, "Team Nine")


if __name__ == "__main__":
    unittest.main()
