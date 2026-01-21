# INSTRUCCIONES: Manejo de productos_sin_imagen_final.csv

## ¿Qué es este archivo?
Este CSV contiene todos los productos que NO pudieron obtener una imagen de manera automática
después de ejecutar el script de búsqueda web.

## Estructura del CSV
- **ID**: ID del producto en WooCommerce
- **SKU**: Código único del producto
- **Nombre**: Nombre completo del producto
- **Categorías**: Categorías actuales del producto

---

## OPCIÓN 1: Asignación Manual de Imágenes (Recomendado para pocos productos)

### Pasos:
1. Abre el CSV en Excel o Google Sheets
2. Para cada producto:
   - Busca manualmente la imagen en Google/Bing
   - Descarga la imagen a tu PC
   - Ve a: https://arcam.cl/wp-admin/post.php?post=REEMPLAZA_CON_ID&action=edit
   - En el panel derecho "Imagen del producto", haz clic en "Establecer imagen"
   - Sube la imagen descargada

---

## OPCIÓN 2: Asignación Masiva con Script Python (Recomendado para muchos productos)

### Caso A: Tienes las imágenes en una carpeta local

1. **Organiza tus imágenes** en una carpeta (ej: `imagenes_productos/`)
   - Renombra cada imagen con el SKU o ID del producto
   - Ejemplo: `12345.jpg` o `PRODUCTO123.png`

2. **Ejecuta el script de asignación local:**
   ```bash
   python asignar_imagenes_local.py
   ```
   (Este script ya existe en tu proyecto)

### Caso B: Tienes URLs de imágenes

1. **Agrega una nueva columna al CSV** llamada `URL_IMAGEN`
2. Rellena con las URLs directas de cada imagen
3. **Crea y ejecuta un script como este:**

```python
import csv
import requests
from dotenv import load_dotenv
from base64 import b64encode
import os

load_dotenv()
WOO_URL = os.getenv("WOO_URL")
WOO_KEY = os.getenv("WOO_KEY")
WOO_SECRET = os.getenv("WOO_SECRET")

def get_headers():
    credentials = f"{WOO_KEY}:{WOO_SECRET}"
    token = b64encode(credentials.encode()).decode("utf-8")
    return {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

with open('productos_sin_imagen_final.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pid = row['ID']
        url_img = row['URL_IMAGEN']
        
        if url_img:
            # Descargar y subir imagen aquí (similar al script principal)
            print(f"Procesando producto {pid}...")
```

---

## OPCIÓN 3: Re-ejecutar búsqueda con términos mejorados

Para productos específicos que el script no encontró, puedes:

1. **Editar manualmente el nombre en WooCommerce** para que sea más específico
   - Ejemplo: "POLAR QUEBEC" → "Polerón Polar Quebec marca XYZ"
   
2. **Re-ejecutar el script solo para esos productos** filtrando por categoría:
   ```python
   # Modificar línea 164 del script:
   endpoint = f"{WOO_URL}/wp-json/wc/v3/products?category=64&status=publish&per_page=25&page={page}"
   ```

---

## ¿Cuántos productos sin imagen es normal?

- **Menos de 50**: Asignación manual es viable
- **Entre 50-200**: Usa script con URLs o carpeta local
- **Más de 200**: Considera contratar un servicio de fotografía de productos

---

## Tip Extra: Placeholder genérico

Si quieres que ningún producto quede "vacío" mientras consigues las imágenes reales:

1. Crea una imagen placeholder profesional (ej: logo de Arcam + "Imagen próximamente")
2. Asígnala masivamente a todos los productos sin imagen
3. Reemplázalas gradualmente con las reales

**Script para asignar placeholder:**
```python
# Ver script: asignar_placeholder.py (crear si no existe)
```
