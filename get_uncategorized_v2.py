import requests
import json
import time
import os
import csv
from dotenv import load_dotenv
from base64 import b64encode

load_dotenv()

# --- CREDENCIALES ---
WOO_URL = os.getenv("WOO_URL")
WOO_KEY = os.getenv("WOO_KEY")
WOO_SECRET = os.getenv("WOO_SECRET")

def get_headers():
    credentials = f"{WOO_KEY}:{WOO_SECRET}"
    token = b64encode(credentials.encode()).decode("utf-8")
    return { "Authorization": f"Basic {token}", "Content-Type": "application/json" }

def main():
    print("------------------------------------------------")
    print("*** BUSCANDO PRODUCTOS SIN CATEGORÍA ***")
    print("------------------------------------------------")
    print(f"URL: {WOO_URL}")

    # Primero obtenemos el ID de "Sin categoría"
    cat_id = None
    try:
        url = f"{WOO_URL}/wp-json/wc/v3/products/categories?slug=sin-categoria"
        r = requests.get(url, headers=get_headers(), timeout=30)
        if r.status_code == 200:
            cats = r.json()
            if cats:
                cat_id = cats[0]['id']
                print(f"ID de 'Sin categoría': {cat_id}")
    except Exception as e:
        print(f"Error obteniendo categoría: {e}")

    if not cat_id:
        # Intenta con 'uncategorized'
        try:
            url = f"{WOO_URL}/wp-json/wc/v3/products/categories?slug=uncategorized"
            r = requests.get(url, headers=get_headers(), timeout=30)
            if r.status_code == 200:
                cats = r.json()
                if cats:
                    cat_id = cats[0]['id']
                    print(f"ID de 'Uncategorized': {cat_id}")
        except Exception as e:
            print(f"Error: {e}")

    if not cat_id:
        print("No se encontró la categoría 'Sin categoría'. Buscando manualmente...")
        cat_id = 17  # ID por defecto según lista

    # Archivo de salida
    outfile = "productos_sin_categoria.csv"
    
    fieldnames = ['id', 'name', 'sku', 'status', 'price', 'short_description', 'permalink']
    
    with open(outfile, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        page = 1
        found_count = 0

        while True:
            try:
                print(f"Leyendo página {page}...", flush=True)
                # Filtramos directamente por la categoría
                url = f"{WOO_URL}/wp-json/wc/v3/products?category={cat_id}&per_page=100&page={page}"
                r = requests.get(url, headers=get_headers(), timeout=60)
                
                if r.status_code != 200:
                    print(f"[X] Status {r.status_code}")
                    break
                
                productos = r.json()
                if not productos:
                    print("[OK] No hay más productos.")
                    break
                
                print(f"   Encontrados {len(productos)} en esta página", flush=True)
                    
                for p in productos:
                    found_count += 1
                    
                    # Clean description
                    short_desc = p.get('short_description', '')
                    if short_desc:
                        short_desc = short_desc.replace('\n', ' ').replace('\r', '').replace('<p>', '').replace('</p>', '').strip()
                    
                    writer.writerow({
                        'id': p['id'],
                        'name': p['name'],
                        'sku': p.get('sku', ''),
                        'status': p['status'],
                        'price': p.get('price', ''),
                        'short_description': short_desc[:200] if short_desc else '',
                        'permalink': p.get('permalink', '')
                    })
                    
                    print(f"   [{p['id']}] {p['name'][:50]}...", flush=True)

                page += 1
                
            except Exception as e:
                print(f"[!] Error en página {page}: {e}")
                time.sleep(3)
                break

    print("\n------------------------------------------------")
    print(f"Finalizado. Se encontraron {found_count} productos sin categoría.")
    print(f"Guardado en: {outfile}")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()
