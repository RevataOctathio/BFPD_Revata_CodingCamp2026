import unittest
from unittest.mock import patch, Mock
import pandas as pd
from utils.extract import scrape_fashion_data

class TestExtract(unittest.TestCase):
    @patch("utils.extract.requests.Session")
    def test_scrape_success(self, mock_session):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'''
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">Kaos Test</h3>
                <p class="price">$10.00</p>
                <p>Rating: 4.0 / 5</p>
                <p>2 Colors</p>
                <p>Size: L</p>
                <p>Gender: Men</p>
            </div>
        </div>
        '''
        mock_session.return_value.get.return_value = mock_response
        
        df = scrape_fashion_data("http://fakeurl.com", max_pages=1)
        
        self.assertIsNotNone(df)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['Title'], "Kaos Test")

    @patch("utils.extract.requests.Session")
    def test_scrape_fail(self, mock_session):
        mock_session.return_value.get.side_effect = Exception("Connection Error")
        df = scrape_fashion_data("http://fakeurl.com", max_pages=1)
        self.assertIsNone(df)

if __name__ == '__main__':
    unittest.main()