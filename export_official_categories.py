import requests
import json
import os
import csv
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

def get_full_path(cat, all_cats_dict):
    path = [cat['name']]
    parent_id = cat['parent']
    while parent_id != 0:
        parent = all_cats_dict.get(parent_id)
        if parent:
            path.insert(0, parent['name'])
            parent_id = parent['parent']
        else:
            break
    return " > ".join(path)

def main():
    print("Obteniendo todas las categorías de WooCommerce...")
    page = 1
    all_cats = []
    
    while True:
        try:
            url = f"{WOO_URL}/wp-json/wc/v3/products/categories?per_page=100&page={page}"
            r = requests.get(url, headers=get_headers(), timeout=30)
            if r.status_code != 200:
                break
            cats = r.json()
            if not cats:
                break
            all_cats.extend(cats)
            page += 1
        except Exception as e:
            print(f"Error: {e}")
            break

    # Crear diccionario para búsqueda rápida
    all_cats_dict = {c['id']: c for c in all_cats}
    
    # Generar CSV con rutas completas
    outfile = "categorias_oficiales_arcam.csv"
    with open(outfile, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Nombre de Categoria', 'Ruta Completa', 'Productos Asociados'])
        
        for c in all_cats:
            if c['slug'] == 'uncategorized' or c['name'].lower() == 'sin categoría':
                continue
            
            full_path = get_full_path(c, all_cats_dict)
            writer.writerow([c['id'], c['name'], full_path, c['count']])

    print(f"Listo! Se han guardado {len(all_cats)} categorías en {outfile}")

if __name__ == "__main__":
    main()
