import requests
import json
import os
from dotenv import load_dotenv
from base64 import b64encode

load_dotenv()

# --- TUS CREDENCIALES ---
WOO_URL = os.getenv("WOO_URL")
WOO_KEY = os.getenv("WOO_KEY")
WOO_SECRET = os.getenv("WOO_SECRET")


# --- LA CLAVE MAESTRA DEL PLUGIN WPCLEVER ---
CLAVE_WPC = os.getenv("CLAVE_PLUGIN")

def get_headers():
    credentials = f"{WOO_KEY}:{WOO_SECRET}"
    token = b64encode(credentials.encode()).decode("utf-8")
    return { "Authorization": f"Basic {token}", "Content-Type": "application/json" }

def probar_union():
    print("------------------------------------------------")
    print("🧪 PRUEBA DEFINITIVA CON WPC LINKED VARIATION")
    print("------------------------------------------------")
    
    id_1 = input("1. ID del primer producto (ej: Kimono Verde 6454): ")
    id_2 = input("2. ID del segundo producto (ej: Kimono Rojo): ")
    
    print(f"\n⚙️  Vinculando el producto {id_2} dentro del {id_1}...")

    # El plugin espera una lista de IDs con los que se conecta
    data = {
        "meta_data": [
            {
                "key": CLAVE_WPC,
                "value": [int(id_2)] 
            }
        ]
    }
    
    url = f"{WOO_URL}/wp-json/wc/v3/products/{id_1}"
    r = requests.put(url, headers=get_headers(), json=data)
    
    if r.status_code == 200:
        print("\n✅ ¡ÉXITO! El servidor guardó el cambio.")
        print(f"👉 Ve a WordPress, edita el producto {id_1} y mira la pestaña 'Linked Variations'.")
        print(f"   ¿Aparece el producto {id_2} en la lista?")
    else:
        print(f"\n❌ Falló: {r.status_code}")
        print(r.text)

if __name__ == "__main__":
    probar_union()