import requests
import json
import time
import os
from dotenv import load_dotenv
from base64 import b64encode

load_dotenv()

# --- TUS CREDENCIALES (PÉGALAS AQUÍ DENTRO DE LAS COMILLAS) ---
WOO_URL = os.getenv("WOO_URL")
WOO_KEY = os.getenv("WOO_KEY")
WOO_SECRET = os.getenv("WOO_SECRET") 

# --- CONFIGURACIÓN ARCAM ---
# Mínimo de letras iguales al inicio para ser familia
LARGO_MINIMO_COINCIDENCIA = 10 
# Archivo temporal para no descargar 20.000 veces
ARCHIVO_CACHE = "respaldo_productos.json"

def get_headers():
    credentials = f"{WOO_KEY}:{WOO_SECRET}"
    token = b64encode(credentials.encode()).decode("utf-8")
    return { "Authorization": f"Basic {token}", "Content-Type": "application/json" }

def obtener_prefijo_comun(texto1, texto2):
    largo = min(len(texto1), len(texto2))
    for i in range(largo):
        if texto1[i] != texto2[i]:
            return texto1[:i]
    return texto1[:largo]

def descargar_productos():
    print(f"📡 Conectando a {WOO_URL}...")
    productos = []
    page = 1
    while True:
        try:
            url = f"{WOO_URL}/wp-json/wc/v3/products?page={page}&per_page=100"
            r = requests.get(url, headers=get_headers())
            
            if r.status_code != 200: break
            data = r.json()
            if not data: break
            
            for p in data:
                # Guardamos solo lo necesario
                productos.append({
                    "id": p["id"], 
                    "name": p["name"].strip().upper() 
                })
            
            print(f"   Descargando página {page} ({len(productos)} productos)...", end="\r")
            page += 1
            time.sleep(0.5)
        except:
            break
            
    # Guardar en disco para futuro uso
    with open(ARCHIVO_CACHE, "w", encoding="utf-8") as f:
        json.dump(productos, f)
    print(f"\n💾 Respaldo guardado en '{ARCHIVO_CACHE}'.")
    return productos

def main():
    print("------------------------------------------------")
    print("🚀 INICIANDO SCRIPT DE AGRUPACIÓN (ARCAM)")
    print("------------------------------------------------")

    # 1. CARGAR DATOS (Desde web o desde archivo si ya existe)
    if os.path.exists(ARCHIVO_CACHE):
        print(f"📂 Cargando productos desde archivo local '{ARCHIVO_CACHE}'...")
        print("   (Si quieres descargar de nuevo, borra ese archivo)")
        with open(ARCHIVO_CACHE, "r", encoding="utf-8") as f:
            productos = json.load(f)
    else:
        productos = descargar_productos()

    if not productos:
        print("❌ No se encontraron productos o fallaron las claves.")
        return

    print(f"\n🧠 Analizando {len(productos)} productos con Patrón de Prefijo...")
    
    # 2. ORDENAR Y AGRUPAR (Lógica Arcam)
    productos.sort(key=lambda x: x['name'])
    
    familias = {}
    grupo_actual = [productos[0]]
    
    for i in range(1, len(productos)):
        prod_previo = productos[i-1]
        prod_actual = productos[i]
        
        prefijo = obtener_prefijo_comun(prod_previo['name'], prod_actual['name'])
        
        if len(prefijo) >= LARGO_MINIMO_COINCIDENCIA:
            grupo_actual.append(prod_actual)
        else:
            if len(grupo_actual) > 1:
                # La clave será el nombre común limpio (sin guiones al final)
                nombre_familia = obtener_prefijo_comun(grupo_actual[0]['name'], grupo_actual[-1]['name'])
                nombre_familia = nombre_familia.strip(" -")
                familias[nombre_familia] = [p['id'] for p in grupo_actual]
            grupo_actual = [prod_actual]

    # Guardar último grupo
    if len(grupo_actual) > 1:
        nombre_familia = obtener_prefijo_comun(grupo_actual[0]['name'], grupo_actual[-1]['name']).strip(" -")
        familias[nombre_familia] = [p['id'] for p in grupo_actual]

    # 3. RESULTADO FINAL
    archivo_salida = "familias_finales.json"
    with open(archivo_salida, "w", encoding="utf-8") as f:
        json.dump(familias, f, indent=4)

    print("------------------------------------------------")
    print(f"✅ ¡TERMINADO! Se crearon {len(familias)} familias.")
    print(f"📁 Revisa el archivo: {archivo_salida}")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()