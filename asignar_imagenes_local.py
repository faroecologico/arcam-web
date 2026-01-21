import os
import requests
import json
import re
import unicodedata
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
CARPETAS_IMAGENES = ["2014", "2020", "2023"]
EXTENSIONES_VALIDAS = {".jpg", ".jpeg", ".png", ".webp"}
PATRON_SUFIJO = re.compile(r"-(?:\d+x\d+|scaled)$")  # Detecta -150x150, -768x768, -scaled al final

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

def limpiar_nombre_archivo(nombre_archivo):
    """
    Quita extensión y sufijos de tamaño de WordPress.
    Ej: 'foto-producto-150x150.jpg' -> 'foto-producto'
    """
    nombre_base, ext = os.path.splitext(nombre_archivo)
    if ext.lower() not in EXTENSIONES_VALIDAS:
        return None
    
    # Quitar sufijo si existe (-NNNxNNN)
    nombre_limpio = PATRON_SUFIJO.sub("", nombre_base)
    return nombre_limpio.lower()

def normalizar_slug(texto):
    """Convierte texto a slug compatible con nombres de archivo."""
    # Quitar acentos y caracteres especiales
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    texto = texto.lower()
    # Reemplazar espacios y símbolos raros por guiones
    texto = re.sub(r'[^a-z0-9]+', '-', texto)
    return texto.strip('-')

def indexar_imagenes_locales():
    """
    Recorre las carpetas y construye un diccionario:
    { "nombre-limpio": "ruta/completa/a/la/imagen_mas_grande.jpg" }
    """
    print("[!] Indexando imagenes locales...")
    indice = {}
    base_dir = os.getcwd()
    
    total_archivos = 0
    
    for carpeta in CARPETAS_IMAGENES:
        ruta_carpeta = os.path.join(base_dir, carpeta)
        if not os.path.exists(ruta_carpeta):
            print(f"[!]  Carpeta no encontrada: {carpeta}")
            continue
            
        for root, dirs, files in os.walk(ruta_carpeta):
            for file in files:
                nombre_limpio = limpiar_nombre_archivo(file)
                if not nombre_limpio:
                    continue
                
                ruta_completa = os.path.join(root, file)
                size = os.path.getsize(ruta_completa)
                
                # Si ya existe, guardamos solo si esta es más grande (mejor calidad)
                if nombre_limpio in indice:
                    archivo_existente = indice[nombre_limpio]
                    size_existente = os.path.getsize(archivo_existente)
                    if size > size_existente:
                        indice[nombre_limpio] = ruta_completa
                else:
                    indice[nombre_limpio] = ruta_completa
                
                total_archivos += 1

    print(f"[OK] Se indexaron {len(indice)} imágenes únicas (de {total_archivos} archivos encontrados).")
    return indice

def subir_imagen_wp(ruta_imagen, alt_text):
    """Sube la imagen a WordPress y devuelve el ID."""
    print(f"   [!]  Subiendo: {os.path.basename(ruta_imagen)}...")
    url = f"{WOO_URL}/wp-json/wp/v2/media"
    
    # Determinar MIME type
    ext = os.path.splitext(ruta_imagen)[1].lower()
    mime_type = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
    if ext == ".webp": mime_type = "image/webp"

    try:
        with open(ruta_imagen, 'rb') as f:
            image_data = f.read()
            
        headers = get_media_headers(os.path.basename(ruta_imagen))
        headers["Content-Type"] = mime_type
        
        r = requests.post(url, headers=headers, data=image_data, timeout=60)
        
        if r.status_code in [200, 201]:
            media_id = r.json().get('id')
            # Actualizar ALT text y Título
            if media_id:
                requests.post(
                    f"{url}/{media_id}", 
                    headers=get_headers(), 
                    json={"alt_text": alt_text, "title": alt_text, "caption": alt_text}
                )
            return media_id
        else:
            print(f"   [X] Error subiendo: {r.status_code} - {r.text[:100]}")
            return None
    except Exception as e:
        print(f"   [X] Excepción subiendo: {e}")
        return None

def main():
    print("------------------------------------------------")
    print("[CAMARA] ASIGNADOR DE IMAGENES LOCALES -> WOOCOMMERCE")
    print("------------------------------------------------")

    # 1. Indexar imágenes
    mapa_imagenes = indexar_imagenes_locales()
    if not mapa_imagenes:
        print("[X] No se encontraron imágenes válidas.")
        return

    # 2. Obtener productos sin imagen
    page = 1
    modificados = 0
    
    while True:
        print(f"\n[!] Buscando productos sin imagen (Pagina {page})...")
        try:
            # Solo traemos productos PUBLICADOS
            endpoint = f"{WOO_URL}/wp-json/wc/v3/products?status=publish&per_page=50&page={page}"
            r = requests.get(endpoint, headers=get_headers(), timeout=30)
            
            if r.status_code != 200:
                print(" [X] Fin o error en API.")
                if r.status_code == 400: break # Fin de paginación usualmente
                break
                
            productos = r.json()
            if not productos:
                break
            
            for p in productos:
                p_id = p['id']
                nombre = p['name']
                slug_producto = p.get('slug') # WooCommerce ya suele tener el slug hecho
                imagenes_actuales = p.get('images', [])
                
                # Si ya tiene imagen, saltar
                if imagenes_actuales:
                    continue
                
                # Opción A: Match por SKU (Prioridad Alta)
                sku = str(p.get('sku', '')).strip()
                match_sku = None
                if sku:
                    sku_limpio = normalizar_slug(sku)
                    if sku_limpio in mapa_imagenes:
                        match_sku = sku_limpio

                # Opción B: Match por Slug del nombre
                match_slug = None
                key_slug = slug_producto if slug_producto else normalizar_slug(nombre)
                if key_slug in mapa_imagenes:
                    match_slug = key_slug

                # Decisión final
                ruta_encontrada = None
                if match_sku:
                    ruta_encontrada = mapa_imagenes[match_sku]
                    print(f"[MATCH] SKU: '{sku}' -> '{os.path.basename(ruta_encontrada)}'")
                elif match_slug:
                    ruta_encontrada = mapa_imagenes[match_slug]
                    print(f"[MATCH] NOMBRE: '{nombre}' -> '{os.path.basename(ruta_encontrada)}'")
                
                if ruta_encontrada:
                    # Subir
                    media_id = subir_imagen_wp(ruta_encontrada, nombre)
                    
                    if media_id:
                        # Asignar
                        url_up = f"{WOO_URL}/wp-json/wc/v3/products/{p_id}"
                        data_up = { "images": [ { "id": media_id } ] }
                        res = requests.put(url_up, headers=get_headers(), json=data_up)
                        
                        if res.status_code == 200:
                            print(f"   [OK] Imagen asignada correctamente.")
                            modificados += 1
                        else:
                            print(f"   [!] Error asignando al producto.")
                else:
                    # Debug silencioso o verbose
                    # print(f"   . No imagen para: {key_busqueda}")
                    pass

            page += 1
            
        except Exception as e:
            print(f"[X] Error crítico en bucle: {e}")
            break

    print("------------------------------------------------")
    print(f"[FIN] Proceso finalizado. Total productos actualizados: {modificados}")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()
