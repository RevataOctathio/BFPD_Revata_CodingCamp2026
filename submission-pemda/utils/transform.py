import pandas as pd
import numpy as np

def transform_products(df):
    if df is None or df.empty:
        return None

    try:
        subset_cols = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender']
        df = df.drop_duplicates(subset=subset_cols).copy()

        df = df[df['Title'] != 'Unknown Product']

        df['Price'] = df['Price'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False)
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        df = df.dropna(subset=['Price'])
        df['Price'] = (df['Price'] * 16000).astype(float)

        df['Rating'] = df['Rating'].astype(str).str.extract(r'(\d+\.\d+|\d+)')
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        df = df.dropna(subset=['Rating'])

        df['Colors'] = df['Colors'].astype(str).str.extract(r'(\d+)').astype(float)
        df = df.dropna(subset=['Colors'])
        df['Colors'] = df['Colors'].astype(int)

        df['Size'] = df['Size'].astype(str).str.replace(r'^Size:\s*', '', regex=True)
        df['Gender'] = df['Gender'].astype(str).str.replace(r'^Gender:\s*', '', regex=True)

        df = df.reset_index(drop=True)
        
        return df
        
    except Exception as e:
        print(f"Error Transform: {e}")
        return None