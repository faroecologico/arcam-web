import requests
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
    # ID de "Sin categoría" es 17 según vimos antes
    url = f"{WOO_URL}/wp-json/wc/v3/products?category=17&per_page=1"
    r = requests.get(url, headers=get_headers())
    if r.status_code == 200:
        count = r.headers.get('X-WP-Total')
        print(f"Productos restantes en 'Sin categoría': {count}")
    else:
        print("No se pudo verificar.")

if __name__ == "__main__":
    main()
