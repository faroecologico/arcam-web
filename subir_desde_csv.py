import os
import requests
import json
import csv
import time
from dotenv import load_dotenv
from base64 import b64encode

# Cargar variables de entorno
load_dotenv()

import functools
print = functools.partial(print, flush=True)

WOO_URL = os.getenv("WOO_URL")
WOO_KEY = os.getenv("WOO_KEY")
WOO_SECRET = os.getenv("WOO_SECRET")

# Configuración
CSV_ENTRADA = "productos_sin_imagen.csv"
CARPETA_TEMP = "temp_manual"

HEADERS_BROWSER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
}

def get_headers():
    credentials = f"{WOO_KEY}:{WOO_SECRET}"
    token = b64encode(credentials.encode()).decode("utf-8")
    return { 
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json"
    }

def get_media_headers(filename):
    credentials = f"{WOO_KEY}:{WOO_SECRET}"
    token = b64encode(credentials.encode()).decode("utf-8")
    return { 
        "Authorization": f"Basic {token}",
        "Content-Disposition": f'attachment; filename="{filename}"'
    }

def descargar_y_subir(url_imagen, nombre_producto, id_producto):
    print(f"   ⬇️  Descargando: {url_imagen[:60]}...")
    
    try:
        # 1. Descargar
        if not os.path.exists(CARPETA_TEMP): os.makedirs(CARPETA_TEMP)
        path = os.path.join(CARPETA_TEMP, f"manual_{id_producto}.jpg")
        
        r = requests.get(url_imagen, headers=HEADERS_BROWSER, timeout=20)
        if r.status_code != 200:
            print(f"   ❌ Error descargando: {r.status_code}")
            return False
            
        with open(path, 'wb') as f:
            f.write(r.content)
            
        # 2. Subir a WP
        print(f"   ⬆️  Subiendo a WooCommerce...")
        url = f"{WOO_URL}/wp-json/wp/v2/media"
        filename = os.path.basename(path)
        
        with open(path, 'rb') as f:
            data = f.read()
            
        headers = get_media_headers(filename)
        headers['Content-Type'] = 'image/jpeg' 
        
        r_up = requests.post(url, headers=headers, data=data, timeout=60)
        if r_up.status_code not in [200, 201]:
            print(f"   ❌ Error subiendo a WP: {r_up.status_code}")
            return False
            
        media_id = r_up.json().get('id')
        
        # 3. Asignar
        if media_id:
            requests.post(f"{url}/{media_id}", headers=get_headers(), json={"alt_text": nombre_producto, "title": nombre_producto})
            
            res = requests.put(f"{WOO_URL}/wp-json/wc/v3/products/{id_producto}", headers=get_headers(), json={"images": [{"id": media_id}]})
            
            if res.status_code == 200:
                print("   ✨ ¡Asignada con éxito!")
                # Limpiar
                try: os.remove(path)
                except: pass
                return True
                
    except Exception as e:
        print(f"   ❌ Error: {e}")
        
    return False

def main():
    print("------------------------------------------------")
    print("📥 CARGADOR MASIVO DESDE CSV")
    print("------------------------------------------------")
    
    if not os.path.exists(CSV_ENTRADA):
        print(f"❌ No existe el archivo '{CSV_ENTRADA}'.")
        return

    print(f"Leyendo {CSV_ENTRADA}...")
    
    filas = []
    with open(CSV_ENTRADA, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        filas = list(reader)
        
    print(f"Total filas: {len(filas)}")
    exitos = 0
    
    for fila in filas:
        pid = fila.get("ID")
        nombre = fila.get("Nombre")
        url_manual = fila.get("URL_IMAGEN_MANUAL", "").strip()
        
        if pid and url_manual:
            print(f"\n🔹 Procesando ID {pid}: {nombre[:30]}...")
            if descargar_y_subir(url_manual, nombre, pid):
                exitos += 1
        else:
            # Si no hay URL, ignoramos
            pass
            
    print("\n------------------------------------------------")
    print(f"✅ Proceso terminado. Productos actualizados: {exitos}")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()
