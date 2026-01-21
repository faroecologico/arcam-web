import requests
import os
import time
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

def cleanup_empty_categories():
    print("------------------------------------------------")
    print("INICIANDO LIMPIEZA DE CATEGORÍAS VACÍAS")
    print("------------------------------------------------")
    
    page = 1
    empty_cats = []
    
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
                # No borrar "Sin categoría" ni categorías que tengan productos
                if c['count'] == 0 and c['slug'] != 'uncategorized' and c['name'].lower() != 'sin categoría':
                    empty_cats.append(c)
            
            page += 1
        except Exception as e:
            print(f"Error: {e}")
            break

    if not empty_cats:
        print("No se encontraron categorías vacías.")
        return

    print(f"Se encontraron {len(empty_cats)} categorías vacías.")
    
    for c in empty_cats:
        cid = c['id']
        name = c['name']
        print(f"   [-] Borrando: [{cid}] {name}...", flush=True)
        try:
            # force=true para borrar definitivamente
            url_del = f"{WOO_URL}/wp-json/wc/v3/products/categories/{cid}?force=true"
            r_del = requests.delete(url_del, headers=get_headers(), timeout=20)
            if r_del.status_code == 200:
                print(f"      [OK]")
            else:
                print(f"      [X] Error: {r_del.status_code}")
        except Exception as e:
            print(f"      [!] Excepción: {e}")
        time.sleep(0.2)

    print("------------------------------------------------")
    print("LIMPIEZA FINALIZADA")
    print("------------------------------------------------")

if __name__ == "__main__":
    cleanup_empty_categories()
