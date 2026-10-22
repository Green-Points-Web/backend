* * *

# 🍃 GreenPoints · Backend

> Proyecto colaborativo para el desarrollo web de GreenPoints, una aplicación pensada para registrar acciones sostenibles que te permite cuantificar tu impacto ambiental positivo (mediante puntos obtenidos a través del cálculo de CO₂ ahorrado).

---

## ✨ Aspectos Clave

*   **📊 Dashboard de impacto:** resumen en tiempo de KPIs —puntos totales, CO₂ ahorrado y acciones registradas— con lista de las acciones más recientes.
*   **🗂️ Catálogo de acciones:** grid de acciones sostenibles con búsqueda y filtrado por categoría, cada tarjeta codificada por color (Movilidad, Naturaleza, Reciclaje, Participación).
*   **✅ Registro de acciones:** alta rápida desde el catálogo o mediante un modal dedicado; cada acción guarda fecha, categoría y puntos/CO₂ asociados.
*   **📜 Historial paginado:** tabla de acciones registradas con paginación (15 por página), iconografía por categoría y acciones de editar/eliminar.
*   **🌱 Cálculo de impacto:** los puntos se derivan del CO₂ ahorrado según el tipo de acción.
*   **⚡ SPA sin recargar:** Hash Router propio que inyecta vistas parciales y mantiene la experiencia fluida.
*   **🔔 Secciones sincronizadas:** un mismo registro se refleja en dashboard e historial en vivo mediante eventos (`action:created` / `action:deleted`), sin refrescar la página.
*   **🎨 UI ligera y sin dependencias:** Vanilla JS + CSS tradicional e iconografía Material Symbols; sin framework ni bundler.
*   **🔌 API REST:** consumo del backend con `fetch` nativo, con estados de carga/error y estados vacíos en cada vista.

---

# 🚀 Instalación y Guía de Configuración

Bienvenido al repositorio del proyecto. Esta guía ofrece instrucciones paso a paso para configurar el entorno de desarrollo, instalar las dependencias necesarias, ejecutar el servidor backend con FastAPI y Uvicorn, y lanzar la interfaz del frontend.

---

## 📋 Requisitos previos

Asegúrate de tener instalado lo siguiente en tu equipo antes de comenzar:
- **Python** (se recomienda versión 3.9 o superior)
- **Git** para el control de versiones
- Un navegador web moderno

---

## ⚙️ 1. Configuración del backend (FastAPI / Uvicorn)

El backend gestiona el cálculo de puntos, la progresión de nivel del usuario y las rutas de la API.

### 1.1. Sincronizar los cambios del repositorio
Cambia a la rama de desarrollo y descarga las últimas actualizaciones:
```bash
git checkout dev
git pull origin dev
```

### 1.2. Crear y activar un entorno virtual
Se recomienda aislar las dependencias del proyecto:
```bash
# En macOS / Linux
python3 -m venv venv
source venv/bin/activate

# En Windows (CMD / PowerShell)
python -m venv venv
venv\Scripts\activate
```

### 1.3. Instalar las dependencias
El archivo `requirements.txt` contiene los paquetes necesarios (fastapi, uvicorn, pydantic, pytest, etc.). Instálalos con:
```bash
pip install -r requirements.txt

# Nota: si necesitas instalar las dependencias principales directamente, ejecuta:

pip install fastapi uvicorn pydantic pytest httpx
```

### 1.4. Ejecutar el servidor Uvicorn
Inicia el servidor FastAPI en modo desarrollo con recarga automática:
```bash
uvicorn app.main:app --reload --reload-dir app --host 127.0.0.1 --port 8000
```
* Endpoint de la API: http://127.0.0.1:8000
* Documentación interactiva de la API (Swagger UI): http://127.0.0.1:8000/docs

---

# 💻 2. Ejecutar el frontend

El frontend renderiza dinámicamente las estadísticas de puntos del usuario, el progreso de nivel y las tablas de historial.

## 2.1. Lanzar la interfaz
Puedes servir los archivos estáticos del frontend con el servidor HTTP incorporado de Python:
```bash
# Ejecutar desde la raíz o desde el directorio frontend
python3 -m http.server 5500
```
Después, abre http://127.0.0.1:5500 en tu navegador, o abre directamente el archivo `index.html` principal.

---

# 🧪 3. Ejecutar los tests unitarios (Pytest)

Para verificar los rangos de puntos, los umbrales de nivel (Seed, Sprout, Tree, Forest, Planet Hero) y los endpoints de la API:

```bash
pytest tests/ -v
```

<Elicitations message="What would you like to do next?">
  <Elicitation label="Create requirements.txt file" query="Genera el contenido exacto para el archivo requirements.txt del backend con sus versiones recomendadas."/>
  <Elicitation label="Explain how to connect JS frontend to FastAPI" query="Explícame cómo conectar el script de renderizado de historial en JavaScript con los endpoints de puntos de FastAPI."/>
</Elicitations>

---

## 🔌 Endpoints de la API (Gestión de acciones)

A continuación se describen las rutas desarrolladas para consultar el catálogo y registrar nuevas acciones sostenibles.

### 1. Obtener el catálogo de acciones
- **Ruta:** `GET /catalog`
- **Descripción:** Devuelve una lista de todas las acciones sostenibles disponibles para los usuarios, incluyendo su categoría, los puntos otorgados y el impacto en CO₂.
- **Respuesta correcta (200 OK):**
  ```json
  [
    {
      "id": 1,
      "name": "Reciclar plástico",
      "category": "Reciclaje",
      "points": 10,
      "co2_kg": 0.5,
      "active": true
    }
  ]
  ```

---

## Uso de herramientas de IA y metodología

### Propósito

Las herramientas de Inteligencia Artificial se utilizaron como apoyo durante el desarrollo de GreenPoints para ayudar a comprender conceptos técnicos, resolver problemas de programación y mejorar la documentación del proyecto.

### Cómo se utilizaron las herramientas de IA

- **Orientación técnica:** las herramientas de IA ayudaron a aclarar conceptos relacionados con Python, FastAPI, Git y pruebas de software.
- **Resolución de problemas:** se utilizaron herramientas de IA para investigar errores y explorar posibles soluciones durante el desarrollo.
- **Documentación:** la asistencia de IA ayudó a organizar la información técnica y a mejorar la claridad de la documentación escrita.
- **Apoyo en la revisión de código:** las sugerencias generadas por IA se usaron como referencia al revisar el código y considerar posibles mejoras.

### Validación y responsabilidad

Las respuestas generadas por IA fueron revisadas y adaptadas a los requisitos del proyecto. Las soluciones sugeridas deben probarse antes de integrarse en el código.

El equipo de desarrollo sigue siendo responsable de la implementación final, las decisiones técnicas y la verificación del funcionamiento del proyecto.

### Uso responsable

- Las herramientas de IA se utilizan como apoyo para el aprendizaje y el desarrollo, no como sustituto de la comprensión del código.
- Las sugerencias generadas se revisan antes de aplicarse.
- Los requisitos del proyecto y las convenciones de código tienen prioridad sobre las recomendaciones generadas por IA.
- La información sensible, como contraseñas, claves de API y credenciales, no debe compartirse con herramientas de IA.







