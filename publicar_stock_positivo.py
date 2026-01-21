import requests
import json
from base64 import b64encode
import time
import os
from dotenv import load_dotenv

load_dotenv()

# --- TUS CREDENCIALES ---
WOO_URL = os.getenv("WOO_URL")
WOO_KEY = os.getenv("WOO_KEY")
WOO_SECRET = os.getenv("WOO_SECRET") 

def get_headers():
    credentials = f"{WOO_KEY}:{WOO_SECRET}"
    token = b64encode(credentials.encode()).decode("utf-8")
    return { "Authorization": f"Basic {token}", "Content-Type": "application/json" }

def main():
    print("------------------------------------------------")
    print("📢 PUBLICANDO PRODUCTOS CON STOCK POSITIVO")
    print("------------------------------------------------")

    page = 1
    modificados = 0

    while True:
        # Pedimos productos de 100 en 100
        # Filtramos por 'status=draft' (o pending) para no revisar los que ya están publicados
        print(f"📄 Leyendo página {page} de borradores...")
        
        endpoint = f"{WOO_URL}/wp-json/wc/v3/products?status=draft&per_page=100&page={page}"
        r = requests.get(endpoint, headers=get_headers())
        
        if r.status_code != 200:
            print("❌ Fin o Error (posiblemente no hay más páginas).")
            break

        productos = r.json()
        if not productos:
            print("✅ No hay más productos borradores.")
            break

        for p in productos:
            p_id = p['id']
            stock = p.get('stock_quantity')
            nombre = p.get('name')

            # LÓGICA: Si el stock es None (infinito) o mayor a 0
            tiene_stock = (stock is not None and stock > 0) or (p.get('manage_stock') is False)

            if tiene_stock:
                print(f"   🟢 ID {p_id} tiene stock ({stock}). Publicando...")
                
                # Actualizamos a 'publish'
                update_url = f"{WOO_URL}/wp-json/wc/v3/products/{p_id}"
                data = {"status": "publish"}
                
                try:
                    requests.put(update_url, headers=get_headers(), json=data)
                    modificados += 1
                except:
                    print(f"   ⚠️ Error al publicar ID {p_id}")
            else:
                # Si no tiene stock, lo ignoramos (sigue en borrador)
                pass

        page += 1
        
    print("------------------------------------------------")
    print(f"🎉 ¡LISTO! Se publicaron {modificados} productos.")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()