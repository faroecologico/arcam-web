import os
import requests
import json
import re
import csv
import time
import queue
import threading
from dotenv import load_dotenv
from base64 import b64encode
from urllib.parse import quote_plus

# Cargar variables de entorno
load_dotenv()

import functools
print = functools.partial(print, flush=True)

WOO_URL = os.getenv("WOO_URL")
WOO_KEY = os.getenv("WOO_KEY")
WOO_SECRET = os.getenv("WOO_SECRET")

CSV_REPORTE = "productos_sin_imagen.csv"
CARPETA_TEMP = "temp_descargas"

# Configuración de Headers para simular navegador real (evita bloqueos rápidos)
HEADERS_BROWSER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
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

# ==========================================
# 🕵️ MÓDULOS DE BÚSQUEDA
# ==========================================

def buscar_bing(query):
    """Busca en Bing Images parseando HTML"""
    try:
        url = f"https://www.bing.com/images/search?q={quote_plus(query)}&first=1&count=1"
        r = requests.get(url, headers=HEADERS_BROWSER, timeout=10)
        if r.status_code == 200:
            # Patrones comunes de Bing para imágenes directas
            # Murl suele ser el link directo en el JSON incrustado
            matches = re.findall(r'murl&quot;:&quot;(https?://.*?)&quot;', r.text)
            if not matches:
                matches = re.findall(r'"murl":"(https?://[^"]+)"', r.text)
            
            if matches:
                return matches[0]
    except Exception as e:
        print(f"      [!] Error Bing: {e}")
    return None

def buscar_duckduckgo(query):
    """Busca en DuckDuckGo API (versión no oficial)"""
    try:
        url = f"https://duckduckgo.com/?q={quote_plus(query)}&t=h_&iax=images&ia=images"
        # DDG requiere un proceso de 2 pasos normalmente (token -> búsqueda), 
        # pero simplificaremos intentando extraer del html si es posible o usando su API vqd si se implementara full.
        # Por simplicidad y robustez inmediata, usaremos una API pública si existe o scrape simple.
        # Intento via api html simple:
        
        # NOTA: DDG es difícil de scrapear sin tokens.
        # Alternativa rápida: Usar un servicio de búsqueda secundario o Google "lite".
        # Intentaremos Google Custom Search si Bing falla es mejor, pero sin API key es difícil.
        # Vamos a simular una petición simple a un metabuscador si es posible o un scrape básico.
        
        # Para mantener esto simple y funcional sin librerías externas complejas (selenium),
        # usaremos un fallback a una búsqueda genérica html.
        pass 
    except:
        pass
    return None

def buscar_google_lite(query):
    """Intento de búsqueda en Google Images (muy propenso a bloqueo, usar con cuidado)"""
    try:
        url = f"https://www.google.com/search?q={quote_plus(query)}&tbm=isch"
        r = requests.get(url, headers=HEADERS_BROWSER, timeout=10)
        
        # Google suele poner las imagenes en scripts. Buscamos patrones de URL de imagen jpg/png
        # Regex heurística para encontrar urls de imagen grandes
        patron = r'(https?://[^"]+\.(?:jpg|jpeg|png))'
        candidatos = re.findall(patron, r.text)
        
        for url_img in candidatos:
            # Filtramos iconos pequeños o de google
            if 'gstatic' not in url_img and 'google' not in url_img:
                return url_img
                
    except Exception as e:
        print(f"      [!] Error Google: {e}")
    return None

def buscar_imagen_multicanal(query):
    """Orquestador de búsquedas"""
    print(f"    [?] Buscando: '{query}'")
    
    # 1. Bing (Suele ser el más permisivo)
    img = buscar_bing(query)
    if img: 
        print(f"      [OK] Encontrada en Bing")
        return img
    
    # 2. Google Lite (Fallback)
    img = buscar_google_lite(query)
    if img:
        print(f"      [OK] Encontrada en Google")
        return img
        
    return None

# ==========================================
# 🛠️ UTILIDADES
# ==========================================

def descargar_imagen(url, nombre_temp):
    if not os.path.exists(CARPETA_TEMP):
        os.makedirs(CARPETA_TEMP)
        
    path = os.path.join(CARPETA_TEMP, nombre_temp)
    try:
        r = requests.get(url, headers=HEADERS_BROWSER, timeout=15)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                f.write(r.content)
            return path
    except:
        return None
    return None

def subir_imagen_wp(ruta_imagen, alt_text):
    url = f"{WOO_URL}/wp-json/wp/v2/media"
    filename = os.path.basename(ruta_imagen)
    
    try:
        with open(ruta_imagen, 'rb') as f:
            data = f.read()
            
        headers = get_media_headers(filename)
        headers['Content-Type'] = 'image/jpeg' # Asumimos jpeg por simplicidad
        
        r = requests.post(url, headers=headers, data=data, timeout=60)
        if r.status_code in [200, 201]:
            media_id = r.json().get('id')
            if media_id:
                requests.post(f"{url}/{media_id}", headers=get_headers(), json={"alt_text": alt_text, "title": alt_text})
            return media_id
    except Exception as e:
        print(f"      [X] Error subida: {e}")
    return None

def agregar_a_csv(producto):
    archivo_existe = os.path.exists(CSV_REPORTE)
    with open(CSV_REPORTE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not archivo_existe:
            writer.writerow(["ID", "SKU", "Nombre", "URL_IMAGEN_MANUAL"])
        
        writer.writerow([producto['id'], producto['sku'], producto['name'], ""])

# ==========================================
# 🚀 MAIN
# ==========================================

def main():
    print("------------------------------------------------")
    print("[CAZADOR] BUSCADOR DE IMAGENES WEB v1.0")
    print("------------------------------------------------")
    
    if os.path.exists(CSV_REPORTE):
        print("[!]  Borrando reporte anterior...")
        os.remove(CSV_REPORTE)

    page = 1
    total_web = 1
    
    while True:
        print(f"\n[!] Leyendo pagina {page} de productos...")
        endpoint = f"{WOO_URL}/wp-json/wc/v3/products?status=publish&per_page=20&page={page}"
        
        try:
            r = requests.get(endpoint, headers=get_headers(), timeout=30)
        except:
            break
            
        if r.status_code != 200: break
        
        productos = r.json()
        if not productos: break
        
        for p in productos:
            # Solo procesar si NO tiene imagen
            if not p['images']:
                sku = p.get('sku', '')
                nombre = p.get('name', '')
                pid = p['id']
                
                print(f" [{total_web}] [ID {pid}]: {nombre[:40]}...")
                
                # Estrategia de búsqueda: Nombre + SKU
                query = f"{nombre} {sku}".strip()
                url_img = buscar_imagen_multicanal(query)
                
                exito = False
                if url_img:
                    # Descargar
                    local_path = descargar_imagen(url_img, f"temp_{pid}.jpg")
                    if local_path:
                        # Subir
                        media_id = subir_imagen_wp(local_path, nombre)
                        if media_id:
                            # Asignar
                            res = requests.put(f"{WOO_URL}/wp-json/wc/v3/products/{pid}", headers=get_headers(), json={"images": [{"id": media_id}]})
                            if res.status_code == 200:
                                print("      [OK] Asignada correctamente.")
                                exito = True
                        
                        # Limpieza
                        try: os.remove(local_path)
                        except: pass
                
                if not exito:
                    print("      [X] No se encontró imagen. Agregando a CSV.")
                    agregar_a_csv({"id": pid, "sku": sku, "name": nombre})
                
                # Pausa anti-bloqueo
                time.sleep(2)
                total_web += 1
                
        page += 1

    print("\n------------------------------------------------")
    print(f"[FINAL] Ejecución terminada. Revisa '{CSV_REPORTE}' para los fallidos.")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()
