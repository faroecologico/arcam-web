import csv
import re
import unicodedata
import json
import os
from collections import defaultdict

# =========================
# ⚙️ CONFIGURACIÓN
# =========================

# TU RUTA EXACTA (Usamos r"..." para que Windows lea bien las barras)
CANDIDATE_PATHS = [
    r"C:\Users\usuario_tr7\Desktop\Archivos de reportes Enero 2025\arcam-web\Stock-actual_Nueva-sucursal-zapallar_18-01-2026_1768703881.csv",
]

# False = Solo crea familia si hay 2 o más variantes. True = Incluye productos únicos.
INCLUDE_SINGLETONS = False

# =========================
# 🧹 DICCIONARIOS DE LIMPIEZA
# =========================

SIZE_LABELS = {
    "TALLA", "TALLAS", "SIZE", "NUM", "NUMERO", "NRO", "NRO.", "N", "NO", "NR",
}

SIZE_TOKENS = {
    "XS", "S", "M", "L", "XL", "XXL", "XXXL", "XXXXL", "UNICA", "UNICO",
    "S/M", "M/L", "L/XL", "XL/XXL", "M-L", "S-M", "L-XL", "XL-XXL",
}

COLOR_TOKENS = {
    "ROJO", "AZUL", "VERDE", "NEGRO", "BLANCO", "AMARILLO", "NARANJO", "NARANJA",
    "GRIS", "CAFE", "MARRON", "BEIGE", "CELESTE", "FUCSIA", "MORADO", "VIOLETA",
    "ROSADO", "DORADO", "PLATA", "PLATEADO", "TRANSPARENTE",
    "GRAFITO", "KHAKI", "BRONCE", "COBRE", "CROMADO", "TITANIO", "TITANIUM",
    "NATURAL", "FLUOR", "FLUORESCENTE",
}

COLOR_MODIFIERS = {
    "CLARO", "OSCURO", "MARINO", "PASTEL",
}

PACKAGING_TOKENS = {
    "UNIDAD", "UNIDADES", "UN", "UND", "U",
    "PAR", "PARES",
    "PACK", "SET", "JUEGO", "KIT",
    "CAJA", "BOLSA", "SACO", "ROLLO",
    "BOT", "BOTELLA", "BID", "BIDON", "ENVASE",
    "PZ", "PZA", "PZAS", "PCS", "PC",
}

# INCLUYE TUS UNIDADES ESPECIALES (KILOS, LITROS)
UNITS = {
    "MM", "CM", "M", "MT", "MTS", "METRO", "METROS",
    "L", "LT", "LTS", "LITRO", "LITROS", "ML",
    "G", "GR", "GRS", "GRAMO", "GRAMOS", "KG", "KILO", "KILOS", "OZ", "LB",
    "W", "KW", "V", "KV", "A", "AMP", "AMPS",
    "VAC", "VDC", "CC",
    "AWG", "BTU", "HP", "PSI", "BAR", "RPM",
    "PULG", "PULGADAS",
}

KEEP_NUMBER_CONTEXT = {
    "CLASE", "CATEGORIA", "CATEG", "CAT", "TIPO", "GRADO", "SERIE", "SAE", "ISO", "ANSI",
    "COD", "CODIGO", "COD.", "MOD", "MODELO", "MODEL", "REF", "NU",
}

COMMON_MEASURE_NUMBERS = {
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12,
    13, 14, 15, 16, 18, 19, 20, 22, 24, 25, 26, 28, 30, 32, 35, 38, 40, 42, 45, 48, 50,
    55, 60, 63, 70, 75, 80, 90, 100, 110, 125, 160, 200, 250,
}

COMBINED_MEASURE_RE = re.compile(r"^\d+(?:[.,]\d+)?(MM|CM|M|MT|LT|L|ML|G|GR|KG|OZ|LB|W|KW|V|KV|A|AMP|AMPS|AWG|BTU|HP|PSI|BAR|RPM|VAC|VDC|CC)$")
FRACTION_RE = re.compile(r"^\d+/\d+$")
DIM_RE = re.compile(r"^\d+(?:[.,]\d+)?(?:X\d+(?:[.,]\d+)?)+$")
DECIMAL_NUMBER_RE = re.compile(r"^\d+[.,]\d+$") # Detecta 7,5

# =========================
# 🧠 LÓGICA DE LIMPIEZA
# =========================

def strip_accents(text: str) -> str:
    text = unicodedata.normalize("NFKD", str(text))
    return "".join(c for c in text if not unicodedata.combining(c))

def normalize_product_name(name: str) -> str:
    s = strip_accents(name).upper().strip()
    s = re.sub(r"^(?:\s*FERR\.?\s*[-–—]*\s*)+", "", s)
    s = re.sub(r"(?<=\d)(?=[A-Z])|(?<=[A-Z])(?=\d)", " ", s)
    s = re.sub(r'[^A-Z0-9%/.,"]+', " ", s) 
    s = re.sub(r"\s+", " ", s).strip()
    return s

def is_color_combo(tok: str) -> bool:
    if "/" not in tok: return False
    parts = [p for p in tok.split("/") if p]
    return len(parts) >= 2 and all(p in COLOR_TOKENS for p in parts)

def remove_color_tail(tokens: list[str]) -> bool:
    if not tokens: return False
    t = tokens[-1]
    prev = tokens[-2] if len(tokens) >= 2 else None
    
    if t.isdigit() and len(t) <= 3 and prev and (prev in COLOR_TOKENS or prev in COLOR_MODIFIERS):
        tokens.pop(); tokens.pop()
        if tokens and tokens[-1] in COLOR_TOKENS: tokens.pop()
        return True
    
    if t in COLOR_MODIFIERS and prev and prev in COLOR_TOKENS:
        tokens.pop(); tokens.pop(); return True
    
    if t in COLOR_TOKENS or is_color_combo(t):
        tokens.pop()
        if tokens and tokens[-1] in COLOR_MODIFIERS: tokens.pop()
        return True
    return False

def tail_has_measure_indicator(tokens: list[str]) -> bool:
    tail = tokens[-8:] if len(tokens) > 8 else tokens
    for tok in tail:
        if tok in UNITS or tok == "X" or '"' in tok or "/" in tok: return True
        if COMBINED_MEASURE_RE.match(tok) or DIM_RE.match(tok): return True
    return False

def is_measure_piece(tok: str) -> bool:
    if tok in UNITS or tok == "X" or COMBINED_MEASURE_RE.match(tok) or DIM_RE.match(tok): return True
    if '"' in tok or FRACTION_RE.match(tok): return True
    if tok.isdigit() and len(tok) <= 3: return True
    if DECIMAL_NUMBER_RE.match(tok): return True 
    return False

def remove_measure_tail(tokens: list[str]) -> bool:
    if not tokens or not tail_has_measure_indicator(tokens): return False
    removed = False
    while tokens and is_measure_piece(tokens[-1]):
        tokens.pop()
        removed = True
    return removed

def prettify_root(root: str) -> str:
    parts = root.split()
    out = []
    for p in parts:
        if p.isdigit() or "/" in p or "%" in p: out.append(p)
        elif re.fullmatch(r"[A-Z0-9]{1,4}", p) or re.fullmatch(r"[A-Z]+[0-9]+[A-Z0-9]*", p): out.append(p)
        else: out.append(p.lower().capitalize())
    return " ".join(out)

def extract_root(product_name: str) -> str:
    s = normalize_product_name(product_name)
    tokens = s.split()
    if not tokens: return s

    while True:
        changed = False
        if tokens and tokens[-1] in PACKAGING_TOKENS:
            tokens.pop(); changed = True; continue
        
        if tokens and tokens[-1].isdigit() and len(tokens[-1]) <= 2:
            n = int(tokens[-1])
            if 20 <= n <= 60:
                tokens.pop()
                if tokens and tokens[-1] in SIZE_LABELS: tokens.pop()
                changed = True; continue
        
        if tokens and tokens[-1] in SIZE_TOKENS:
            tokens.pop()
            if tokens and tokens[-1] in SIZE_LABELS: tokens.pop()
            changed = True; continue
            
        if tokens and tokens[-1] in SIZE_LABELS:
            tokens.pop(); changed = True; continue
            
        if remove_color_tail(tokens): changed = True; continue
        if remove_measure_tail(tokens): changed = True; continue
        
        if tokens and tokens[-1].isdigit():
            n = int(tokens[-1])
            prev = tokens[-2] if len(tokens) >= 2 else ""
            if (n in COMMON_MEASURE_NUMBERS) and (prev not in KEEP_NUMBER_CONTEXT) and (not re.fullmatch(r"[A-Z]{1,3}", prev)):
                tokens.pop(); changed = True; continue
        
        if not changed: break
    
    root = " ".join(tokens).strip()
    return root if root else s

def unique_preserve(seq: list[str]) -> list[str]:
    seen = set()
    out = []
    for x in seq:
        if x not in seen: seen.add(x); out.append(x)
    return out

# =========================
# 🚀 EJECUCIÓN PRINCIPAL
# =========================

def main():
    print("------------------------------------------------")
    print("GENERADOR DE FAMILIAS INTELIGENTE")
    print("------------------------------------------------")

    file_path = None
    for p in CANDIDATE_PATHS:
        if os.path.exists(p):
            file_path = p
            break
            
    if file_path is None:
        print("Error: No encuentro el archivo CSV.")
        print(f"   Ruta buscada: {CANDIDATE_PATHS[0]}")
        return

    print(f"Procesando archivo: {file_path}")
    families = defaultdict(list)

    try:
        with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
            # Detectar si usa ; o , automáticamente
            sample = f.read(2048)
            f.seek(0)
            sniffer = csv.Sniffer()
            try:
                dialect = sniffer.sniff(sample)
            except:
                print("No pude detectar el delimitador automáticamente. Usando punto y coma (;).")
                class Dialect: delimiter = ';'
                dialect = Dialect()
            
            reader = csv.DictReader(f, dialect=dialect)
            
            count = 0
            for row in reader:
                producto = row.get("Producto", "")
                sku = str(row.get("SKU", "")).strip()

                if not sku or sku.lower() == "nan": continue

                root = extract_root(producto)
                family_name = prettify_root(root)
                families[family_name].append(sku)
                count += 1
                
            print(f"Se analizaron {count} productos.")

    except Exception as e:
        print(f"Error crítico leyendo el CSV: {e}")
        return

    # Filtrar familias con variantes
    if INCLUDE_SINGLETONS:
        FAMILIAS_SKU = {k: unique_preserve(v) for k, v in sorted(families.items(), key=lambda kv: kv[0])}
    else:
        FAMILIAS_SKU = {
            k: unique_preserve(v)
            for k, v in sorted(families.items(), key=lambda kv: kv[0])
            if len(set(v)) >= 2
        }

    print(f"Se detectaron {len(FAMILIAS_SKU)} familias de variantes.")

    # Guardar Resultado
    output_file = "mapa_variantes.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(FAMILIAS_SKU, f, indent=4)

    print(f"Archivo '{output_file}' creado exitosamente.")
    print("LISTO. Ahora ejecuta el siguiente script: python conectar_desde_json.py")

if __name__ == "__main__":
    main()