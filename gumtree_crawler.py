#!/usr/bin/env python3
"""
Prosty crawler do Gumtree (Irlandia Północna)
Szuka używanych konsol i kontrolerów
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-GB,en;q=0.9'
}

KEYWORDS = [
    'xbox', 'playstation', 'ps5', 'ps4', 'nintendo switch', 
    'controller', 'pad', 'konsola', 'console'
]

LOCATION = 'northern-ireland'


def search_gumtree():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Szukam ofert na Gumtree...\n")
    
    results = []
    
    for keyword in KEYWORDS:
        url = f"https://www.gumtree.com/search?search_category=video-games-consoles&search_location={LOCATION}&q={keyword}"
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                print(f"Błąd przy wyszukiwaniu: {keyword}")
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            listings = soup.find_all('div', class_='tileV2')  # może wymagać aktualizacji selektora
            
            for listing in listings[:15]:  # bierzemy pierwsze 15 wyników
                try:
                    title = listing.find('h2').get_text(strip=True) if listing.find('h2') else 'Brak tytułu'
                    price_tag = listing.find('span', class_='price')
                    price = price_tag.get_text(strip=True) if price_tag else 'Brak ceny'
                    link_tag = listing.find('a', href=True)
                    link = 'https://www.gumtree.com' + link_tag['href'] if link_tag else '#'
                    
                    results.append({
                        'title': title,
                        'price': price,
                        'link': link,
                        'keyword': keyword
                    })
                except:
                    continue
                    
            time.sleep(2)  # grzeczne opóźnienie
            
        except Exception as e:
            print(f"Błąd: {e}")
            continue
    
    # Usuwamy duplikaty
    seen = set()
    unique_results = []
    for r in results:
        if r['link'] not in seen:
            seen.add(r['link'])
            unique_results.append(r)
    
    # Sortujemy po cenie (jeśli da się wyciągnąć liczbę)
    def get_price_num(item):
        try:
            return float(''.join(filter(str.isdigit, item['price'])))
        except:
            return 999999
    
    unique_results.sort(key=get_price_num)
    
    print(f"Znaleziono {len(unique_results)} unikalnych ofert:\n")
    
    for item in unique_results[:30]:  # pokazujemy max 30 najtańszych
        print(f"{item['price']} | {item['title'][:70]}")
        print(f"Link: {item['link']}\n")


if __name__ == "__main__":
    print("Crawler Gumtree - Konsole i pady\n")
    search_gumtree()