# Solución de Búsqueda y Nombres de Productos

Esta solución resuelve los siguientes problemas:

## 🎯 Problemas Resueltos

### 1. **Zapatos de Seguridad sin productos**
- **Problema**: Al buscar "Zapatos de Seguridad" no aparecen resultados
- **Solución**: Sistema de tags/palabras clave para categorías que mejora la búsqueda y asociación de productos

### 2. **Nombres completos en búsquedas y catálogo**
- **Problema**: Los productos muestran nombres con variantes incluidas (ej: "PANTALON TÉRMICO FORRO POLAR MTX Talla L")
- **Solución**: Función centralizada `getCleanProductName()` que limpia los nombres en todo el frontend

### 3. **Títulos de productos con variantes**
- **Problema**: "POLAR P.JACK VPO400 DELTA VARON AZUL TALLA L" debería ser "POLAR P.JACK VPO400 DELTA"
- **Solución**: Los nombres ahora se limpian automáticamente removiendo colores, géneros, tallas, etc.

---

## 🚀 Cambios Realizados en Frontend

### Archivo: `src/lib/woocommerce.ts`
✅ **Nueva función `getCleanProductName()`**
- Remueve prefijos (FERR., FERRE.)
- Remueve tallas (TALLA X, TX, TL, etc.)
- Remueve colores (NEGRO, AZUL, ROJO, VERDE, AMARILLO, etc.)
- Remueve géneros (VARON, DAMA, HOMBRE, MUJER, UNISEX)
- Remueve dimensiones (42mm, 10kg, etc.)
- Remueve números de talla (N° 42, # 10)

✅ **Función `deduplicateProducts()` mejorada**
- Ahora usa la nueva función centralizada
- Agrupa productos por nombre base (sin variantes)
- Mantiene deduplicación inteligente

### Archivos actualizados para usar `getCleanProductName()`:
- ✅ `src/components/product/ProductCard.tsx`
- ✅ `src/components/product/ProductDetail.tsx`
- ✅ `src/app/api/search/route.ts`

### Resultado:
- **ANTES**: "POLAR P.JACK VPO400 DELTA VARON AZUL TALLA L"
- **AHORA**: "POLAR P.JACK VPO400 DELTA"

---

## 🏷️ Sistema de Tags para Categorías

### Scripts Creados

#### 1. **`generar_tags_categorias.py`**
Script con tags pre-configurados para las categorías principales:
- Zapatos de Seguridad
- Cascos
- Polar
- Chaleco Geólogo
- Guantes
- Lentes de Seguridad
- Arnés
- Ropa de Trabajo
- Protector Auditivo
- Mascarilla

**Uso:**
```bash
python generar_tags_categorias.py
```

**Salida:**
- `category_tags_map.json` - Mapa completo de tags por categoría
- `category_tags_map.csv` - Vista en CSV para revisión

#### 2. **`generar_tags_ia.py`**
Script avanzado que analiza productos reales y prepara datos para IA:
- Extrae keywords de nombres de productos
- Analiza productos por categoría
- Genera archivos para enviar a ChatGPT/Claude/Gemini

**Uso:**
```bash
python generar_tags_ia.py
```

**Salida:**
- `categorias_para_ia.csv` - Datos de categorías con keywords
- `categorias_para_ia.json` - Versión JSON
- `prompt_para_ia.txt` - Prompt listo para copiar a la IA

**Proceso con IA:**
1. Ejecutar el script
2. Abrir ChatGPT, Claude o Gemini
3. Subir el archivo `categorias_para_ia.csv`
4. Copiar y pegar el contenido de `prompt_para_ia.txt`
5. La IA generará tags automáticamente
6. Guardar como `category_tags_generated.json`

#### 3. **`aplicar_busqueda_tags.py`**
Script que aplica los tags para recategorizar productos:
- Analiza productos actuales
- Encuentra coincidencias basadas en tags
- Sugiere recategorizaciones
- Aplica cambios a WooCommerce

**Uso (modo prueba):**
```bash
python aplicar_busqueda_tags.py
```

**Uso (aplicar cambios):**
```bash
python aplicar_busqueda_tags.py --apply
```

**Salida:**
- `sugerencias_recategorizacion.json` - Productos con sugerencias
- `productos_sin_coincidencias_tags.json` - Productos sin matches

---

## 📋 Flujo de Trabajo Completo

### Opción A: Usar Tags Pre-configurados
```bash
# 1. Generar tags con diccionario incluido
python generar_tags_categorias.py

# 2. Analizar productos (modo prueba)
python aplicar_busqueda_tags.py

# 3. Revisar archivo: sugerencias_recategorizacion.json

# 4. Aplicar cambios
python aplicar_busqueda_tags.py --apply
```

### Opción B: Usar IA para Generar Tags
```bash
# 1. Generar datos para IA
python generar_tags_ia.py

# 2. Usar ChatGPT/Claude/Gemini con los archivos generados
# - subir categorias_para_ia.csv
# - usar prompt_para_ia.txt
# - guardar resultado como category_tags_generated.json

# 3. Analizar productos (modo prueba)
python aplicar_busqueda_tags.py

# 4. Revisar sugerencias

# 5. Aplicar cambios
python aplicar_busqueda_tags.py --apply
```

---

## 🎨 Ejemplos de Tags Generados

### Zapatos de Seguridad
```json
{
  "tags": [
    "zapato", "zapatos", "calzado", "bota", "botas", "botín", "botines",
    "seguridad", "protección", "punta de acero", "steel toe", "composite",
    "dielectrico", "antideslizante", "cat", "caterpillar", "timberland",
    "work boot", "safety shoe", "industrial"
  ]
}
```

### Polar
```json
{
  "tags": [
    "polar", "polares", "fleece", "chaqueta", "jacket", "casaca",
    "polerón", "abrigo", "térmico", "termico", "calor", "frio",
    "manga larga", "cuello", "cierre", "zip", "microfleece",
    "softshell", "invierno", "winter", "warm"
  ]
}
```

---

## 🔍 Cómo Funciona la Búsqueda Mejorada

### Antes:
- Búsqueda solo por nombre exacto
- "Zapatos de Seguridad" → Sin resultados
- Productos duplicados por variantes

### Ahora:
1. **Limpieza de nombres**: Todos los productos muestran solo su nombre base
2. **Deduplicación inteligente**: Agrupa variantes como un solo producto
3. **Búsqueda con tags**: Encuentra productos por sinónimos y términos relacionados
4. **Categorización mejorada**: Asigna automáticamente categorías basadas en keywords

### Ejemplo de Búsqueda:
- **Usuario busca**: "zapato seguridad"
- **Sistema encuentra**:
  - Productos en categoría "Zapatos de Seguridad"
  - Productos con "zapato" o "calzado" en el nombre
  - Productos con "bota" o "botin" (sinónimos)
  - Productos con "steel toe" o "punta de acero"

---

## 📊 Resultados Esperados

### Búsqueda
✅ "Zapatos de Seguridad" ahora encuentra productos
✅ Sinónimos funcionan (calzado, botas, etc.)
✅ Términos en inglés también funcionan

### Nombres de Productos
✅ Todos los nombres limpios sin variantes
✅ Consistencia en buscador, catálogo, carruseles
✅ Variantes visibles solo al clickear el producto

### Categorización
✅ Productos automáticamente asignados a categorías correctas
✅ Menos productos sin categoría
✅ Mejor organización del catálogo

---

## 🛠️ Mantenimiento

### Agregar Nuevas Categorías
Edita `generar_tags_categorias.py` y agrega al diccionario `CATEGORY_TAGS`:
```python
CATEGORY_TAGS = {
    "Nueva Categoría": [
        "tag1", "tag2", "tag3", ...
    ],
    ...
}
```

### Actualizar Tags Existentes
1. Ejecuta `python generar_tags_ia.py` para analizar productos actualizados
2. Usa IA para generar nuevos tags
3. Aplica con `python aplicar_busqueda_tags.py --apply`

---

## ⚠️ Importante

- Los cambios en frontend son **automáticos** - no requiere acción
- Los scripts de Python son **opcionales** pero recomendados para mejorar la búsqueda
- Siempre ejecuta en modo prueba primero (`sin --apply`)
- Revisa `sugerencias_recategorizacion.json` antes de aplicar cambios

---

## 📞 Soporte

Si necesitas agregar más categorías o tags, o ajustar la lógica de limpieza de nombres:
1. Edita `generar_tags_categorias.py` para más tags
2. Edita `src/lib/woocommerce.ts` función `getCleanProductName()` para ajustar limpieza
3. Re-ejecuta los scripts según sea necesario
