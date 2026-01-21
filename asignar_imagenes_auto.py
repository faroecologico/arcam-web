import requests
import json
import time
import os
from dotenv import load_dotenv
import shutil
from base64 import b64encode
from urllib.parse import quote_plus
import re

load_dotenv()

# --- TUS CREDENCIALES ---
WOO_URL = os.getenv("WOO_URL")
WOO_KEY = os.getenv("WOO_KEY")
WOO_SECRET = os.getenv("WOO_SECRET") 

TEMP_DIR = "temp_images"

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
        "Content-Disposition": f'attachment; filename="{filename}"',
    }

def buscar_imagen_bing(query, limit=1):
    """Busca imágenes en Bing y retorna lista de URLs."""
    try:
        # Usamos Bing.com/images/search y parseamos el HTML
        search_url = f"https://www.bing.com/images/search?q={quote_plus(query)}&first=0&count={limit}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        r = requests.get(search_url, headers=headers, timeout=10)
        
        if r.status_code == 200:
            # Buscamos URLs de imágenes en el HTML
            # Bing suele tener patrones como "murl":"..." o enlaces directos
            pattern = r'"murl":"(https?://[^"]+)"'
            matches = re.findall(pattern, r.text)
            
            if matches:
                return matches[:limit]
        
        return []
    except Exception as e:
        print(f"      [!] Error buscando en Bing: {e}")
        return []

def descargar_imagen(url, save_path):
    """Descarga una imagen desde URL y la guarda localmente."""
    try:
        r = requests.get(url, timeout=15, stream=True)
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        return False
    except Exception as e:
        print(f"      [!] Error descargando: {e}")
        return False

def upload_image_to_woo(image_path, alt_text):
    """Sube una imagen local a la biblioteca de medios de WordPress y retorna su ID."""
    url = f"{WOO_URL}/wp-json/wp/v2/media"
    filename = os.path.basename(image_path)
    
    headers = get_media_headers(filename)
    headers["Content-Type"] = "image/jpeg"
    
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
            
        r = requests.post(url, headers=headers, data=image_data, timeout=30)
        
        if r.status_code in [200, 201]:
            media_id = r.json().get('id')
            if media_id:
                requests.post(
                    f"{url}/{media_id}", 
                    headers=get_headers(), 
                    json={"alt_text": alt_text, "title": alt_text}
                )
            return media_id
        else:
            print(f"      [X] Error subiendo imagen: {r.status_code}")
            return None
    except Exception as e:
        print(f"      [!] Excepcion al subir: {e}")
        return None

def buscar_y_asignar_imagen():
    print("------------------------------------------------")
    print("[CAMARA] BUSCADOR AUTOMATICO DE IMAGENES (BING)")
    print("------------------------------------------------")

    # Limpieza inicial
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR, exist_ok=True)

    page = 1
    productos_procesados = 0
    MAX_PRODUCTOS = 10  # LIMITE DE PRUEBA - cambiar a None para todos
    
    while True:
        print(f" -- Leyendo pagina {page} de productos...")
        
        endpoint = f"{WOO_URL}/wp-json/wc/v3/products?per_page=20&page={page}"
        try:
            r = requests.get(endpoint, headers=get_headers(), timeout=20)
        except Exception as e:
            print(f" [X] Error de conexion: {e}")
            break

        if r.status_code != 200:
            print(f" [X] Fin o Error API: {r.status_code}")
            break

        productos = r.json()
        if not productos:
            print(" [OK] No hay mas productos.")
            break

        for p in productos:
            p_id = p.get('id')
            nombre = p.get('name')
            sku = p.get('sku', '')
            images = p.get('images', [])
            stock = p.get('stock_quantity')
            
            # Criterio: Sin imagen Y con stock positivo
            tiene_stock = (stock is not None and stock > 0) or (p.get('manage_stock') is False)
            
            if not images and tiene_stock:
                productos_procesados += 1
                print(f"\n   [{productos_procesados}] BUSCANDO: {nombre[:60]}... (SKU: {sku})")
                
                query = f"{nombre} {sku}".strip()
                
                # Buscar imágenes
                image_urls = buscar_imagen_bing(query, limit=1)
                
                if image_urls:
                    image_url = image_urls[0]
                    print(f"      [ENCONTRADA] {image_url[:80]}...")
                    
                    # Descargar
                    temp_file = os.path.join(TEMP_DIR, f"temp_{p_id}.jpg")
                    if descargar_imagen(image_url, temp_file):
                        print(f"      [DESCARGADA]")
                        
                        # Subir a WordPress
                        media_id = upload_image_to_woo(temp_file, nombre)
                        
                        if media_id:
                            print(f"      [SUBIDA] Media ID: {media_id}")
                            
                            # Asignar a Producto
                            update_data = { "images": [ { "id": media_id } ] }
                            up_url = f"{WOO_URL}/wp-json/wc/v3/products/{p_id}"
                            
                            res = requests.put(up_url, headers=get_headers(), json=update_data, timeout=20)
                            
                            if res.status_code in [200, 201]:
                                print("      [OK] Imagen asignada al producto.")
                            else:
                                print(f"      [ERROR] Asignando: {res.status_code}")
                        else:
                            print("      [ERROR] No se pudo subir.")
                        
                        # Limpiar archivo temporal
                        try:
                            os.remove(temp_file)
                        except: pass
                    else:
                        print("      [ERROR] No se pudo descargar.")
                else:
                    print("      [!] No se encontraron imagenes en Bing.")
                
                # Pausa para no saturar
                time.sleep(2)
                
                # Limite de prueba
                if MAX_PRODUCTOS and productos_procesados >= MAX_PRODUCTOS:
                    print(f"\n[LIMITE] Alcanzado limite de {MAX_PRODUCTOS} productos. Terminando...")
                    return

        page += 1
    
    print(f"\n[FIN] Procesados {productos_procesados} productos en total.")

if __name__ == "__main__":
    buscar_y_asignar_imagen()
