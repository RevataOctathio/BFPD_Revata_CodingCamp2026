import unittest
import pandas as pd
from utils.transform import transform_products

class TestTransform(unittest.TestCase):
    def setUp(self):
        # Menyiapkan data dummy yang "kotor" untuk dites
        self.raw_data = pd.DataFrame({
            "Title": ["Kemeja Keren", "Unknown Product", "Kaos Bagus"],
            "Price": ["$10.00", "$5.00", "Price Unavailable"],
            "Rating": ["4.5 / 5", "3.0 / 5", "Invalid"],
            "Colors": ["3 Colors", "1 Color", "0"],
            "Size": ["Size: M", "Size: L", "Size: XL"],
            "Gender": ["Gender: Men", "Gender: Women", "Gender: Unisex"]
        })

    def test_transformation_logic(self):
        clean_df = transform_products(self.raw_data)
        self.assertNotIn("Unknown Product", clean_df['Title'].values)
        self.assertEqual(clean_df.iloc[0]['Price'], 160000.0)
        self.assertEqual(clean_df.iloc[0]['Size'], "M")
        
    def test_transform_empty_or_none(self):
        # Menguji jika dataframe None (untuk trigger error handling)
        self.assertIsNone(transform_products(None))
        # Menguji jika dataframe kosong
        empty_df = pd.DataFrame()
        self.assertIsNone(transform_products(empty_df))

if __name__ == "__main__":
    unittest.main()