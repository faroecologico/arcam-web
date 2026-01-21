"""
Script para generar tags de categorías usando IA basándose en productos reales
Este script analiza los productos de cada categoría y genera tags relevantes

NOTA: Este script prepara un CSV con productos por categoría que luego puedes
enviar a una IA (como ChatGPT, Claude, Gemini) para que genere los tags automáticamente.

Uso:
    python generar_tags_ia.py
"""

import json
import csv
import os
import sys
import io
from collections import defaultdict
from dotenv import load_dotenv
from woocommerce import API

# Configurar encoding para Windows
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Cargar variables de entorno
load_dotenv()

# Configuración de WooCommerce
wcapi = API(
    url=os.getenv("WOO_URL"),
    consumer_key=os.getenv("WOO_KEY"),
    consumer_secret=os.getenv("WOO_SECRET"),
    version="wc/v3",
    timeout=30
)

def get_all_categories():
    """Obtener todas las categorías de WooCommerce"""
    print("📦 Obteniendo categorías de WooCommerce...")
    categories = []
    page = 1
    
    while True:
        try:
            response = wcapi.get("products/categories", params={
                "per_page": 100,
                "page": page,
                "hide_empty": True  # Solo categorías con productos
            })
            
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break
                categories.extend(data)
                page += 1
            else:
                print(f"❌ Error al obtener categorías: {response.status_code}")
                break
        except Exception as e:
            print(f"❌ Error: {e}")
            break
    
    print(f"✅ Se encontraron {len(categories)} categorías con productos")
    return categories

def get_products_by_category(category_id, limit=50):
    """Obtener productos de una categoría específica"""
    products = []
    page = 1
    
    while len(products) < limit:
        try:
            response = wcapi.get("products", params={
                "category": str(category_id),
                "per_page": min(100, limit - len(products)),
                "page": page,
                "status": "publish",
                "stock_status": "instock"
            })
            
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break
                products.extend(data)
                page += 1
                
                if len(data) < 100:  # Última página
                    break
            else:
                break
        except Exception as e:
            print(f"   ⚠️  Error al obtener productos: {e}")
            break
    
    return products[:limit]

def extract_keywords_from_products(products):
    """Extraer palabras clave de los nombres de productos"""
    keywords = defaultdict(int)
    
    for product in products:
        name = product.get('name', '').upper()
        
        # Limpiar el nombre
        name = name.replace('FERR.', '').replace('FERRE.', '').strip()
        
        # Dividir en palabras
        words = name.split()
        
        for word in words:
            # Ignorar palabras muy cortas o números de talla
            if len(word) < 3:
                continue
            if word.startswith('TALLA'):
                continue
            if word.startswith('N°') or word.startswith('#'):
                continue
            if word in ['DE', 'LA', 'EL', 'LOS', 'LAS', 'CON', 'SIN', 'PARA']:
                continue
            
            # Limpiar caracteres especiales
            word = word.strip('.,;:()[]{}')
            
            if word:
                keywords[word] += 1
    
    # Ordenar por frecuencia
    sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_keywords

def generate_ia_input_file():
    """Generar archivo CSV con información para que la IA genere tags"""
    categories = get_all_categories()
    
    category_data = []
    
    print("\n🔍 Analizando productos por categoría...")
    
    for category in categories:
        cat_id = category['id']
        cat_name = category['name']
        cat_slug = category['slug']
        cat_count = category.get('count', 0)
        
        print(f"\n📂 {cat_name} ({cat_count} productos)")
        
        # Obtener productos de muestra
        products = get_products_by_category(cat_id, limit=50)
        
        if not products:
            print("   ⚠️  Sin productos")
            continue
        
        # Extraer palabras clave
        keywords = extract_keywords_from_products(products)
        
        # Tomar top 20 keywords
        top_keywords = [kw[0] for kw in keywords[:20]]
        
        # Tomar nombres de 10 productos de muestra
        sample_names = [p.get('name', '') for p in products[:10]]
        
        category_data.append({
            'id': cat_id,
            'name': cat_name,
            'slug': cat_slug,
            'product_count': cat_count,
            'top_keywords': ', '.join(top_keywords),
            'sample_products': ' | '.join(sample_names)
        })
        
        print(f"   ✓ Top keywords: {', '.join(top_keywords[:5])}...")
    
    # Guardar a CSV para la IA
    csv_file = "categorias_para_ia.csv"
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'id', 'name', 'slug', 'product_count', 'top_keywords', 'sample_products'
        ])
        writer.writeheader()
        writer.writerows(category_data)
    
    print(f"\n✅ Archivo CSV generado: {csv_file}")
    
    # Generar también un JSON más estructurado
    json_file = "categorias_para_ia.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(category_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Archivo JSON generado: {json_file}")
    
    return category_data

def generate_ia_prompt():
    """Generar un prompt para usar con IA"""
    prompt_file = "prompt_para_ia.txt"
    
    prompt = """
INSTRUCCIONES PARA GENERAR TAGS DE CATEGORÍAS
==============================================

Analiza el archivo 'categorias_para_ia.csv' que contiene información sobre categorías de productos
de una ferretería industrial y tienda de ropa de trabajo.

Para cada categoría, genera una lista de 20-30 TAGS/PALABRAS CLAVE que:

1. INCLUYAN variaciones y sinónimos del nombre de la categoría
2. INCLUYAN términos técnicos relacionados
3. INCLUYAN marcas comunes en esa categoría
4. INCLUYAN términos en español e inglés
5. INCLUYAN variaciones de escritura (con/sin acentos, singular/plural)
6. INCLUYAN palabras relacionadas con el uso, características y aplicaciones

FORMATO DE SALIDA:
Genera un archivo JSON con la siguiente estructura:

{
  "nombre-de-categoria": {
    "id": 123,
    "name": "Nombre de Categoría",
    "slug": "nombre-de-categoria",
    "tags": [
      "tag1",
      "tag2",
      "tag3",
      ...
    ]
  },
  ...
}

EJEMPLOS DE TAGS CORRECTOS:

Para "Zapatos de Seguridad":
- zapato, zapatos, calzado, bota, botas, botín, botines
- seguridad, protección, protector
- punta de acero, steel toe, composite
- dielectrico, antideslizante, work boot
- cat, caterpillar, timberland

Para "Guantes":
- guante, guantes, glove, gloves
- nitrilo, latex, cuero, leather
- anticorte, cut resistant
- mecánico, soldador, térmico
- mano, dedos, protección

IMPORTANTE:
- Usa solo minúsculas
- Sin caracteres especiales (excepto guiones)
- Tags de 1-3 palabras máximo
- Prioriza términos que realmente ayuden en búsquedas

Genera el archivo JSON con todos los tags para todas las categorías.
"""
    
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    print(f"✅ Prompt generado: {prompt_file}")
    
    print("\n" + "="*70)
    print("SIGUIENTE PASO: USAR IA PARA GENERAR LOS TAGS")
    print("="*70)
    print("\n1. Abre ChatGPT, Claude, o Gemini")
    print("2. Sube el archivo 'categorias_para_ia.csv'")
    print("3. Copia y pega el contenido de 'prompt_para_ia.txt'")
    print("4. La IA generará un archivo JSON con todos los tags")
    print("5. Guarda el resultado como 'category_tags_generated.json'")
    print("\n" + "="*70)

if __name__ == "__main__":
    print("="*70)
    print("GENERADOR DE DATOS PARA IA - TAGS DE CATEGORÍAS")
    print("="*70)
    
    try:
        category_data = generate_ia_input_file()
        generate_ia_prompt()
        
        print("\n✅ Archivos generados exitosamente!")
        print("\nSigue las instrucciones para usar una IA y generar los tags.")
        
    except Exception as e:
        print(f"\n❌ Error en el proceso: {e}")
        import traceback
        traceback.print_exc()
