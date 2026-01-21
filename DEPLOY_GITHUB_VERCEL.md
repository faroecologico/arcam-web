# 🚀 Instrucciones para Deploy a GitHub y Vercel

## ✅ Estado Actual

- ✅ Código compilado exitosamente (build sin errores)
- ✅ Commit inicial creado con todos los cambios
- ✅ Repositorio Git inicializado localmente
- ⏳ Pendiente: Conectar con GitHub y desplegar a Vercel

---

## 📋 Pasos para Subir a GitHub

### 1. Crear Repositorio en GitHub

1. Ve a [github.com](https://github.com)
2. Click en "New repository" (botón verde)
3. Nombre sugerido: `arcam-web`
4. Descripción: "E-commerce de productos industriales y ropa de trabajo - ARCAM"
5. **NO** inicialices con README, .gitignore o licencia (ya los tenemos)
6. Click en "Create repository"

### 2. Conectar Repositorio Local con GitHub

Copia y pega estos comandos en tu terminal:

```bash
cd "c:\Users\usuario_tr7\Desktop\Archivos de reportes Enero 2025\arcam-web"

# Reemplaza TU_USUARIO con tu usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/arcam-web.git

# Renombrar rama a main si es master
git branch -M main

# Primer push
git push -u origin main
```

**Ejemplo:**
Si tu usuario es "johndoe":
```bash
git remote add origin https://github.com/johndoe/arcam-web.git
git branch -M main
git push -u origin main
```

---

## 🌐 Desplegar a Vercel

### Opción A: Desde el Dashboard de Vercel (Recomendado)

1. Ve a [vercel.com](https://vercel.com)
2. Click en "Add New Project"
3. Importa tu repositorio de GitHub: `arcam-web`
4. Configuración del proyecto:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`

5. Variables de entorno (Environment Variables):
   ```
   NEXT_PUBLIC_WOO_URL = https://arcam.cl
   WC_CONSUMER_KEY = ck_8d962ed36abef8b8c11c34e22170e23361265281
   WC_CONSUMER_SECRET = cs_5bc4372f8e356cf5d725ccdc9f8e1a7d9fa7f1ef
   ```

6. Click en "Deploy"

### Opción B: Desde la Terminal con Vercel CLI

```bash
# Instalar Vercel CLI (solo primera vez)
npm install -g vercel

# Navegar al directorio del frontend
cd frontend

# Iniciar deploy
vercel

# Seguir las instrucciones:
# - Set up and deploy? Yes
# - Which scope? Tu cuenta
# - Link to existing project? No
# - Project name? arcam-web
# - In which directory is your code located? ./
# - Want to override settings? Yes
#   - Build Command: npm run build
#   - Output Directory: .next
#   - Development Command: npm run dev

# Deploy a producción
vercel --prod
```

---

## 🔒 Variables de Entorno en Vercel

Asegúrate de agregar estas variables en: **Project Settings → Environment Variables**

```
NEXT_PUBLIC_WOO_URL = https://arcam.cl
WC_CONSUMER_KEY = ck_8d962ed36abef8b8c11c34e22170e23361265281
WC_CONSUMER_SECRET = cs_5bc4372f8e356cf5d725ccdc9f8e1a7d9fa7f1ef
```

**Importante:** Estas variables ya están en tu `.env.local` pero Vercel necesita su propia configuración.

---

## 🎯 Verificar el Deploy

Una vez completado:

1. Vercel te dará una URL (ej: `arcam-web.vercel.app`)
2. Prueba las funcionalidades:
   - ✅ Búsqueda de productos
   - ✅ Nombres limpios sin variantes
   - ✅ Catálogo con productos deduplicados
   - ✅ Carruseles funcionando
   - ✅ Detalle de productos con variantes

---

## 📱 Comandos Rápidos para Futuros Cambios

```bash
# Hacer cambios en el código...

# 1. Agregar archivos modificados
git add .

# 2. Commit con mensaje descriptivo
git commit -m "descripción de los cambios"

# 3. Push a GitHub
git push

# Vercel auto-despliega los cambios automáticamente! 🚀
```

---

## ⚠️ Notas Importantes

### Archivo .gitignore
Ya está configurado para excluir:
- `.env` y `.env.local` (seguridad)
- `node_modules/` (pesado)
- `.next/` (generado automáticamente)
- Archivos temporales y de sistema

### Seguridad
- ❌ **NUNCA** subas el archivo `.env` a GitHub
- ✅ Usa variables de entorno de Vercel para credenciales
- ✅ El `.gitignore` ya protege estos archivos

### Estructura del Proyecto
```
arcam-web/
├── frontend/           → Aplicación Next.js
│   ├── src/
│   ├── public/
│   └── package.json
├── *.py               → Scripts Python (backend tools)
├── category_tags_map.json → Tags generados
└── README.md          → Este archivo
```

---

## 🆘 Solución de Problemas

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/arcam-web.git
```

### Error en Vercel: "Build failed"
1. Verifica que Root Directory sea `frontend`
2. Verifica que las variables de entorno estén configuradas
3. Revisa los logs de build en el dashboard de Vercel

### Error: "Authentication failed"
```bash
# Usar token de GitHub en lugar de contraseña
# Ve a: GitHub → Settings → Developer settings → Personal access tokens
# Genera un token y úsalo como contraseña
```

---

## ✅ Checklist Final

- [ ] Repositorio creado en GitHub
- [ ] Remote origin configurado
- [ ] Código subido con `git push`
- [ ] Proyecto importado en Vercel
- [ ] Root directory configurado como `frontend`
- [ ] Variables de entorno agregadas en Vercel
- [ ] Deploy exitoso
- [ ] Sitio funcionando en la URL de Vercel
- [ ] Pruebas de búsqueda y catálogo realizadas

---

## 🎉 ¡Listo!

Una vez completados estos pasos, tu sitio estará live en Vercel y cualquier push a GitHub se desplegará automáticamente.

**URL de producción:** `https://arcam-web.vercel.app` (o la que Vercel te asigne)
