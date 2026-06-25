from utils.extract import scrape_fashion_data
from utils.transform import transform_products
from utils.load import load_to_csv, load_to_postgresql, load_to_google_sheets

def run_pipeline():
    BASE_URL = "https://fashion-studio.dicoding.dev"
    print("--- Memulai ETL Pipeline ---")
    
    # 1. Tahap Extract
    print("[1/3] Tahap Extract...")
    raw_data = scrape_fashion_data(BASE_URL, max_pages=50)
    
    if raw_data is not None and not raw_data.empty:
        print(f"Total data mentah terkumpul: {len(raw_data)} baris.")
        
        # 2. Tahap Transform
        print("\n[2/3] Tahap Transform...")
        clean_data = transform_products(raw_data)
        
        if clean_data is not None and not clean_data.empty:
            print(f"Data bersih siap diload: {len(clean_data)} baris.")
            
            # 3. Tahap Load
            print("\n[3/3] Tahap Load...")
            
            # A. Load CSV
            load_to_csv(clean_data, "products.csv")
            
            # B. Load PostgreSQL
            db_config = {
                'user': 'postgres', 
                'password': '1234', 
                'host': 'localhost', 
                'port': '5432', 
                'database': 'fashion_db'
            }
            load_to_postgresql(clean_data, db_config)
            
            # C. Load Google Sheets
            load_to_google_sheets(clean_data, "17ne8u3m098sKRdpFtJUncoAbe8LwM-Xq6i-p3vT2SI0", "google-sheets-api.json")
            
            print("\n=== Pipeline Selesai! ===")
        else:
            print("=== Pipeline terhenti: Data hasil transformasi kosong. ===")
    else:
        print("=== Pipeline terhenti: Gagal mengekstrak data mentah. ===")

if __name__ == "__main__":
    run_pipeline()