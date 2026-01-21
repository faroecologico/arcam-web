# 🏪 ARCAM E-Commerce

E-commerce moderno para productos industriales, EPP (Elementos de Protección Personal) y ropa de trabajo.

## 🚀 Últimas Actualizaciones

### ✅ Implementación de Limpieza de Nombres y Sistema de Tags (2026-01-21)

- **Limpieza automática de nombres de productos**: Los productos ahora se muestran sin variantes en catálogos y búsquedas
  - Antes: *"POLAR P.JACK VPO400 DELTA VARON AZUL TALLA L"*
  - Ahora: *"POLAR P.JACK VPO400 DELTA"*
  
- **Sistema de tags para categorías**: Mejora la búsqueda por sinónimos y términos relacionados
  - "Zapatos de Seguridad" ahora encuentra productos correctamente
  - 74 tags por categoría principal (zapato, calzado, bota, safety, etc.)
  
- **Deduplicación inteligente**: Agrupa variantes como un solo producto en listados
- **Build sin errores**: Compilación exitosa en Next.js 16.1.4

## 📁 Estructura del Proyecto

```
arcam-web/
├── frontend/                          # Aplicación Next.js
│   ├── src/
│   │   ├── app/                       # App Router (Next.js 13+)
│   │   ├── components/                # Componentes React
│   │   │   ├── layout/               # Header, Footer, etc.
│   │   │   ├── product/              # ProductCard, ProductDetail
│   │   │   └── ui/                   # Componentes UI reutilizables
│   │   ├── lib/
│   │   │   └── woocommerce.ts        # API WooCommerce + getCleanProductName()
│   │   └── store/                    # Zustand state management
│   ├── public/                        # Assets estáticos
│   └── package.json
│
├── *.py                               # Scripts Python (herramientas backend)
│   ├── generar_tags_categorias.py    # Generar tags predefinidos
│   ├── generar_tags_ia.py            # Preparar datos para IA
│   ├── aplicar_busqueda_tags.py      # Aplicar recategorización
│   ├── auto_categorias.py            # Categorización automática
│   └── ...otros scripts de gestión
│
├── category_tags_map.json             # Mapa de tags generado
├── SOLUCION_BUSQUEDA_Y_NOMBRES.md    # Documentación de la solución
└── DEPLOY_GITHUB_VERCEL.md           # Guía de deploy
```

## 🛠️ Tecnologías

### Frontend
- **Next.js 16.1.4** (App Router + Turbopack)
- **React 19**
- **TypeScript**
- **Tailwind CSS**
- **Zustand** (State Management)
- **Framer Motion** (Animaciones)
- **Lucide React** (Iconos)

### Backend/CMS
- **WooCommerce** (WordPress) - API REST
- **Python Scripts** - Automatización y gestión de productos

### Integraciones
- **Supabase** - Base de datos y autenticación
- **Bsale** - Sincronización de stock

## 🚀 Inicio Rápido

### Requisitos Previos
- Node.js 18+ 
- Python 3.9+
- Cuenta en WooCommerce/WordPress

### Instalación

1. **Clonar repositorio**
```bash
git clone https://github.com/TU_USUARIO/arcam-web.git
cd arcam-web
```

2. **Configurar Frontend**
```bash
cd frontend
npm install
```

3. **Variables de Entorno**

Crear `frontend/.env.local`:
```env
NEXT_PUBLIC_WOO_URL=https://arcam.cl
WC_CONSUMER_KEY=tu_consumer_key
WC_CONSUMER_SECRET=tu_consumer_secret
```

Crear `.env` en la raíz:
```env
WOO_URL=https://arcam.cl
WOO_KEY=tu_consumer_key
WOO_SECRET=tu_consumer_secret
```

4. **Ejecutar en Desarrollo**
```bash
cd frontend
npm run dev
```

Abre [http://localhost:3000](http://localhost:3000)

## 📦 Scripts Python

### Instalar Dependencias
```bash
pip install -r requests.txt
# o
pip install requests python-dotenv woocommerce
```

### Scripts Disponibles

#### Gestión de Tags y Búsqueda
```bash
# Generar tags para categorías
python generar_tags_categorias.py

# Analizar productos y generar datos para IA
python generar_tags_ia.py

# Aplicar recategorización (modo prueba)
python aplicar_busqueda_tags.py

# Aplicar recategorización (aplicar cambios)
python aplicar_busqueda_tags.py --apply
```

#### Gestión de Productos
```bash
# Categorización automática
python auto_categorias.py

# Asignar imágenes automáticamente
python asignar_imagenes_auto.py

# Conectar variantes de productos
python conectar_desde_json.py
```

Ver `SOLUCION_BUSQUEDA_Y_NOMBRES.md` para documentación completa.

## 🎨 Características Principales

### 🛒 E-Commerce Dual Mode
- **Modo Persona (B2C)**: Precios visibles, compra directa
- **Modo Empresa (B2B)**: Cotizaciones, precios por volumen

### 🔍 Búsqueda Inteligente
- Búsqueda en tiempo real con sugerencias
- Sistema de tags y sinónimos
- Nombres limpios sin variantes
- Deduplicación automática

### 📱 UI/UX Moderno
- Diseño responsive
- Animaciones fluidas (Framer Motion)
- Dark mode / Light mode
- Carruseles de productos
- Mega menú con categorías

### 🏷️ Sistema de Productos
- Gestión de variantes (tallas, colores)
- Imágenes automáticas
- Categorización inteligente
- Stock en tiempo real

## 📊 Funcionalidades de Búsqueda

### Problema Resuelto: "Zapatos de Seguridad"

**Antes:**
- Búsqueda: "Zapatos de Seguridad" → Sin resultados
- Productos: "POLAR VARON AZUL TALLA L" (nombre completo)

**Ahora:**
- Búsqueda: "Zapatos de Seguridad" → 74 tags activos (zapato, calzado, bota, safety...)
- Productos: "POLAR P.JACK VPO400 DELTA" (nombre limpio)
- Variantes visibles solo al clickear

### Función `getCleanProductName()`

Ubicación: `frontend/src/lib/woocommerce.ts`

Remueve automáticamente:
- ✅ Prefijos (FERR., FERRE.)
- ✅ Tallas (TALLA L, TX, T42)
- ✅ Colores (NEGRO, AZUL, ROJO, VERDE, AMARILLO, etc.)
- ✅ Géneros (VARON, DAMA, HOMBRE, MUJER, UNISEX)
- ✅ Dimensiones (42mm, 10kg, etc.)
- ✅ Números (N° 42, # 10)

## 🌐 Deploy

### Vercel (Recomendado)

Ver guía completa en: [DEPLOY_GITHUB_VERCEL.md](./DEPLOY_GITHUB_VERCEL.md)

**Resumen:**
1. Push a GitHub
2. Importar proyecto en Vercel
3. Configurar Root Directory: `frontend`
4. Agregar variables de entorno
5. Deploy automático ✨

### Variables de Entorno en Vercel
```
NEXT_PUBLIC_WOO_URL = https://arcam.cl
WC_CONSUMER_KEY = tu_key
WC_CONSUMER_SECRET = tu_secret
```

## 📝 Comandos Útiles

### Frontend
```bash
cd frontend

# Desarrollo
npm run dev

# Build
npm run build

# Lint
npm run lint

# Iniciar producción
npm start
```

### Git
```bash
# Commit y push
git add .
git commit -m "descripción"
git push

# Ver cambios
git status
git log --oneline
```

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es privado y confidencial de ARCAM.

## 📞 Soporte

Para problemas o preguntas:
- Revisa la documentación en `/docs`
- Consulta `SOLUCION_BUSQUEDA_Y_NOMBRES.md` para temas de búsqueda
- Consulta `DEPLOY_GITHUB_VERCEL.md` para deploy

## 🎯 Roadmap

- [x] Sistema de limpieza de nombres de productos
- [x] Sistema de tags para categorías
- [x] Deduplicación de variantes
- [x] Build sin errores
- [ ] Integración completa con Bsale
- [ ] Panel de administración mejorado
- [ ] Optimización de imágenes
- [ ] SEO avanzado
- [ ] Analytics integrado

---

**Última actualización:** 21 de Enero, 2026  
**Versión:** 1.0.0  
**Estado:** ✅ En Producción
