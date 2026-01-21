import requests
import os
import time
from dotenv import load_dotenv
from base64 import b64encode

load_dotenv()

# --- CONFIGURACIÓN ---
WOO_URL = os.getenv("WOO_URL")
WOO_KEY = os.getenv("WOO_KEY")
WOO_SECRET = os.getenv("WOO_SECRET")

# Imagen de relleno (Placeholder)
PLACEHOLDER_IMAGE = "https://placehold.co/600x600/e2e8f0/1e293b.png?text=ARCAM"
# O alternativamente una imagen real si se prefiere:
# PLACEHOLDER_IMAGE = "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?auto=format&fit=crop&w=800&q=80" 

def get_headers():
    credentials = f"{WOO_KEY}:{WOO_SECRET}"
    token = b64encode(credentials.encode()).decode("utf-8")
    return { "Authorization": f"Basic {token}", "Content-Type": "application/json" }

def rellenar_imagenes_faltantes():
    print("------------------------------------------------")
    print(">> RELLENANDO IMAGENES FALTANTES")
    print("------------------------------------------------")
    
    page = 1
    per_page = 50
    headers = get_headers()
    updated_count = 0
    
    while True:
        try:
            print(f"Cargando página {page}...")
            url = f"{WOO_URL}/wp-json/wc/v3/products?page={page}&per_page={per_page}"
            r = requests.get(url, headers=headers, timeout=30)
            
            if r.status_code != 200:
                print(f"Error cargando página {page}: {r.status_code}")
                break
                
            products = r.json()
            if not products:
                break # Fin del inventario
            
            for p in products:
                product_id = p['id']
                product_name = p['name']
                images = p.get('images', [])
                
                # Si no tiene imágenes, asignamos la placeholder
                if not images:
                    print(f"   [SIN IMAGEN] ID {product_id} - {product_name[:30]}")
                    
                    update_payload = {
                        "images": [
                            {
                                "src": PLACEHOLDER_IMAGE,
                                "name": product_name,
                                "alt": product_name
                            }
                        ]
                    }
                    
                    try:
                        update_url = f"{WOO_URL}/wp-json/wc/v3/products/{product_id}"
                        ur = requests.put(update_url, headers=headers, json=update_payload, timeout=20)
                        
                        if ur.status_code in [200, 201]:
                            print(f"      -> Imagen asignada exitosamente.")
                            updated_count += 1
                        else:
                            print(f"      -> Error asignando imagen: {ur.status_code} - {ur.text}")
                            
                    except Exception as e:
                        print(f"      -> Excepción al actualizar: {e}")
                        
            page += 1
            
        except Exception as e:
            print(f"Error general en página {page}: {e}")
            break
            
    print("------------------------------------------------")
    print(f"Proceso finalizado. Total productos actualizados: {updated_count}")

if __name__ == "__main__":
    if not WOO_URL or not WOO_KEY:
        print("Error: Credenciales no encontradas en .env")
    else:
        rellenar_imagenes_faltantes()
