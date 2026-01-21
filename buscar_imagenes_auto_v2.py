import os
import requests
import json
import re
import csv
import time
from dotenv import load_dotenv
from base64 import b64encode
from urllib.parse import quote_plus

load_dotenv()

import functools
print = functools.partial(print, flush=True)

WOO_URL = os.getenv("WOO_URL")
WOO_KEY = os.getenv("WOO_KEY")
WOO_SECRET = os.getenv("WOO_SECRET")

CSV_REPORTE = "productos_sin_imagen_final.csv"
CARPETA_TEMP = "temp_descargas"
PROGRESS_FILE = "image_search_progress.json"

HEADERS_BROWSER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
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

def buscar_bing(query):
    try:
        url = f"https://www.bing.com/images/search?q={quote_plus(query)}&first=1"
        r = requests.get(url, headers=HEADERS_BROWSER, timeout=12)
        if r.status_code == 200:
            matches = re.findall(r'murl&quot;:&quot;(https?://.*?)&quot;', r.text)
            if not matches:
                matches = re.findall(r'"murl":"(https?://[^"]+)"', r.text)
            
            if matches:
                return matches[0]
    except Exception as e:
        print(f"      [!] Error Bing: {e}")
    return None

def buscar_imagen(nombre_producto, sku=""):
    query_base = nombre_producto
    query_base = query_base.replace("FERR.", "").replace("LIBR.", "").strip()
    
    print(f"    [?] Buscando: '{query_base[:50]}...'")
    
    img = buscar_bing(query_base)
    if img: 
        print(f"      [OK] Encontrada")
        return img
    
    if sku:
        img = buscar_bing(f"{query_base} {sku}")
        if img:
            print(f"      [OK] Encontrada con SKU")
            return img
    
    return None

def descargar_imagen(url, nombre_temp):
    if not os.path.exists(CARPETA_TEMP):
        os.makedirs(CARPETA_TEMP)
        
    path = os.path.join(CARPETA_TEMP, nombre_temp)
    try:
        r = requests.get(url, headers=HEADERS_BROWSER, timeout=15, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            return path
    except Exception as e:
        print(f"      [!] Error descarga: {e}")
    return None

def subir_imagen_wp(ruta_imagen, alt_text):
    url = f"{WOO_URL}/wp-json/wp/v2/media"
    filename = os.path.basename(ruta_imagen)
    
    try:
        with open(ruta_imagen, 'rb') as f:
            data = f.read()
            
        headers = get_media_headers(filename)
        if filename.lower().endswith('.png'):
            headers['Content-Type'] = 'image/png'
        else:
            headers['Content-Type'] = 'image/jpeg'
        
        r = requests.post(url, headers=headers, data=data, timeout=60)
        if r.status_code in [200, 201]:
            media_id = r.json().get('id')
            if media_id:
                requests.post(f"{url}/{media_id}", headers=get_headers(), 
                            json={"alt_text": alt_text, "title": alt_text}, timeout=20)
            return media_id
    except Exception as e:
        print(f"      [X] Error subiendo a WP: {e}")
    return None

def agregar_a_csv(producto):
    archivo_existe = os.path.exists(CSV_REPORTE)
    with open(CSV_REPORTE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not archivo_existe:
            writer.writerow(["ID", "SKU", "Nombre", "Categorias"])
        
        cats = " | ".join([c['name'] for c in producto.get('categories', [])])
        writer.writerow([producto['id'], producto.get('sku',''), producto['name'], cats])

def cargar_progreso():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f).get('last_page', 1)
    return 1

def guardar_progreso(page):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({'last_page': page}, f)

def main():
    print("------------------------------------------------")
    print("BUSCADOR AUTOMATICO DE IMAGENES v2.0")
    print("------------------------------------------------")
    
    last_page = cargar_progreso()
    print(f"Reanudando desde pagina {last_page}...")
    
    page = last_page
    total_procesados = 0
    total_exito = 0
    
    while True:
        print(f"\nLeyendo pagina {page}...")
        endpoint = f"{WOO_URL}/wp-json/wc/v3/products?status=publish&per_page=25&page={page}"
        
        try:
            r = requests.get(endpoint, headers=get_headers(), timeout=30)
        except Exception as e:
            print(f"Error conexion: {e}")
            break
            
        if r.status_code != 200: 
            print("Fin de productos o error.")
            break
        
        productos = r.json()
        if not productos: break
        
        for p in productos:
            if not p['images']:
                total_procesados += 1
                sku = p.get('sku', '')
                nombre = p.get('name', '')
                pid = p['id']
                
                print(f"\n[{total_procesados}] ID {pid}: {nombre[:45]}...")
                
                url_img = buscar_imagen(nombre, sku)
                
                if url_img:
                    local_path = descargar_imagen(url_img, f"img_{pid}.jpg")
                    if local_path:
                        media_id = subir_imagen_wp(local_path, nombre)
                        if media_id:
                            res = requests.put(
                                f"{WOO_URL}/wp-json/wc/v3/products/{pid}", 
                                headers=get_headers(), 
                                json={"images": [{"id": media_id}]},
                                timeout=20
                            )
                            if res.status_code == 200:
                                print("      [OK] Imagen asignada correctamente")
                                total_exito += 1
                        
                        try: os.remove(local_path)
                        except: pass
                else:
                    print("      [X] No encontrada - agregando a reporte")
                    agregar_a_csv(p)
                
                time.sleep(3)
                
        guardar_progreso(page + 1)
        page += 1
        time.sleep(1)

    print("\n------------------------------------------------")
    print(f"Finalizado: {total_exito} imagenes asignadas de {total_procesados} procesados")
    print(f"Revisa '{CSV_REPORTE}' para los productos sin imagen")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()
