"""
Script para generar tags/palabras clave para categorías de WooCommerce
Esto ayudará a mejorar la búsqueda y asociación de productos a categorías

Uso:
    python generar_tags_categorias.py
"""

import sys
import io
import json
import csv
import os
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

# Diccionario de tags/palabras clave para cada categoría
# Estos tags ayudarán a encontrar productos relacionados con cada categoría
CATEGORY_TAGS = {
    "Zapatos de Seguridad": [
        "zapato", "zapatos", "calzado", "bota", "botas", "botín", "botines",
        "seguridad", "seguro", "protección", "protector",
        "punta", "acero", "composite", "steel", "toe",
        "dielectrico", "dieléctrico", "antideslizante", "anti-deslizante",
        "cuero", "pu", "poliuretano", "nobuck", "nobuk",
        "trabajo", "industrial", "construcción", "minero", "minera",
        "cat", "caterpillar", "timberland", "apache", "workshoe", "work shoe",
        "safety", "boot", "shoe", "footwear"
    ],
    
    "Cascos": [
        "casco", "cascos", "helmet", "helmets",
        "seguridad", "protección", "cabeza", "craneal",
        "obra", "construcción", "minero", "minera", "industrial",
        "barboquejo", "barbiquejo", "suspensión",
        "tipo", "clase", "dieléctrico", "dielectrico",
        "msa", "3m", "north", "v-gard",
        "hard hat", "safety helmet", "head protection"
    ],
    
    "Polar": [
        "polar", "polares", "fleece",
        "chaqueta", "jacket", "casaca", "polerón", "poleron",
        "abrigo", "térmico", "termico", "calor", "frio", "frío",
        "manga", "larga", "cuello", "cierre", "zip", "zipper",
        "microfleece", "micro", "softshell", "soft shell",
        "invierno", "winter", "warm", "cold"
    ],
    
    "Chaleco Geólogo": [
        "chaleco", "vest", "chalecos", "vests",
        "geólogo", "geologo", "geologist", "topógrafo", "topografo",
        "bolsillos", "pockets", "reflectante", "reflective",
        "naranja", "amarillo", "orange", "yellow", "green", "verde",
        "malla", "mesh", "tela", "fabric",
        "seguridad", "safety", "visibility", "visibilidad", "alta",
        "trabajo", "work", "outdoor", "campo", "terreno"
    ],
    
    "Guantes": [
        "guante", "guantes", "glove", "gloves",
        "mano", "manos", "hand", "hands", "dedos", "fingers",
        "protección", "protection", "seguridad", "safety",
        "nitrilo", "latex", "látex", "cuero", "leather", "nylon",
        "mecánico", "mecanico", "mechanic", "soldador", "welder",
        "anticorte", "anti-corte", "cut", "resistant",
        "térmico", "termico", "thermal", "frio", "frío", "cold",
        "trabajo", "industrial", "construcción", "construction"
    ],
    
    "Lentes de Seguridad": [
        "lentes", "lente", "anteojos", "antiparras", "gafas",
        "glasses", "goggles", "eyewear", "safety glasses",
        "protección", "protection", "ocular", "ojos", "eye", "eyes",
        "claro", "oscuro", "clear", "dark", "smoke", "espejo", "mirror",
        "policarbonato", "polycarbonate", "anti-empañante", "anti-fog",
        "uv", "ultravioleta", "sol", "sun",
        "seguridad", "safety", "industrial", "work",
        "3m", "honeywell", "uvex", "steelpro"
    ],
    
    "Arnés": [
        "arnés", "arnes", "harness",
        "altura", "height", "caída", "caida", "fall", "anticaídas", "anticaidas",
        "cuerpo", "body", "completo", "full",
        "mosquetón", "mosqueton", "gancho", "hook", "clip",
        "eslinga", "lanyard", "cuerda", "rope", "línea", "linea", "life",
        "absorvedor", "absorbedor", "absorber", "shock",
        "seguridad", "safety", "protección", "protection",
        "trabajo", "altura", "vertical", "climbing", "escalada"
    ],
    
    "Ropa de Trabajo": [
        "pantalón", "pantalon", "pants", "trousers",
        "camisa", "shirt", "polera", "polo",
        "overol", "overall", "coverall", "buzo",
        "chaqueta", "jacket", "parka", "casaca",
        "trabajo", "work", "laboral", "industrial",
        "jean", "denim", "drill", "gabardina",
        "reforzado", "reinforced", "resistente", "durable",
        "cargo", "bolsillos", "pockets",
        "talla", "size", "color", "azul", "gris", "negro", "beige"
    ],
    
    "Protector Auditivo": [
        "protector", "protection", "audítivo", "auditivo", "hearing",
        "oído", "oidos", "ear", "ears", "oreja", "orejas",
        "tapón", "tapon", "plug", "plugs",
        "fonos", "fono", "auricular", "auriculares", "earmuff", "muff",
        "ruido", "noise", "sonido", "sound", "decibel", "db",
        "3m", "peltor", "howard", "leight",
        "seguridad", "safety", "industrial", "work"
    ],
    
    "Mascarilla": [
        "mascarilla", "mask", "respirador", "respirator",
        "protección", "protection", "respiratoria", "respiratory",
        "filtro", "filter", "cartucho", "cartridge",
        "polvo", "dust", "vapor", "gas", "humo", "smoke",
        "n95", "n99", "p100", "ffp2", "ffp3",
        "3m", "north", "msa", "honeywell",
        "desechable", "disposable", "reutilizable", "reusable",
        "media", "cara", "completa", "full", "face", "half"
    ]
}

def get_all_categories():
    """Obtener todas las categorías de WooCommerce"""
    print("📦 Obteniendo categorías de WooCommerce...")
    categories = []
    page = 1
    
    while True:
        try:
            response = wcapi.get("products/categories", params={
                "per_page": 100,
                "page": page
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
    
    print(f"✅ Se encontraron {len(categories)} categorías")
    return categories

def assign_tags_to_category(category_name, category_id):
    """Asignar tags a una categoría específica"""
    # Buscar coincidencias en el diccionario
    matched_tags = []
    
    for cat_key, tags in CATEGORY_TAGS.items():
        # Buscar coincidencia parcial (ej: "Zapatos" coincide con "Zapatos de Seguridad")
        if cat_key.lower() in category_name.lower() or category_name.lower() in cat_key.lower():
            matched_tags.extend(tags)
    
    # Si no hay coincidencia exacta, buscar por palabras clave en el nombre
    if not matched_tags:
        name_lower = category_name.lower()
        for cat_key, tags in CATEGORY_TAGS.items():
            # Buscar palabras individuales
            key_words = cat_key.lower().split()
            if any(word in name_lower for word in key_words if len(word) > 3):
                matched_tags.extend(tags)
    
    # Remover duplicados
    matched_tags = list(set(matched_tags))
    
    return matched_tags

def generate_category_tags_file():
    """Generar archivo JSON con tags para cada categoría"""
    categories = get_all_categories()
    
    category_tags_map = {}
    
    print("\n🏷️  Generando tags para categorías...")
    
    for category in categories:
        cat_id = category['id']
        cat_name = category['name']
        cat_slug = category['slug']
        
        # Asignar tags
        tags = assign_tags_to_category(cat_name, cat_id)
        
        category_tags_map[cat_slug] = {
            "id": cat_id,
            "name": cat_name,
            "slug": cat_slug,
            "tags": tags,
            "tag_count": len(tags)
        }
        
        if tags:
            print(f"  ✓ {cat_name}: {len(tags)} tags")
    
    # Guardar a archivo JSON
    output_file = "category_tags_map.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(category_tags_map, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Archivo generado: {output_file}")
    
    # Generar también un CSV para revisión
    csv_file = "category_tags_map.csv"
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Categoría', 'Slug', 'ID', 'Cantidad Tags', 'Tags'])
        
        for slug, data in category_tags_map.items():
            writer.writerow([
                data['name'],
                slug,
                data['id'],
                data['tag_count'],
                ', '.join(data['tags'][:10]) + ('...' if len(data['tags']) > 10 else '')
            ])
    
    print(f"✅ Archivo CSV generado: {csv_file}")
    
    # Estadísticas
    total_cats = len(category_tags_map)
    cats_with_tags = sum(1 for data in category_tags_map.values() if data['tag_count'] > 0)
    
    print(f"\n📊 Estadísticas:")
    print(f"  • Total de categorías: {total_cats}")
    print(f"  • Categorías con tags: {cats_with_tags}")
    print(f"  • Categorías sin tags: {total_cats - cats_with_tags}")
    
    return category_tags_map

def add_more_tags():
    """Función para agregar más tags personalizados"""
    print("\n" + "="*60)
    print("AGREGAR TAGS PERSONALIZADOS")
    print("="*60)
    print("\nPuedes editar este script y agregar más categorías y tags")
    print("en el diccionario CATEGORY_TAGS al inicio del archivo.")
    print("\nPara agregar tags automáticamente usando IA, ejecuta:")
    print("  python generar_tags_ia.py")

if __name__ == "__main__":
    print("="*60)
    print("GENERADOR DE TAGS PARA CATEGORÍAS DE WOOCOMMERCE")
    print("="*60)
    
    try:
        category_tags_map = generate_category_tags_file()
        add_more_tags()
        
        print("\n✅ Proceso completado exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error en el proceso: {e}")
        import traceback
        traceback.print_exc()
