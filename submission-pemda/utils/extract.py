import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def scrape_fashion_data(base_url, max_pages=50):
    all_products = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        for page in range(1, max_pages + 1):
            if page == 1:
                url = base_url
            else:
                url = f"{base_url}/page{page}.html"
            
            print(f"--- [EXTRACT] Mengambil data dari: {url} ---")

            response = session.get(url, headers=headers, timeout=15)

            if response.status_code == 404:
                print(f"Peringatan: Halaman {page} tidak ditemukan (404). Melewati...")
                continue
                
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            cards = soup.find_all('div', class_='collection-card')
            
            if not cards:
                print(f"Peringatan: Tidak ada produk ditemukan di halaman {page}.")
                continue

            for card in cards:
                details = card.find('div', class_='product-details')
                if details:
                    title_tag = details.find('h3', class_='product-title')
                    title = title_tag.text.strip() if title_tag else "Unknown Product"
                    
                    price_tag = details.find(class_='price')
                    price = price_tag.text.strip() if price_tag else "Price Unavailable"
                    
                    paragraphs = details.find_all('p')
                    rating, colors, size, gender = "Invalid", "0", "Unknown", "Unknown"
                    for p in paragraphs:
                        txt = p.text.strip()
                        if "Rating:" in txt: rating = txt
                        elif "Colors" in txt: colors = txt
                        elif "Size:" in txt: size = txt
                        elif "Gender:" in txt: gender = txt

                    all_products.append({
                        "Title": title,
                        "Price": price,
                        "Rating": rating,
                        "Colors": colors,
                        "Size": size,
                        "Gender": gender,
                        "timestamp": current_time
                    })
            
            print(f"Berhasil mengambil {len(cards)} produk dari halaman {page}.")
            time.sleep(0.5)
        
        return pd.DataFrame(all_products)

    except Exception as e:
        print(f"Terjadi kesalahan fatal saat ekstraksi: {e}")
        return pd.DataFrame(all_products) if all_products else None