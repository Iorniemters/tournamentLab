
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


    def test_load_rejects_non_dictionary_data(self):
        with tempfile.TemporaryDirectory() as folder:
            filepath = os.path.join(folder, "tournament.json")

            with open(filepath, "w", encoding="utf-8") as file:
                json.dump([], file)

            with self.assertRaises(ValueError):
                load_tournament(filepath)

    def test_load_rejects_missing_teams(self):
        with tempfile.TemporaryDirectory() as folder:
            filepath = os.path.join(folder, "tournament.json")

            invalid_data = {
                "schema_version": 1,
                "fixtures": []
            }

            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(invalid_data, file)

            with self.assertRaises(ValueError):
                load_tournament(filepath)

    def test_load_rejects_boolean_schema_version(self):
        with tempfile.TemporaryDirectory() as folder:
            filepath = os.path.join(folder, "tournament.json")

            invalid_data = {
                "schema_version": True,
                "teams": [],
                "fixtures": []
            }

            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(invalid_data, file)

            with self.assertRaises(ValueError):
                load_tournament(filepath)

                
    def test_load_rejects_duplicate_team_ids(self):
        with tempfile.TemporaryDirectory() as folder:
            filepath = os.path.join(folder, "tournament.json")

            invalid_data = {
                "schema_version": 1,
                "teams": [
                    {"id": "TM001", "name": "Iorniem United"},
                    {"id": "TM001", "name": "Tersoo FC"}
                ],
                "fixtures": []
            }

            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(invalid_data, file)

            with self.assertRaises(ValueError):
                load_tournament(filepath)

    def test_load_rejects_duplicate_team_names(self):
        with tempfile.TemporaryDirectory() as folder:
            filepath = os.path.join(folder, "tournament.json")

            invalid_data = {
                "schema_version": 1,
                "teams": [
                    {"id": "TM001", "name": "Iorniem United"},
                    {"id": "TM002", "name": "IORNIEM UNITED"}
                ],
                "fixtures": []
            }

            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(invalid_data, file)

            with self.assertRaises(ValueError):
                load_tournament(filepath)

                
    def test_load_rejects_unknown_team_in_fixture(self):
        with tempfile.TemporaryDirectory() as folder:
            filepath = os.path.join(folder, "tournament.json")

            invalid_data = {
                "schema_version": 1,
                "teams": self.teams,
                "fixtures": [
                    {
                        "id": "M001",
                        "home_id": "TM001",
                        "away_id": "TM999",
                        "status": "pending",
                        "home_score": None,
                        "away_score": None
                    }
                ]
            }

            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(invalid_data, file)

            with self.assertRaises(ValueError):
                load_tournament(filepath)

    def test_load_rejects_team_playing_itself(self):
        with tempfile.TemporaryDirectory() as folder:
            filepath = os.path.join(folder, "tournament.json")

            invalid_data = {
                "schema_version": 1,
                "teams": self.teams,
                "fixtures": [
                    {
                        "id": "M001",
                        "home_id": "TM001",
                        "away_id": "TM001",
                        "status": "pending",
                        "home_score": None,
                        "away_score": None
                    }
                ]
            }

            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(invalid_data, file)

            with self.assertRaises(ValueError):
                load_tournament(filepath)

    def test_load_rejects_duplicate_pairings(self):
        with tempfile.TemporaryDirectory() as folder:
            filepath = os.path.join(folder, "tournament.json")

            invalid_data = {
                "schema_version": 1,
                "teams": self.teams,
                "fixtures": [
                    {
                        "id": "M001",
                        "home_id": "TM001",
                        "away_id": "TM002",
                        "status": "pending",
                        "home_score": None,
                        "away_score": None
                    },
                    {
                        "id": "M002",
                        "home_id": "TM002",
                        "away_id": "TM001",
                        "status": "pending",
                        "home_score": None,
                        "away_score": None
                    }
                ]
            }

            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(invalid_data, file)

            with self.assertRaises(ValueError):
                load_tournament(filepath)

    def test_load_rejects_negative_scores(self):
        with tempfile.TemporaryDirectory() as folder:
            filepath = os.path.join(folder, "tournament.json")

            invalid_data = {
                "schema_version": 1,
                "teams": self.teams,
                "fixtures": [
                    {
                        "id": "M001",
                        "home_id": "TM001",
                        "away_id": "TM002",
                        "status": "played",
                        "home_score": -1,
                        "away_score": 2
                    }
                ]
            }

            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(invalid_data, file)

            with self.assertRaises(ValueError):
                load_tournament(filepath)

                
    def test_load_rejects_duplicate_fixture_ids(self):
     with tempfile.TemporaryDirectory() as folder:
        filepath = os.path.join(folder, "tournament.json")

        invalid_data = {
            "schema_version": 1,
            "teams": self.teams,
            "fixtures": [
                {
                    "id": "M001",
                    "home_id": "TM001",
                    "away_id": "TM002",
                    "status": "pending",
                    "home_score": None,
                    "away_score": None
                },
                {
                    "id": "M001",
                    "home_id": "TM002",
                    "away_id": "TM001",
                    "status": "pending",
                    "home_score": None,
                    "away_score": None
                }
            ]
        }

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(invalid_data, file)

        with self.assertRaises(ValueError):
            load_tournament(filepath)

            
    def test_load_rejects_invalid_fixture_status(self):
      with tempfile.TemporaryDirectory() as folder:
        filepath = os.path.join(folder, "tournament.json")

        invalid_data = {
            "schema_version": 1,
            "teams": self.teams,
            "fixtures": [
                {
                    "id": "M001",
                    "home_id": "TM001",
                    "away_id": "TM002",
                    "status": "cancelled",
                    "home_score": None,
                    "away_score": None
                }
            ]
        }

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(invalid_data, file)

        with self.assertRaises(ValueError):
            load_tournament(filepath)

            
    def test_load_rejects_boolean_scores(self):
       with tempfile.TemporaryDirectory() as folder:
         filepath = os.path.join(folder, "tournament.json")

         invalid_data = {
            "schema_version": 1,
            "teams": self.teams,
            "fixtures": [
                {
                    "id": "M001",
                    "home_id": "TM001",
                    "away_id": "TM002",
                    "status": "played",
                    "home_score": True,
                    "away_score": 2
                }
            ]
        }

         with open(filepath, "w", encoding="utf-8") as file:
            json.dump(invalid_data, file)

         with self.assertRaises(ValueError):
            load_tournament(filepath)

            
    def test_load_rejects_decimal_scores(self):
      with tempfile.TemporaryDirectory() as folder:
        filepath = os.path.join(folder, "tournament.json")

        invalid_data = {
            "schema_version": 1,
            "teams": self.teams,
            "fixtures": [
                {
                    "id": "M001",
                    "home_id": "TM001",
                    "away_id": "TM002",
                    "status": "played",
                    "home_score": 2.5,
                    "away_score": 1
                }
            ]
        }

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(invalid_data, file)

        with self.assertRaises(ValueError):
            load_tournament(filepath)

            
    def test_load_rejects_played_fixture_with_missing_score(self):
      with tempfile.TemporaryDirectory() as folder:
        filepath = os.path.join(folder, "tournament.json")

        invalid_data = {
            "schema_version": 1,
            "teams": self.teams,
            "fixtures": [
                {
                    "id": "M001",
                    "home_id": "TM001",
                    "away_id": "TM002",
                    "status": "played",
                    "home_score": None,
                    "away_score": 2
                }
            ]
        }

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(invalid_data, file)

        with self.assertRaises(ValueError):
            load_tournament(filepath)

    def test_load_rejects_team_id_with_surrounding_spaces(self):
        self.teams[0]["id"] = " TM001 "

        with tempfile.TemporaryDirectory() as folder:
            filepath = os.path.join(folder, "tournament.json")
            save_data = {
                "schema_version": 1,
                "teams": self.teams,
                "fixtures": self.fixtures
            }

            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(save_data, file)

            with self.assertRaises(ValueError):
                load_tournament(filepath)

    def test_load_rejects_fixture_id_with_surrounding_spaces(self):
        self.fixtures[0]["id"] = " M001 "

        with tempfile.TemporaryDirectory() as folder:
            filepath = os.path.join(folder, "tournament.json")
            save_data = {
                "schema_version": 1,
                "teams": self.teams,
                "fixtures": self.fixtures
            }

            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(save_data, file)

            with self.assertRaises(ValueError):
                load_tournament(filepath)

    def test_load_rejects_non_text_team_ids_in_fixtures(self):
        self.fixtures[0]["home_id"] = ["TM001"]

        with tempfile.TemporaryDirectory() as folder:
            filepath = os.path.join(folder, "tournament.json")
            save_data = {
                "schema_version": 1,
                "teams": self.teams,
                "fixtures": self.fixtures
            }

            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(save_data, file)

            with self.assertRaises(ValueError):
                load_tournament(filepath)

    def test_save_rejects_invalid_fixtures(self):
        invalid_fixtures = [
            {
                "id": "M001",
                "home_id": "TM001",
                "away_id": "TM999",
                "status": "played",
                "home_score": 2,
                "away_score": 1
            }
        ]

        with tempfile.TemporaryDirectory() as folder:
            filepath = os.path.join(folder, "tournament.json")

            with self.assertRaises(ValueError):
                save_tournament(self.teams, invalid_fixtures, filepath)









if __name__ == "__main__":
    unittest.main()
