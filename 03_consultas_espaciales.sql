-- Coordenadas de referencia del usuario (ejemplo: Carretera de Carmona, 30):
-- Latitud: 37.40193 | Longitud: -5.97479 (mi barrio)

-- -----------------------------------------------------------------------------
-- CONSULTA 1: El Bar con la Cerveza más Barata a menos de 500 metros
-- Objetivo: Resolver la necesidad inmediata del usuario (encontrar el mejor precio a distancia a pie).
-- Técnica: ST_DWithin sobre índice GiST geodésico y ordenación por precio ascendente.
-- -----------------------------------------------------------------------------
SELECT id, nombre, direccion, precio_cana AS "Precio (€)", formato AS "Formato",
    ROUND(
        ST_Distance(
            geom::geography, 
            ST_SetSRID(ST_MakePoint(-5.97479, 37.40193), 4326)::geography -- Hacemos la coordenada del usuario geography para que se pueda calcular la distancia en metros
        )::numeric, 
        1 -- 1 decimal
    ) AS "Distancia (m)"
FROM bares
-- ST_DWithin nos permite buscar elementos dentro de un radio de distancia
WHERE ST_DWithin(
    geom::geography, 
    -- ST_MakePoint crea el punto de mi casa y ST_SetSRID le asigna el SRID 4326 y lo convierte a geography  
    ST_SetSRID(ST_MakePoint(-5.97479, 37.40193), 4326)::geography, -- longitud,latitud de mi "casa" 
    500 -- 500 metros a la redonda
) -- Si no hubieramos puesto esta condición, nos hubiera devuelto todos los bares de la base de datos
ORDER BY precio_cana ASC, "Distancia (m)" ASC
LIMIT 1;


-- -----------------------------------------------------------------------------
-- CONSULTA 2: Ranking Top 5 Bares Más Cercanos (Independientemente del precio)
-- Objetivo: Cuando el usuario prioriza la inmediatez sobre el precio exacto.
-- Técnica: Operador de distancia espacial ordenado de forma ascendente.
-- -----------------------------------------------------------------------------
SELECT 
    id,
    nombre,
    direccion,
    precio_cana AS "Precio (€)",
    formato AS "Formato",
    ROUND(
        ST_Distance(
            geom::geography, 
            ST_SetSRID(ST_MakePoint(-5.97479, 37.40193), 4326)::geography
        )::numeric, 
        1
    ) AS "Distancia (m)"
FROM bares
ORDER BY "Distancia (m)" ASC
LIMIT 5;


-- -----------------------------------------------------------------------------
-- CONSULTA 3: Comparativa en Radio Ampliado (1.000 m) - Filtro "Cerveza Barata" (<= 1.50 €)
-- Objetivo: Búsqueda de bares económicos en un radio de 10-12 minutos caminando.
-- -----------------------------------------------------------------------------
SELECT 
    id,
    nombre,
    direccion,
    precio_cana AS "Precio (€)",
    formato AS "Tipo Cerveza",
    ROUND(
        ST_Distance(
            geom::geography, 
            ST_SetSRID(ST_MakePoint(-5.97479, 37.40193), 4326)::geography
        )::numeric, 
        1
    ) AS "Distancia (m)"
FROM bares
WHERE ST_DWithin(
    geom::geography, 
    ST_SetSRID(ST_MakePoint(-5.97479, 37.40193), 4326)::geography, 
    1000
)
AND precio_cana <= 1.50
ORDER BY precio_cana ASC, "Distancia (m)" ASC;


-- -----------------------------------------------------------------------------
-- CONSULTA 4: Estadísticas de Mercado en el Entorno (Agregación Espacial)
-- Objetivo: Conocer el precio medio, mínimo y máximo en el radio de 800 metros.
-- Técnica: Funciones agregadas de SQL combinadas con filtro geodésico PostGIS.
-- -----------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_bares_en_radio,
    MIN(precio_cana) AS precio_minimo_eur,
    ROUND(AVG(precio_cana), 2) AS precio_medio_eur,
    MAX(precio_cana) AS precio_maximo_eur
FROM bares
WHERE ST_DWithin(
    geom::geography, 
    ST_SetSRID(ST_MakePoint(-5.97479, 37.40193), 4326)::geography, 
    800
);


-- -----------------------------------------------------------------------------
-- CONSULTA 5: Exportación en Formato GeoJSON para Visualización Cartográfica
-- Objetivo: Demostrar la interoperabilidad de PostGIS con herramientas web (Leaflet, Mapbox, QGIS).
-- Técnica: ST_AsGeoJSON transforma la geometría directamente a estándar GeoJSON.
-- -----------------------------------------------------------------------------
SELECT 
    json_build_object(
        'type', 'FeatureCollection',
        'features', json_agg(
            json_build_object(
                'type', 'Feature',
                'geometry', ST_AsGeoJSON(geom)::json,
                'properties', json_build_object(
                    'id', id,
                    'nombre', nombre,
                    'direccion', direccion,
                    'precio_cana', precio_cana,
                    'formato', formato
                )
            )
        )
    ) AS geojson_dataset
FROM bares;


-- -----------------------------------------------------------------------------
-- CONSULTA 6: Justificación Técnica con EXPLAIN ANALYZE (Prueba para la Memoria)
-- Objetivo: Demostrar que el motor utiliza el índice GiST (idx_bares_geog_gist)
-- en lugar de realizar un escaneo secuencial completo (Seq Scan / Full Table Scan).
-- -----------------------------------------------------------------------------
EXPLAIN ANALYZE
SELECT 
    id, 
    nombre, 
    precio_cana, 
    ROUND(ST_Distance(geom::geography, ST_SetSRID(ST_MakePoint(-5.97479, 37.40193), 4326)::geography)::numeric, 1) AS dist_metros
FROM bares
WHERE ST_DWithin(
    geom::geography, 
    ST_SetSRID(ST_MakePoint(-5.97479, 37.40193), 4326)::geography, 
    500
)
ORDER BY precio_cana ASC;
