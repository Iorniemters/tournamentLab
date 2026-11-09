

import unittest

from tournament.results import record_result


class TestMatchResults(unittest.TestCase):

    def setUp(self):
        self.fixtures = [
            {
                "id": "M001",
                "home_id": "TM001",
                "away_id": "TM002",
                "status": "pending",
                "home_score": None,
                "away_score": None
            }
        ]

    def test_record_valid_result(self):
        fixture = record_result(
            self.fixtures, "M001", 2, 1
        )

        self.assertEqual(fixture["home_score"], 2)
        self.assertEqual(fixture["away_score"], 1)
        self.assertEqual(fixture["status"], "played")

    def test_negative_score_rejected(self):
        with self.assertRaises(ValueError):
            record_result(self.fixtures, "M001", -1, 2)

    def test_decimal_score_rejected(self):
        with self.assertRaises(ValueError):
            record_result(self.fixtures, "M001", 2.5, 1)

    def test_boolean_score_rejected(self):
        with self.assertRaises(ValueError):
            record_result(self.fixtures, "M001", True, 1)

    def test_unknown_fixture_rejected(self):
        with self.assertRaises(ValueError):
            record_result(self.fixtures, "M999", 2, 1)

    def test_result_cannot_be_edited(self):
        record_result(self.fixtures, "M001", 2, 1)

        with self.assertRaises(ValueError):
            record_result(self.fixtures, "M001", 3, 0)

    def test_invalid_score_does_not_change_fixture(self):
        original_fixture = self.fixtures[0].copy()

        with self.assertRaises(ValueError):
            record_result(self.fixtures, "M001", 2, -1)

        self.assertEqual(self.fixtures[0], original_fixture)


if __name__ == "__main__":
    unittest.main()
