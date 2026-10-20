-- 1. Activación de la extensión espacial PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- 2. Eliminación preventiva de la tabla si ya existía
DROP TABLE IF EXISTS bares CASCADE;

-- 3. Definición de la tabla 'bares'
CREATE TABLE bares (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    direccion VARCHAR(180) NOT NULL,
    lat NUMERIC(9, 6) NOT NULL,
    lon NUMERIC(9, 6) NOT NULL,
    precio_cana NUMERIC(4, 2) NOT NULL,
    formato VARCHAR(60) NOT NULL,
    fuente VARCHAR(150),
    -- Columna geométrica espacial: Punto 2D en sistema de coordenadas WGS 84 (SRID 4326)
    geom GEOMETRY(Point, 4326) NOT NULL, -- GEOMETRY es el tipo de dato geometrico de POSTGIS, 4326 es el codigo de referencia de coordenadas (WGS84)

    -- Restricciones de integridad (Check constraints)
    CONSTRAINT chk_precio_positivo CHECK (precio_cana > 0),
    CONSTRAINT chk_lat_valida CHECK (lat BETWEEN -90.0 AND 90.0), -- las coordenadas de latitud deben estar entre -90 y 90
    CONSTRAINT chk_lon_valida CHECK (lon BETWEEN -180.0 AND 180.0) -- las coordenadas de longitud deben estar entre -180 y 180
);

-- 4. Creación de Índices para Optimización de Consultas

-- Índice GiST sobre geometría (R-Tree multinivel para búsquedas espaciales en 2D)
CREATE INDEX idx_bares_geom_gist 
    ON bares 
    USING GIST (geom);

-- Índice GiST funcional sobre tipo GEOGRAPHY (calcula distancias geodésicas en metros sobre el elipsoide)
CREATE INDEX idx_bares_geog_gist 
    ON bares 
    USING GIST ((geom::geography)); -- Basicamente es para calcular en metros la distancia entre dos puntos, no en grados

-- Índice B-Tree estándar sobre el precio (para filtros y ordenaciones rápidas por coste)
CREATE INDEX idx_bares_precio_btree 
    ON bares (precio_cana);

-- 5. Documentación de metadatos en el catálogo de PostgreSQL
COMMENT ON TABLE bares IS 'Catálogo geoespacial de establecimientos hosteleros con precios de cerveza en Sevilla';
COMMENT ON COLUMN bares.geom IS 'Punto GPS con coordenadas WGS84 (SRID 4326), formato Point(lon, lat)';
COMMENT ON COLUMN bares.precio_cana IS 'Precio unitario de la caña o formato más popular en euros (€)';
COMMENT ON INDEX idx_bares_geom_gist IS 'Índice GiST para acelerar consultas espaciales (bounding box y operadores PostGIS)';
COMMENT ON INDEX idx_bares_geog_gist IS 'Índice GiST funcional para operaciones de proximidad (ST_DWithin) en metros';
