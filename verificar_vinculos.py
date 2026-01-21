import requests
import json
import random
import os
from dotenv import load_dotenv
from base64 import b64encode

load_dotenv()

# --- CREDENCIALES ---
WOO_URL = os.getenv("WOO_URL")
WOO_KEY = os.getenv("WOO_KEY")
WOO_SECRET = os.getenv("WOO_SECRET")

CLAVE_PLUGIN = os.getenv("CLAVE_PLUGIN")
ARCHIVO_JSON = os.getenv("ARCHIVO_JSON")

def get_headers():
    credentials = f"{WOO_KEY}:{WOO_SECRET}"
    token = b64encode(credentials.encode()).decode("utf-8")
    return { "Authorization": f"Basic {token}", "Content-Type": "application/json" }

def get_product_by_sku(sku):
    try:
        url = f"{WOO_URL}/wp-json/wc/v3/products?sku={sku}"
        r = requests.get(url, headers=get_headers(), timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data:
                return data[0]
    except Exception as e:
        print(f"Error consultando SKU {sku}: {e}")
    return None

def check_family(nombre, skus):
    print(f"\n[?] Verificando familia: '{nombre}'")
    print(f"   SKUs esperados: {skus}")
    
    products_data = {}
    found_ids = []
    
    # 1. Obtener datos de cada SKU (ID y Metadatos)
    for sku in skus:
        p = get_product_by_sku(sku)
        if p:
            products_data[sku] = p
            found_ids.append(p['id'])
        else:
            print(f"   [!] SKU {sku} no encontrado en WooCommerce.")

    if len(found_ids) < 2:
        print("   [!] Menos de 2 productos encontrados. No se puede verificar vinculo.")
        return False

    found_ids.sort()
    all_ok = True
    
    # 2. Verificar que cada producto apunte a sus hermanos
    for sku, p in products_data.items():
        my_id = p['id']
        # Hermanos son todos menos yo
        expected_links = [x for x in found_ids if x != my_id]
        expected_links.sort()
        
        # Obtener ids actuales del plugin
        actual_links = []
        meta = p.get('meta_data', [])
        for m in meta:
            if m['key'] == CLAVE_PLUGIN:
                val = m['value']
                if isinstance(val, list):
                    actual_links = sorted(val)
                elif isinstance(val, str):
                    # A veces viene como string si es uno solo o vacio, o serializado.
                    # Asumimos lista si el plugin funciona bien.
                    pass
                break
        
        if actual_links == expected_links:
            print(f"   [OK] Prod ID {my_id} ({sku}) -> OK")
        else:
            print(f"   [X] Prod ID {my_id} ({sku}) -> FALLO")
            print(f"      Esperado: {expected_links}")
            print(f"      Actual:   {actual_links}")
            all_ok = False
            
    return all_ok

def main():
    print("------------------------------------------------")
    print("VALIDADOR DE VINCULOS (MUESTREO ALEATORIO)")
    print("------------------------------------------------")
    
    if not os.path.exists(ARCHIVO_JSON):
        print(f"No existe el archivo {ARCHIVO_JSON}")
        return

    with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
        familias = json.load(f)
    
    total = len(familias)
    print(f"Total de familias en mapa: {total}")
    
    # Seleccionar 5 al azar
    muestras = random.sample(list(familias.items()), min(5, total))
    
    exitos = 0
    fallos = 0
    
    for nombre, skus in muestras:
        if check_family(nombre, skus):
            exitos += 1
        else:
            fallos += 1
            
    print("\n------------------------------------------------")
    print(f"Resumen de Muestreo:")
    print(f"[OK] Familias Correctas: {exitos}")
    print(f"[X] Familias Incorrectas: {fallos}")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()
