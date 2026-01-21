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

# ==========================================
# ⚙️ CONFIGURACIÓN
# ==========================================
# True = Pone en borrador (oculta) lo que NO tiene stock.
# False = Solo publica lo que TIENE stock (no oculta nada).
OCULTAR_SIN_STOCK = True 
# ==========================================

def get_headers():
    credentials = f"{WOO_KEY}:{WOO_SECRET}"
    token = b64encode(credentials.encode()).decode("utf-8")
    return { "Authorization": f"Basic {token}", "Content-Type": "application/json" }

def enviar_lote(lista_actualizaciones):
    """ Envía un paquete de hasta 100 actualizaciones de golpe """
    if not lista_actualizaciones: return

    print(f"   >> Enviando lote de {len(lista_actualizaciones)} productos...")
    
    url_batch = f"{WOO_URL}/wp-json/wc/v3/products/batch"
    payload = { "update": lista_actualizaciones }
    
    try:
        r = requests.post(url_batch, headers=get_headers(), json=payload, timeout=30)
        if r.status_code == 200:
            print("      [OK] Lote actualizado correctamente.")
        else:
            print(f"      [X] Error en lote: {r.status_code}")
    except Exception as e:
        print(f"      [!] Error de conexión enviando lote: {e}")

def main():
    print("------------------------------------------------")
    print("*** PUBLICADOR MASIVO DE STOCK")
    print("------------------------------------------------")
    
    page = 1
    lote_cambios = []
    total_procesados = 0
    
    while True:
        try:
            print(f"\n... Leyendo página {page}...")
            url = f"{WOO_URL}/wp-json/wc/v3/products?per_page=50&page={page}"
            r = requests.get(url, headers=get_headers(), timeout=30)
            
            if r.status_code != 200:
                print(f"[X] Fin o Error (Status {r.status_code}).")
                break
            
            productos = r.json()
            if not productos:
                print("[OK] Se revisaron todos los productos.")
                break
                
            for p in productos:
                pid = p['id']
                nombre = p['name']
                estado_actual = p['status']
                stock_status = p['stock_status'] # 'instock' o 'outofstock'
                stock_qty = p.get('stock_quantity')
                
                # Solo consideramos productos con un número positivo de stock
                tiene_stock = (stock_qty is not None and stock_qty > 0)
                
                nuevo_estado = None

                # CASO 1: Tiene stock pero está oculto -> PUBLICAR
                if tiene_stock and estado_actual != 'publish':
                    print(f"   [+] [PUBLICAR] {nombre} (Stock OK)")
                    nuevo_estado = 'publish'

                # CASO 2: No tiene stock y está visible -> BORRADOR (Si está activado)
                elif not tiene_stock and estado_actual == 'publish' and OCULTAR_SIN_STOCK:
                    print(f"   [-] [OCULTAR]  {nombre} (Sin Stock)")
                    nuevo_estado = 'draft' # 'draft' es borrador, 'private' es privado
                
                # Si hay cambio, lo agregamos al lote
                if nuevo_estado:
                    lote_cambios.append({
                        "id": pid,
                        "status": nuevo_estado
                    })
                    total_procesados += 1

                # Cuando juntamos 50 cambios, disparamos
                if len(lote_cambios) >= 50:
                    enviar_lote(lote_cambios)
                    lote_cambios = [] # Vaciamos el cargador
                    time.sleep(1) # Respiro al servidor

            page += 1
            
        except Exception as e:
            print(f"[!] Error en página {page}: {e}")
            time.sleep(5) # Espera de seguridad

    # Si quedaron cambios pendientes en el cargador al final, enviarlos
    if lote_cambios:
        enviar_lote(lote_cambios)

    print("\n------------------------------------------------")
    print(f"LISTO! Se actualizaron {total_procesados} productos.")
    print("------------------------------------------------")

if __name__ == "__main__":
    main()