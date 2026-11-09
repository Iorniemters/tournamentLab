
import unittest
import os
import json
import tempfile

from tournament.storage import save_tournament, load_tournament


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.teams = [
            {"id": "TM001", "name": "Iorniem United"},
            {"id": "TM002", "name": "Tersoo FC"}
        ]

        self.fixtures = [
            {
                "id": "M001",
                "home_id": "TM001",
                "away_id": "TM002",
                "status": "played",
                "home_score": 2,
                "away_score": 1
            }
        ]

    def test_save_tournament(self):
        with tempfile.TemporaryDirectory() as folder:
            filepath = os.path.join(folder, "tournament.json")

            save_tournament(self.teams, self.fixtures, filepath)

            with open(filepath, encoding="utf-8") as file:
                 print(file.read())
            

            self.assertTrue(os.path.exists(filepath))
       
    def test_load_tournament(self):
        with tempfile.TemporaryDirectory() as folder:
            filepath = os.path.join(folder, "tournament.json")

            save_tournament(self.teams, self.fixtures, filepath)

        
            loaded_data = load_tournament(filepath)

            self.assertEqual(loaded_data["teams"], self.teams)

            self.assertEqual(loaded_data["fixtures"], self.fixtures)

    def test_load_rejects_unsupported_version(self):
        with tempfile.TemporaryDirectory() as folder:
            filepath = os.path.join(folder, "tournament.json")

            invalid_data = {
                "schema_version": 99,
                "teams": [],
                "fixtures": []
            }

            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(invalid_data, file)

            with self.assertRaises(ValueError):
                load_tournament(filepath)   


if __name__ == "__main__":
    unittest.main()
