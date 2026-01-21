"""
Script para aplicar búsqueda mejorada con tags de categorías
Este script recategoriza productos basándose en tags/palabras clave

Uso:
    python aplicar_busqueda_tags.py
"""

import json
import os
import sys
import io
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

def load_category_tags():
    """Cargar el mapa de tags de categorías"""
    # Intentar cargar el archivo generado por IA primero
    if os.path.exists("category_tags_generated.json"):
        print("📂 Cargando tags generados por IA...")
        with open("category_tags_generated.json", "r", encoding="utf-8") as f:
            return json.load(f)
    # Si no existe, usar el archivo manual
    elif os.path.exists("category_tags_map.json"):
        print("📂 Cargando tags manuales...")
        with open("category_tags_map.json", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        print("❌ No se encontró archivo de tags. Ejecuta primero:")
        print("   python generar_tags_categorias.py")
        print("   o")
        print("   python generar_tags_ia.py")
        return None

def find_matching_categories(product_name, category_tags_map):
    """Encontrar categorías que coincidan con el nombre del producto"""
    product_name_lower = product_name.lower()
    matches = []
    
    for cat_slug, cat_data in category_tags_map.items():
        tags = cat_data.get('tags', [])
        match_count = 0
        matched_tags = []
        
        # Contar coincidencias de tags
        for tag in tags:
            tag_lower = tag.lower()
            if tag_lower in product_name_lower:
                match_count += 1
                matched_tags.append(tag)
        
        if match_count > 0:
            matches.append({
                'category_id': cat_data['id'],
                'category_name': cat_data['name'],
                'category_slug': cat_slug,
                'match_count': match_count,
                'matched_tags': matched_tags
            })
    
    # Ordenar por número de coincidencias
    matches.sort(key=lambda x: x['match_count'], reverse=True)
    
    return matches

def get_all_products(limit=None):
    """Obtener todos los productos"""
    print("📦 Obteniendo productos de WooCommerce...")
    products = []
    page = 1
    
    while True:
        if limit and len(products) >= limit:
            break
            
        try:
            response = wcapi.get("products", params={
                "per_page": 100,
                "page": page,
                "status": "publish"
            })
            
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break
                products.extend(data)
                page += 1
                
                print(f"  • Página {page-1}: {len(data)} productos")
            else:
                print(f"❌ Error: {response.status_code}")
                break
        except Exception as e:
            print(f"❌ Error: {e}")
            break
    
    final_count = len(products) if not limit else min(len(products), limit)
    print(f"✅ Total: {final_count} productos")
    
    return products[:limit] if limit else products

def analyze_products_with_tags(products, category_tags_map):
    """Analizar productos y sugerir recategorizaciones"""
    print("\n🔍 Analizando productos con tags...")
    
    suggestions = []
    uncategorized = []
    
    for product in products:
        product_id = product['id']
        product_name = product['name']
        current_categories = product.get('categories', [])
        
        # Buscar categorías coincidentes
        matches = find_matching_categories(product_name, category_tags_map)
        
        if matches:
            # Si el producto no tiene categorías o tiene muy pocas coincidencias
            if not current_categories or len(current_categories) == 0:
                suggestions.append({
                    'product_id': product_id,
                    'product_name': product_name,
                    'current_categories': [],
                    'suggested_categories': matches[:3],  # Top 3 sugerencias
                    'priority': 'high'
                })
            else:
                # Verificar si las categorías actuales coinciden con las sugeridas
                current_cat_ids = [cat['id'] for cat in current_categories]
                suggested_cat_ids = [m['category_id'] for m in matches[:3]]
                
                # Si no hay coincidencia, sugerir reclasificación
                if not any(cid in current_cat_ids for cid in suggested_cat_ids):
                    suggestions.append({
                        'product_id': product_id,
                        'product_name': product_name,
                        'current_categories': current_categories,
                        'suggested_categories': matches[:3],
                        'priority': 'medium'
                    })
        else:
            # No se encontraron coincidencias
            uncategorized.append({
                'product_id': product_id,
                'product_name': product_name,
                'current_categories': current_categories
            })
    
    return suggestions, uncategorized

def save_suggestions(suggestions, uncategorized):
    """Guardar sugerencias de recategorización"""
    # Guardar sugerencias
    suggestions_file = "sugerencias_recategorizacion.json"
    with open(suggestions_file, 'w', encoding='utf-8') as f:
        json.dump(suggestions, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Sugerencias guardadas en: {suggestions_file}")
    
    # Guardar productos sin categoría
    uncategorized_file = "productos_sin_coincidencias_tags.json"
    with open(uncategorized_file, 'w', encoding='utf-8') as f:
        json.dump(uncategorized, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Productos sin coincidencias guardados en: {uncategorized_file}")
    
    # Estadísticas
    high_priority = sum(1 for s in suggestions if s['priority'] == 'high')
    medium_priority = sum(1 for s in suggestions if s['priority'] == 'medium')
    
    print(f"\n📊 Estadísticas:")
    print(f"  • Productos con sugerencias (alta prioridad): {high_priority}")
    print(f"  • Productos con sugerencias (media prioridad): {medium_priority}")
    print(f"  • Productos sin coincidencias: {len(uncategorized)}")

def apply_suggestions_to_woocommerce(suggestions, dry_run=True):
    """Aplicar sugerencias de recategorización a WooCommerce"""
    print(f"\n{'🧪 MODO PRUEBA' if dry_run else '⚡ APLICANDO CAMBIOS'}...")
    
    # Filtrar solo sugerencias de alta prioridad (productos sin categoría)
    high_priority = [s for s in suggestions if s['priority'] == 'high']
    
    print(f"\n📝 Procesando {len(high_priority)} productos sin categoría...")
    
    for i, suggestion in enumerate(high_priority[:50], 1):  # Limitar a 50 para prueba
        product_id = suggestion['product_id']
        product_name = suggestion['product_name']
        suggested = suggestion['suggested_categories']
        
        if not suggested:
            continue
        
        # Tomar la categoría con más coincidencias
        best_match = suggested[0]
        category_id = best_match['category_id']
        category_name = best_match['category_name']
        
        print(f"\n{i}. {product_name[:50]}...")
        print(f"   → Asignar a: {category_name} (coincidencias: {best_match['match_count']})")
        print(f"   → Tags: {', '.join(best_match['matched_tags'][:5])}")
        
        if not dry_run:
            try:
                # Actualizar producto
                response = wcapi.put(f"products/{product_id}", {
                    "categories": [{"id": category_id}]
                })
                
                if response.status_code == 200:
                    print("   ✅ Actualizado")
                else:
                    print(f"   ❌ Error: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    if dry_run:
        print("\n" + "="*70)
        print("MODO PRUEBA ACTIVO - No se realizaron cambios")
        print("="*70)
        print("\nPara aplicar los cambios, ejecuta:")
        print("  python aplicar_busqueda_tags.py --apply")

if __name__ == "__main__":
    import sys
    
    print("="*70)
    print("APLICAR BÚSQUEDA MEJORADA CON TAGS")
    print("="*70)
    
    try:
        # Cargar tags
        category_tags_map = load_category_tags()
        
        if not category_tags_map:
            sys.exit(1)
        
        # Obtener productos (limitar a 500 para prueba inicial)
        products = get_all_products(limit=500)
        
        # Analizar
        suggestions, uncategorized = analyze_products_with_tags(products, category_tags_map)
        
        # Guardar
        save_suggestions(suggestions, uncategorized)
        
        # Aplicar (modo prueba por defecto)
        dry_run = "--apply" not in sys.argv
        if suggestions:
            apply_suggestions_to_woocommerce(suggestions, dry_run=dry_run)
        
        print("\n✅ Análisis completado!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
