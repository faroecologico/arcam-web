import requests
import json
import time
import os
from dotenv import load_dotenv
from base64 import b64encode

load_dotenv()

# --- TUS CREDENCIALES ---
WOO_URL = os.getenv("WOO_URL")
WOO_KEY = os.getenv("WOO_KEY")
WOO_SECRET = os.getenv("WOO_SECRET")

# --- CONFIGURACIÓN ---
ARCHIVO_FAMILIAS = "familias_finales.json"
CLAVE_PLUGIN = os.getenv("CLAVE_PLUGIN") 

# --- 🚀 PUNTO DE REINICIO ---
# Como quedaste en el 77, empezamos ahí para asegurar que ese grupo quede bien cerrado.
EMPEZAR_EN_GRUPO = 77

def get_headers():
    credentials = f"{WOO_KEY}:{WOO_SECRET}"
    token = b64encode(credentials.encode()).decode("utf-8")
    return { "Authorization": f"Basic {token}", "Content-Type": "application/json" }

def conectar_producto(id_propio, lista_hermanos):
    ids_a_conectar = [x for x in lista_hermanos if x != id_propio]
    if not ids_a_conectar: return True 

    payload = { "meta_data": [ { "key": CLAVE_PLUGIN, "value": ids_a_conectar } ] }
    
    try:
        url = f"{WOO_URL}/wp-json/wc/v3/products/{id_propio}"
        r = requests.put(url, headers=get_headers(), json=payload)
        if r.status_code in [200, 201]:
            print(f"   ✅ ID {id_propio} conectado.") 
            return True
        else:
            print(f"   ❌ Error en ID {id_propio}: {r.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return False

def main():
    print("------------------------------------------------")
    print(f"🚀 RETOMANDO CONEXIÓN MASIVA DESDE EL GRUPO {EMPEZAR_EN_GRUPO}")
    print("------------------------------------------------")

    if not os.path.exists(ARCHIVO_FAMILIAS):
        print(f"❌ Error: Falta el archivo '{ARCHIVO_FAMILIAS}'.")
        return

    with open(ARCHIVO_FAMILIAS, "r", encoding="utf-8") as f:
        familias = json.load(f)

    total_familias = len(familias)
    print(f"📂 Total grupos: {total_familias}.\n")

    contador = 1
    for nombre_familia, ids_miembros in familias.items():
        if contador < EMPEZAR_EN_GRUPO:
            contador += 1
            continue 

        print(f"🔨 Grupo {contador}/{total_familias}: {nombre_familia} ({len(ids_miembros)} productos)")
        for id_producto in ids_miembros:
            conectar_producto(id_producto, ids_miembros)
        contador += 1

    print("\n------------------------------------------------")
    print("🎉 ¡PROCESO TERMINADO! Ya puedes correr los siguientes scripts.")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()