import requests
import json
from base64 import b64encode

# --- TUS CREDENCIALES (YA ESTÁN PUESTAS) ---
WOO_URL="https://arcam.cl"
WOO_KEY="ck_8d962ed36abef8b8c11c34e22170e23361265281" 
WOO_SECRET="cs_5bc4372f8e356cf5d725ccdc9f8e1a7d9fa7f1ef" 

# --- AQUI ESTA EL CAMBIO: MIRAMOS EL KIMONO (6454) ---
ID_PRODUCTO_PADRE = 6454  

def get_headers():
    credentials = f"{WOO_KEY}:{WOO_SECRET}"
    token = b64encode(credentials.encode()).decode("utf-8")
    return { "Authorization": f"Basic {token}", "Content-Type": "application/json" }

def espiar_todo():
    print(f"------------------------------------------------")
    print(f"👁️  ANALIZANDO EL KIMONO VERDE (ID {ID_PRODUCTO_PADRE})...")
    print(f"------------------------------------------------")
    
    url = f"{WOO_URL}/wp-json/wc/v3/products/{ID_PRODUCTO_PADRE}"
    r = requests.get(url, headers=get_headers())
    
    if r.status_code != 200:
        print(f"❌ Error: {r.status_code}")
        return

    data = r.json()
    meta_data = data.get("meta_data", [])
    
    print("\n--- 🔑 DATOS ENCONTRADOS ---")
    encontrado = False
    for meta in meta_data:
        clave = meta['key']
        valor = meta['value']
        
        # Filtro para ver solo lo importante
        if "wpc" in clave or "linked" in clave or "ids" in clave or isinstance(valor, list):
             print(f"[{clave}]  ==>  {str(valor)}") 
             encontrado = True
    
    if not encontrado:
        print("⚠️ Sigue vacío. Asegúrate de haber presionado 'ACTUALIZAR' en el producto 6454.")

if __name__ == "__main__":
    espiar_todo()