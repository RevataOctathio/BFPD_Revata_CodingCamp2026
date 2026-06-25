import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql

class TestLoad(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({"test": [1, 2, 3]})

    def test_load_to_csv(self):
        filename = "test_output.csv"

        result = load_to_csv(self.df, filename)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(filename))

        if os.path.exists(filename):
            os.remove(filename)

    # Mengetes Google Sheets menggunakan Mock
    @patch('utils.load.build')
    @patch('utils.load.service_account.Credentials.from_service_account_file')
    def test_load_to_google_sheets(self, mock_creds, mock_build):
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        result = load_to_google_sheets(self.df, "dummy_id", "dummy.json")
        self.assertTrue(result)

    # Mengetes PostgreSQL menggunakan Mock
    @patch('utils.load.create_engine')
    def test_load_to_postgresql(self, mock_engine):
        db_config = {'user': 'u', 'password': 'p', 'host': 'h', 'port': '5432', 'database': 'd'}
        result = load_to_postgresql(self.df, db_config)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()