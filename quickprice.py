import webbrowser
import urllib.parse

print("=" * 45)
print("QuickPrice — CEX + eBay UK (Sold Listings)")
print("=" * 45)
print("Narzędzie do szybkiego sprawdzania cen na rynku.\n")

while True:
    item = input("Wpisz nazwę rzeczy (lub 'q' = wyjście): ").strip()
    
    if item.lower() == "q":
        print("Do zobaczenia!")
        break
    
    if not item:
        continue

    q = urllib.parse.quote(item)

    # CEX UK
    webbrowser.open(f"https://uk.webuy.com/search?stext={q}")
    
    # eBay UK - aktualne oferty
    webbrowser.open(f"https://www.ebay.co.uk/sch/i.html?_nkw={q}&_sacat=0")
    
    # eBay UK - SPRZEDANE (najważniejsze!)
    webbrowser.open(f"https://www.ebay.co.uk/sch/i.html?_nkw={q}&LH_Sold=1&LH_Complete=1&_sop=13")

    print(f"✓ Otworzyłem CEX + eBay (w tym sprzedane) dla: {item}\n")