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

    # Archivo de salida
    outfile = "productos_sin_categoria.csv"
    
    # Preparamos el CSV, field names
    fieldnames = ['id', 'name', 'status', 'categories', 'description', 'short_description', 'price', 'permalink']
    
    with open(outfile, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        page = 1
        found_count = 0
        total_checked = 0

        while True:
            try:
                print(f"Leyendo página {page}...")
                # Traemos 50 por página
                url = f"{WOO_URL}/wp-json/wc/v3/products?per_page=50&page={page}"
                r = requests.get(url, headers=get_headers(), timeout=30)
                
                if r.status_code != 200:
                    print(f"[X] Fin o Error en página {page} (Status {r.status_code}).")
                    break
                
                productos = r.json()
                if not productos:
                    print("[OK] No hay más productos.")
                    break
                    
                for p in productos:
                    total_checked += 1
                    cats = p.get('categories', [])
                    
                    # Criterio: Sin categorías o solo tiene "Sin categoría" / "Uncategorized"
                    is_uncategorized = False
                    
                    if not cats:
                        is_uncategorized = True
                    else:
                        # Revisamos si SOLO tiene la categoría por defecto
                        # A veces un producto puede estar en "Sin categoría" y en otra más.
                        # El usuario pide "aquellos productos sin categoría".
                        # Asumimos que si tiene AL MENOS UNA categoría válida (distinta de uncategorized), NO cuenta.
                        
                        valid_categories = []
                        for c in cats:
                            c_name = c['name'].lower()
                            # Ajustar estos nombres según lo que se vea en el sitio
                            if c_name not in ['sin categoría', 'uncategorized', 'sin categoria']:
                                valid_categories.append(c['name'])
                        
                        if not valid_categories:
                            is_uncategorized = True
                    
                    if is_uncategorized:
                        found_count += 1
                        print(f"   [!] Encontrado: [{p['id']}] {p['name']}")
                        
                        writer.writerow({
                            'id': p['id'],
                            'name': p['name'],
                            'status': p['status'],
                            'categories': " | ".join([c['name'] for c in cats]), # Para ver qué sale
                            'description': p['description'].replace('\n', ' ').replace('\r', ''),
                            'short_description': p['short_description'].replace('\n', ' ').replace('\r', ''),
                            'price': p['price'],
                            'permalink': p['permalink']
                        })

                page += 1
                
            except Exception as e:
                print(f"[!] Error en página {page}: {e}")
                time.sleep(5)

    print("\n------------------------------------------------")
    print(f"Finalizado. Se encontraron {found_count} productos sin categoría de {total_checked} revisados.")
    print(f"Guardado en: {outfile}")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()
