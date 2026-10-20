# 🍻 Buscador Geoespacial de Precios de Cerveza en Sevilla (PostGIS + Docker)

Proyecto práctico de bases de datos espaciales desarrollado para la asignatura **Ampliación de Bases de Datos** (Grado en Ingeniería del Software, Universidad Loyola Andalucía).

El objetivo es resolver una necesidad real de búsqueda geoespacial: **encontrar el bar con la cerveza más barata dentro de un radio de búsqueda personalizable (en metros)** respecto a la posición del usuario en Sevilla (área de Carretera de Carmona, Macarena, Capuchinos y Arroyo), demostrando el uso de **PostgreSQL con la extensión espacial PostGIS**, optimización mediante **índices GiST** y visualización interactiva con **Leaflet**.

---

## 🚀 Tecnologías Utilizadas

* **Base de Datos Espacial:** PostgreSQL 16 con extensión **PostGIS 3.4**.
* **Contenerización:** Docker y Docker Compose para un despliegue aislado y reproducible.
* **Sistema de Coordenadas:** WGS 84 (SRID 4326) con proyecciones geodésicas (`geography`) para distancias métricas.
* **Optimización e Índices:** Índices GiST (espacial 2D y funcional geodésico) e índice B-Tree en precio.
* **Visualización Web:** HTML5, CSS3, JavaScript y Leaflet.js (con capas de callejero y satélite).
* **Scripting de Datos:** Python 3 para estructuración y generación del visor interactivo.

---

## 📁 Estructura del Repositorio

| Archivo / Carpeta | Descripción |
| :--- | :--- |
| [`docker-compose.yml`](docker-compose.yml) | Definición y configuración del contenedor Docker de PostgreSQL + PostGIS con volumen persistente. |
| [`01_init_postgis_ddl.sql`](01_init_postgis_ddl.sql) | Script DDL: activación de PostGIS, tabla `bares`, restricciones de integridad (CHECK) e índices GiST. |
| [`02_insert_30_bares.sql`](02_insert_30_bares.sql) | Script DML: población de 30 bares reales con coordenadas GPS (`ST_SetSRID`) y precios de carta reales. |
| [`03_consultas_espaciales.sql`](03_consultas_espaciales.sql) | Consultas de negocio: búsqueda por proximidad (`ST_DWithin`), ordenación por precio, distancias (`ST_Distance`) y métricas de mercado. |
| [`mapa_cervezas.html`](mapa_cervezas.html) | Visor geoespacial interactivo donde el usuario ajusta sus coordenadas y radio en vivo. |
| [`generar_mapa.py`](generar_mapa.py) | Script en Python para procesar el catálogo JSON de bares y generar el visor HTML. |
| [`scratch_30_bares.json`](scratch_30_bares.json) | Dataset en formato JSON con la información, fuentes y coordenadas de los bares. |
| `imgs/` | Capturas de pantalla del despliegue y pruebas del proyecto. |

---

## 🛠️ Puesta en Marcha Rápida

### 1. Requisitos previos
* [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/) instalados.
* Git.

### 2. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
```

### 3. Levantar la base de datos con Docker
```bash
docker compose up -d
```
*El contenedor levantará PostgreSQL + PostGIS escuchando en el puerto local `5432` con la base de datos `cervezas_sevilla`.*

### 4. Inicializar la tabla y cargar los datos
Ejecuta los scripts SQL directamente dentro del contenedor:

```bash
# 1. Crear tabla e índices GiST
docker exec -i postgis_cervezas_sevilla psql -U postgres -d cervezas_sevilla < 01_init_postgis_ddl.sql

# 2. Insertar los 30 bares de Sevilla
docker exec -i postgis_cervezas_sevilla psql -U postgres -d cervezas_sevilla < 02_insert_30_bares.sql
```

### 5. Probar el Visor Interactivo
Simplemente abre el archivo [`mapa_cervezas.html`](mapa_cervezas.html) en tu navegador web favorito (haciendo doble clic o abriéndolo desde Chrome/Firefox):
* Ajusta el **radio de búsqueda** (100 m – 1.500 m) con el control deslizante.
* Haz clic en cualquier calle del mapa para mover tu ubicación.
* Comprueba cómo se calcula en tiempo real el bar más barato y el listado ordenado.

---

## 🧠 Consultas Espaciales Clave (PostGIS)

### 1. El Bar con la Cerveza más Barata a menos de $X$ metros
```sql
SELECT 
    nombre,
    direccion,
    precio_cana AS "Precio (€)",
    ROUND(
        ST_Distance(
            geom::geography, 
            ST_SetSRID(ST_MakePoint(-5.97479, 37.40193), 4326)::geography
        )::numeric, 1
    ) AS "Distancia (m)"
FROM bares
WHERE ST_DWithin(
    geom::geography, 
    ST_SetSRID(ST_MakePoint(-5.97479, 37.40193), 4326)::geography, 
    500
)
ORDER BY precio_cana ASC, "Distancia (m)" ASC
LIMIT 1;
```

### 2. Optimización y Rendimiento (Índices GiST)
Para evitar un escaneo secuencial (`Seq Scan`) en tablas con grandes volúmenes de datos espaciales, se utiliza un índice GiST sobre la conversión a `geography`:

```sql
CREATE INDEX idx_bares_geog_gist ON bares USING GIST ((geom::geography));
```

El análisis de la consulta (`EXPLAIN ANALYZE`) confirma el uso del índice:
* **Plan:** `Index Scan using idx_bares_geog_gist on bares`
* **Tiempo de ejecución:** `< 0.05 ms`

---

## 👤 Autor
* **Fernando** - Grado en Ingeniería del Software, Universidad Loyola Andalucía.
