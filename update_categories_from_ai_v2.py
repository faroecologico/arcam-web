print("--- SCRIPT RESUME START ---", flush=True)

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

# --- CONFIGURACIÓN ---
CSV_PATH = r"C:\Users\usuario_tr7\Desktop\Archivos de reportes Enero 2025\arcam-web\Categorizacion csv\productos_para_recategorizar_con_ruta_sugerida.csv"
PROGRESS_FILE = "recat_progress.json"
BATCH_SIZE = 50

def get_headers():
    credentials = f"{WOO_KEY}:{WOO_SECRET}"
    token = b64encode(credentials.encode()).decode("utf-8")
    return { "Authorization": f"Basic {token}", "Content-Type": "application/json" }

# Caché para evitar duplicar llamadas a la API de categorías
cache_categorias = {}
# Mapa de ID -> Padre para reconstrucción de rutas
id_to_parent = {}
id_to_name = {}

def cargar_categorias_existentes():
    print("Cargando categorías existentes para optimizar...", flush=True)
    page = 1
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
                id_to_name[c['id']] = c['name']
                id_to_parent[c['id']] = c['parent']
            page += 1
        except Exception as e:
            print(f"Error cargando categorías: {e}", flush=True)
            break
            
    # Construir el caché de rutas completas
    def get_full_path(cid):
        path = [id_to_name[cid]]
        curr_parent = id_to_parent[cid]
        while curr_parent != 0:
            if curr_parent in id_to_name:
                path.insert(0, id_to_name[curr_parent])
                curr_parent = id_to_parent[curr_parent]
            else:
                break
        return " > ".join(path)

    for cid in id_to_name:
        path = get_full_path(cid)
        cache_categorias[path] = cid
    
    print(f"Caché cargado con {len(cache_categorias)} rutas de categorías.", flush=True)

def buscar_o_crear_categoria(ruta_completa):
    if not ruta_completa or str(ruta_completa).lower() == 'nan':
        return None
        
    # Normalizar separador
    ruta_norm = ruta_completa.replace(" > ", ">").replace(">", " > ")
    
    if ruta_norm in cache_categorias:
        return cache_categorias[ruta_norm]
        
    partes = [p.strip() for p in ruta_norm.split(">")]
    id_padre = 0
    ruta_acumulada = ""

    for i, parte in enumerate(partes):
        if i == 0:
            ruta_acumulada = parte
        else:
            ruta_acumulada += f" > {parte}"
            
        if ruta_acumulada in cache_categorias:
            id_padre = cache_categorias[ruta_acumulada]
            continue

        # Si no está en caché, buscar o crear
        encontrado_id = None
        try:
            # Buscar bajo el padre actual
            url = f"{WOO_URL}/wp-json/wc/v3/products/categories?search={parte}&parent={id_padre}"
            r = requests.get(url, headers=get_headers(), timeout=20)
            if r.status_code == 200:
                cats = r.json()
                for c in cats:
                    if c['name'].lower() == parte.lower() and c['parent'] == id_padre:
                        encontrado_id = c['id']
                        break
        except: pass

        if not encontrado_id:
            print(f"   [+] Creando categoría: '{parte}' (Padre: {id_padre})", flush=True)
            try:
                url_create = f"{WOO_URL}/wp-json/wc/v3/products/categories"
                r_create = requests.post(url_create, headers=get_headers(), json={"name": parte, "parent": id_padre}, timeout=20)
                if r_create.status_code == 201:
                    encontrado_id = r_create.json()['id']
                else:
                    return None
            except: return None
        
        cache_categorias[ruta_acumulada] = encontrado_id
        id_padre = encontrado_id

    return id_padre

def enviar_lote(lote):
    if not lote: return
    try:
        url_batch = f"{WOO_URL}/wp-json/wc/v3/products/batch"
        r = requests.post(url_batch, headers=get_headers(), json={"update": lote}, timeout=40)
        if r.status_code == 200:
            return True
        else:
            print(f"Error lote: {r.status_code}", flush=True)
            return False
    except Exception as e:
        print(f"Error conexión lote: {e}", flush=True)
        return False

def main():
    cargar_categorias_existentes()
    
    last_processed_idx = 0
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as pf:
            last_processed_idx = json.load(pf).get("idx", 0)
    
    print(f"Iniciando desde el índice {last_processed_idx}...", flush=True)

    lote = []
    total_upd = 0
    
    with open(CSV_PATH, mode='r', encoding='utf-8-sig') as f:
        reader = list(csv.DictReader(f))
        
        for i, row in enumerate(reader):
            if i < last_processed_idx:
                continue
                
            pid = row.get('ID')
            ruta = row.get('Ruta_Categoria_Sugerida')
            
            if not pid or not ruta or str(ruta).lower() == 'nan':
                continue
                
            cid = buscar_o_crear_categoria(ruta)
            if cid:
                lote.append({"id": pid, "categories": [{"id": cid}]})
            
            if len(lote) >= BATCH_SIZE:
                if enviar_lote(lote):
                    total_upd += len(lote)
                    print(f"Procesados {i+1}/{len(reader)} productos...", flush=True)
                    with open(PROGRESS_FILE, 'w') as pf:
                        json.dump({"idx": i + 1}, pf)
                lote = []
                time.sleep(0.5)

        if lote:
            if enviar_lote(lote):
                total_upd += len(lote)
                print(f"Finalizado: {len(reader)}/{len(reader)}", flush=True)
                with open(PROGRESS_FILE, 'w') as pf:
                    json.dump({"idx": len(reader)}, pf)

    print(f"--- FIN. Total {total_upd} productos recategorizados. ---", flush=True)

if __name__ == "__main__":
    main()
