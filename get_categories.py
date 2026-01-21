import requests
import json
import os
from dotenv import load_dotenv
from base64 import b64encode

load_dotenv()

WOO_URL = os.getenv("WOO_URL")
WOO_KEY = os.getenv("WOO_KEY")
WOO_SECRET = os.getenv("WOO_SECRET")

def get_headers():
    credentials = f"{WOO_KEY}:{WOO_SECRET}"
    token = b64encode(credentials.encode()).decode("utf-8")
    return { "Authorization": f"Basic {token}", "Content-Type": "application/json" }

def main():
    print("Getting categories...")
    page = 1
    all_cats = []
    
    with open("lista_categorias.txt", "w", encoding="utf-8") as f:
        while True:
            try:
                url = f"{WOO_URL}/wp-json/wc/v3/products/categories?per_page=100&page={page}"
                r = requests.get(url, headers=get_headers(), timeout=30)
                
                if r.status_code != 200:
                    break
                
                cats = r.json()
                if not cats:
                    break
                
                for c in cats:
                    # Format: ID - Name (Parent ID)
                    line = f"{c['id']} - {c['name']} (Parent: {c['parent']})"
                    print(line)
                    f.write(line + "\n")
                    all_cats.append(c)
                
                page += 1
            except Exception as e:
                print(e)
                break
                
    print(f"Total categories: {len(all_cats)}")

if __name__ == "__main__":
    main()
