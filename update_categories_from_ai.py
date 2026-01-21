print("--- SCRIPT START ---", flush=True)

import requests
import json
import time
import os
import csv
from dotenv import load_dotenv
from base64 import b64encode

print("--- LIBS LOADED ---", flush=True)

load_dotenv()

# --- CREDENCIALES ---
WOO_URL = os.getenv("WOO_URL")
WOO_KEY = os.getenv("WOO_KEY")
WOO_SECRET = os.getenv("WOO_SECRET")

print(f"URL: {WOO_URL}", flush=True)

# --- CONFIGURACIÓN ---
CSV_PATH = r"C:\Users\usuario_tr7\Desktop\Archivos de reportes Enero 2025\arcam-web\Categorizacion csv\productos_para_recategorizar_con_ruta_sugerida.csv"
BATCH_SIZE = 50

def get_headers():
    credentials = f"{WOO_KEY}:{WOO_SECRET}"
    token = b64encode(credentials.encode()).decode("utf-8")
    return { "Authorization": f"Basic {token}", "Content-Type": "application/json" }

cache_categorias = {}

def buscar_o_crear_categoria(ruta_completa):
    if not ruta_completa or str(ruta_completa).lower() == 'nan':
        return None
    if ruta_completa in cache_categorias:
        return cache_categorias[ruta_completa]
    
    partes = [p.strip() for p in ruta_completa.split(">")]
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

        encontrado_id = None
        try:
            url = f"{WOO_URL}/wp-json/wc/v3/products/categories?search={parte}&per_page=100"
            r = requests.get(url, headers=get_headers(), timeout=20)
            if r.status_code == 200:
                cats = r.json()
                for c in cats:
                    if c['name'].lower() == parte.lower() and c['parent'] == id_padre:
                        encontrado_id = c['id']
                        break
        except Exception as e:
            print(f"Error buscando '{parte}': {e}", flush=True)

        if not encontrado_id:
            print(f"   [+] Creando categoría: '{parte}' (Padre ID: {id_padre})", flush=True)
            try:
                url_create = f"{WOO_URL}/wp-json/wc/v3/products/categories"
                payload = {"name": parte, "parent": id_padre}
                r_create = requests.post(url_create, headers=get_headers(), json=payload, timeout=20)
                if r_create.status_code == 201:
                    encontrado_id = r_create.json()['id']
                else:
                    print(f"   [!] Error creando '{parte}': {r_create.text}", flush=True)
                    return None
            except Exception as e:
                print(f"   [!] Excepción creando categoría: {e}", flush=True)
                return None
        
        cache_categorias[ruta_acumulada] = encontrado_id
        id_padre = encontrado_id

    return id_padre

def enviar_lote(lote):
    if not lote: return
    print(f"   >> Enviando actualización para {len(lote)} productos...", flush=True)
    try:
        url_batch = f"{WOO_URL}/wp-json/wc/v3/products/batch"
        payload = {"update": lote}
        r = requests.post(url_batch, headers=get_headers(), json=payload, timeout=40)
        if r.status_code == 200:
            print("      [OK] Lote actualizado.", flush=True)
        else:
            print(f"      [X] Error en lote: {r.status_code} - {r.text}", flush=True)
    except Exception as e:
        print(f"      [!] Error de conexión: {e}", flush=True)

def main():
    print("--- MAIN START ---", flush=True)
    if not os.path.exists(CSV_PATH):
        print(f"Archivo no encontrado: {CSV_PATH}", flush=True)
        return

    lote_actualizaciones = []
    total_procesados = 0

    try:
        with open(CSV_PATH, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            print(f"DEBUG: Headers detectados -> {headers}", flush=True)
            
            if not headers or 'ID' not in headers:
                print("ERROR: No se encontró la columna 'ID'.", flush=True)
                return

            for row in reader:
                pid = row.get('ID')
                ruta_sugerida = row.get('Ruta_Categoria_Sugerida')

                if not pid or not ruta_sugerida or str(ruta_sugerida).lower() == 'nan' or not ruta_sugerida.strip():
                    continue

                cat_id = buscar_o_crear_categoria(ruta_sugerida)
                
                if cat_id:
                    lote_actualizaciones.append({
                        "id": pid,
                        "categories": [{"id": cat_id}]
                    })
                    total_procesados += 1

                if len(lote_actualizaciones) >= BATCH_SIZE:
                    enviar_lote(lote_actualizaciones)
                    lote_actualizaciones = []
                    time.sleep(0.5)

        if lote_actualizaciones:
            enviar_lote(lote_actualizaciones)
            
    except Exception as e:
        print(f"Error procesando CSV: {e}", flush=True)

    print("------------------------------------------------")
    print(f"PROCESO FINALIZADO. Total productos actualizados: {total_procesados}", flush=True)
    print("------------------------------------------------")

if __name__ == "__main__":
    main()
