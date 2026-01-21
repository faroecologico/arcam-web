import requests
import json
import time
import os
from dotenv import load_dotenv
from base64 import b64encode
import sys

load_dotenv()

# --- TUS CREDENCIALES ---
WOO_URL = os.getenv("WOO_URL")
WOO_KEY = os.getenv("WOO_KEY")
WOO_SECRET = os.getenv("WOO_SECRET")

# --- CONFIGURACIÓN ---
CLAVE_PLUGIN = os.getenv("CLAVE_PLUGIN")
ARCHIVO_JSON = os.getenv("ARCHIVO_JSON")

# --- CACHÉ EN MEMORIA ---
CACHE_SKU_ID = {} # Para no preguntar 2 veces el ID del mismo SKU

def get_headers():
    credentials = f"{WOO_KEY}:{WOO_SECRET}"
    token = b64encode(credentials.encode()).decode("utf-8")
    return { "Authorization": f"Basic {token}", "Content-Type": "application/json" }

def cargar_inventario_completo():
    """ 
    Descarga todos los productos (id, sku, meta_data) por lotes.
    Esto reduce drásticamente el tiempo de ejecución al evitar miles de GETs individuales.
    """
    print("------------------------------------------------")
    print(">> CARGANDO INVENTARIO (MODO EFICIENTE)")
    print("------------------------------------------------")
    print("Descargando productos en memoria para acelerar la busqueda...")
    
    page = 1
    per_page = 100
    headers = get_headers()
    total_cargados = 0
    
    while True:
        try:
            # Pedimos ID, SKU y Meta Data
            url = f"{WOO_URL}/wp-json/wc/v3/products?page={page}&per_page={per_page}"
            r = requests.get(url, headers=headers, timeout=30)
            
            if r.status_code == 200:
                data = r.json()
                if not data:
                    break # Se acabaron los productos
                
                for p in data:
                    sku = str(p.get('sku', '')).strip()
                    if sku:
                        CACHE_SKU_ID[sku] = {
                            'id': p['id'],
                            'meta': p.get('meta_data', [])
                        }
                
                total_cargados += len(data)
                print(f"   Pagina {page} | Productos cargados: {total_cargados}")
                page += 1
            else:
                print(f"   [!] Error en pagina {page} (Status {r.status_code})... reintentando en 5s")
                time.sleep(5)
                
        except Exception as e:
            print(f"   [X] Excepcion descargando pagina {page}: {e}... reintentando en 5s")
            time.sleep(5)
    
    print(f">> Inventario cargado: {len(CACHE_SKU_ID)} SKUs unicos en memoria.\n")


def obtener_id_por_sku(sku):
    """ Busca el ID de un producto. Primero en RAM, luego en API si falla. """
    # 1. Búsqueda Rápida (RAM)
    if sku in CACHE_SKU_ID: 
        return CACHE_SKU_ID[sku]
    
    # 2. Búsqueda Lenta (API) - Solo fallback
    intentos = 0
    while intentos < 3:
        try:
            url = f"{WOO_URL}/wp-json/wc/v3/products?sku={sku}"
            r = requests.get(url, headers=get_headers(), timeout=20)
            
            if r.status_code == 200:
                data = r.json()
                if data and isinstance(data, list) and len(data) > 0:
                    found_id = data[0]['id']
                    meta = data[0].get('meta_data', [])
                    res = {'id': found_id, 'meta': meta}
                    CACHE_SKU_ID[sku] = res # Guardar para la próxima
                    return res
                else:
                    return None # No existe
            else:
                time.sleep(2)
                intentos += 1
        except Exception as e:
            time.sleep(5)
            intentos += 1
            
    return None

def conectar_familia(nombre_familia, lista_skus):
    """ Conecta una lista de SKUs entre sí. """
    
    # 1. Traducir SKUs a IDs y obtener datos
    datos_validos = []
    
    for sku in lista_skus:
        info = obtener_id_por_sku(sku)
        if info:
            datos_validos.append(info)
    
    ids_puros = [d['id'] for d in datos_validos]
    
    if len(ids_puros) < 2:
        return

    # 2. Conectar todos con todos
    cambios_realizados = 0
    
    for info_producto in datos_validos:
        id_propio = info_producto['id']
        meta_actual = info_producto['meta']
        
        # La lista de hermanos son todos MENOS yo mismo
        ids_hermanos = [x for x in ids_puros if x != id_propio]
        ids_hermanos.sort() 
        
        # --- VERIFICACIÓN INTELIGENTE (SALTO) ---
        ya_conectado = False
        for m in meta_actual:
            if m['key'] == CLAVE_PLUGIN:
                valor_actual = m['value']
                if isinstance(valor_actual, list):
                    valor_actual.sort()
                    if valor_actual == ids_hermanos:
                        ya_conectado = True
                break
        
        if ya_conectado:
            continue 
        # ----------------------------------------

        # Actualizar
        payload = {
            "meta_data": [
                {
                    "key": CLAVE_PLUGIN,
                    "value": ids_hermanos
                }
            ]
        }
        
        intentos_up = 0
        while intentos_up < 3:
            try:
                url = f"{WOO_URL}/wp-json/wc/v3/products/{id_propio}"
                r = requests.put(url, headers=get_headers(), json=payload, timeout=20)
                
                if r.status_code in [200, 201]:
                    print(f"   [F: {nombre_familia[:20]}...] Conectado ID {id_propio} -> {ids_hermanos}")
                    cambios_realizados += 1
                    # time.sleep(0.2)
                    break
                else:
                    print(f"   Error {r.status_code} en ID {id_propio}")
                    time.sleep(2)
                    intentos_up += 1
            except Exception as e:
                print(f"   Error PUT ID {id_propio}: {e}")
                time.sleep(5)
                intentos_up += 1

    if cambios_realizados > 0:
        print(f"   > Familia actualizada: {nombre_familia}")

def main():
    print("------------------------------------------------")
    print("CONECTOR DE VARIANTES V2.0 (MODO CACHE)")
    print("------------------------------------------------")
    
    if not os.path.exists(ARCHIVO_JSON):
        print(f"ERROR: No existe '{ARCHIVO_JSON}'.")
        return

    # 1. Cargar caché
    cargar_inventario_completo()

    print("Leyendo mapa de variantes...")
    with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
        familias = json.load(f)

    total_familias = len(familias)
    print(f"Procesando {total_familias} familias...\n")
    
    contador = 1
    for nombre, skus in familias.items():
        if contador % 50 == 0:
            print(f"Progreso: {contador}/{total_familias} familias revisadas...")
        
        conectar_familia(nombre, skus)
        contador += 1

    print("\n------------------------------------------------")
    print("¡PROCESO TERMINADO EXITOSAMENTE!")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()