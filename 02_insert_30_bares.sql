-- =============================================================================
-- Universidad Loyola Andalucía - Ampliación de Bases de Datos
-- Trabajo Práctico Individual (TPI 1) - Bases de Datos Especializadas
-- Script: 02_insert_30_bares.sql (Fase 3 - Población de Datos Reales)
-- 30 Establecimientos en Carretera de Carmona y adyacentes (Sevilla)
-- =============================================================================

BEGIN;

-- Limpieza previa por si se re-ejecuta el script
TRUNCATE TABLE bares RESTART IDENTITY;

INSERT INTO bares (id, nombre, direccion, lat, lon, precio_cana, formato, fuente, geom) VALUES
(1, 'Cervecería La Notaría', 'Carretera de Carmona, 30', 37.4015, -5.976, 1.5, 'Caña Cruzcampo', 'Carta local y reseñas recientes (2024)', ST_SetSRID(ST_MakePoint(-5.976, 37.4015), 4326)),
(2, 'La Barra del 3', 'Calle Francisco de Ariño, 3', 37.401, -5.9735, 2.0, 'Caña / Copa especial', 'Carta Gastrobar Solete Repsol (2024-2025)', ST_SetSRID(ST_MakePoint(-5.9735, 37.401), 4326)),
(3, 'Cervecería La Rosaleda', 'Calle Francisco de Ariño, 12', 37.39877, -5.97668, 1.5, 'Caña Cruzcampo', 'Carta física y reseñas de clientes (2024)', ST_SetSRID(ST_MakePoint(-5.97668, 37.39877), 4326)),
(4, 'Taberna La Crisis', 'Calle Tharsis, 14', 37.3996, -5.972, 1.3, 'Botellín / Caña popular', 'Pizarra pública local y reseñas (2024)', ST_SetSRID(ST_MakePoint(-5.972, 37.3996), 4326)),
(5, 'Cervecería Mariluz', 'Calle Jabugo, 1', 37.39877, -5.97582, 1.4, 'Caña Cruzcampo', 'Carta tradicional en barra (2024)', ST_SetSRID(ST_MakePoint(-5.97582, 37.39877), 4326)),
(6, 'Cervecería Mediterráneo', 'Calle Andrés Segovia, 1', 37.4035, -5.971, 1.5, 'Caña tanque salmuera', 'Carta especializada cervecera (2024)', ST_SetSRID(ST_MakePoint(-5.971, 37.4035), 4326)),
(7, 'Cervecería La Duna', 'Calle Tharsis, 1', 37.39934, -5.97141, 1.6, 'Caña Cruzcampo', 'Carta de marisquería/terraza (2024)', ST_SetSRID(ST_MakePoint(-5.97141, 37.39934), 4326)),
(8, 'Cervecería Adrián', 'Avenida de Llanes, 4', 37.4055, -5.9725, 1.7, 'Caña Cruzcampo', 'Carta digital y marisquería (2024)', ST_SetSRID(ST_MakePoint(-5.9725, 37.4055), 4326)),
(9, 'Bar Casa Paco', 'Calle Arroyo, 68', 37.39725, -5.97599, 1.4, 'Caña Cruzcampo', 'Pizarra y barra (2024)', ST_SetSRID(ST_MakePoint(-5.97599, 37.39725), 4326)),
(10, 'Bar Casa Pepe', 'Avenida de Miraflores, 34', 37.404, -5.981, 1.5, 'Caña Cruzcampo', 'Carta taberna taurina (2024)', ST_SetSRID(ST_MakePoint(-5.981, 37.404), 4326)),
(11, 'Bodega San Rafael', 'Calle San Juan Bosco, 30', 37.39701, -5.97856, 1.4, 'Caña Cruzcampo', 'Carta tradicional abacería (2024)', ST_SetSRID(ST_MakePoint(-5.97856, 37.39701), 4326)),
(12, 'Cervecería Los Faroles', 'Calle San Juan Bosco, 12', 37.3968, -5.9789, 1.5, 'Caña Cruzcampo', 'Carta de tapas (2024)', ST_SetSRID(ST_MakePoint(-5.9789, 37.3968), 4326)),
(13, 'Bar Sacramento', 'Calle Arroyo, 28', 37.3965, -5.9775, 1.5, 'Caña Cruzcampo', 'Schlouk Map / Carta bar (2024)', ST_SetSRID(ST_MakePoint(-5.9775, 37.3965), 4326)),
(14, 'Santana Homenaje al Sabor', 'Calle Arroyo, 30', 37.3963, -5.9778, 1.6, 'Caña Cruzcampo', 'Carta y reseñas de clientes (2024)', ST_SetSRID(ST_MakePoint(-5.9778, 37.3963), 4326)),
(15, 'Bodega La Aurora', 'Calle Pérez Hervás, 8', 37.397, -5.98, 1.4, 'Caña Cruzcampo', 'Carta abacería (2024)', ST_SetSRID(ST_MakePoint(-5.98, 37.397), 4326)),
(16, 'Cervecería Bar G. Hijón', 'Ronda de Capuchinos, 1', 37.3985, -5.982, 1.5, 'Caña Cruzcampo', 'Carta y pizarra de caracoles/tapas (2024)', ST_SetSRID(ST_MakePoint(-5.982, 37.3985), 4326)),
(17, 'Bar Avelino', 'Calle Baltasar de Alcázar, 11', 37.4024, -5.96557, 1.3, 'Caña / botellín', 'Precios de barrio San Carlos (2024)', ST_SetSRID(ST_MakePoint(-5.96557, 37.4024), 4326)),
(18, 'Cervecería El Tremendo (Pío XII)', 'Calle Previsión, 10', 37.406, -5.9825, 1.4, 'Caña Cruzcampo tirada fría', 'Referencia histórica y carta fija (2024)', ST_SetSRID(ST_MakePoint(-5.9825, 37.406), 4326)),
(19, 'Bar Dos Hermanas', 'Calle Venecia, 14', 37.39533, -5.979, 1.4, 'Caña Cruzcampo', 'Carta local de barrio (2024)', ST_SetSRID(ST_MakePoint(-5.979, 37.39533), 4326)),
(20, 'Cervecería Vizcaíno', 'Calle Previsión, 2', 37.4063, -5.983, 1.5, 'Caña Cruzcampo', 'Carta de mariscos y caña (2024)', ST_SetSRID(ST_MakePoint(-5.983, 37.4063), 4326)),
(21, 'Cervecería La Roda', 'Calle José Laguillo, 27', 37.394, -5.978, 1.8, 'Caña / Tubo Cruzcampo', 'Carta José Laguillo / Santa Justa (2024)', ST_SetSRID(ST_MakePoint(-5.978, 37.394), 4326)),
(22, 'Marisquería El Marisquero', 'Calle Arroyo, 26', 37.39443, -5.98146, 1.7, 'Caña Cruzcampo', 'Carta UberEats / Local (2024)', ST_SetSRID(ST_MakePoint(-5.98146, 37.39443), 4326)),
(23, 'Casa Galán', 'Calle León XIII, 14', 37.4065, -5.985, 1.8, 'Caña de barril', 'Carta Gastrobar en redes (2024-2025)', ST_SetSRID(ST_MakePoint(-5.985, 37.4065), 4326)),
(24, 'Taberna La Viña Gilsan', 'Calle León XIII, 2', 37.4058, -5.986, 1.6, 'Caña de cerveza', 'Carta en local / reseñas (2024)', ST_SetSRID(ST_MakePoint(-5.986, 37.4058), 4326)),
(25, 'Berraco Sevilla', 'Carretera de Carmona, 14', 37.40278, -5.9623, 2.4, 'Tercio / Caña artesana', 'Carta Gastrobar contemporáneo (2024)', ST_SetSRID(ST_MakePoint(-5.9623, 37.40278), 4326)),
(26, 'Cervecería Café Dodge', 'Carretera de Carmona, 88', 37.4028, -5.9622, 1.8, 'Caña Cruzcampo', 'Carta UberEats / JustEat / Local (2024)', ST_SetSRID(ST_MakePoint(-5.9622, 37.4028), 4326)),
(27, 'Cervecería El Kiki', 'Calle Juan Antonio Cavestany, 20', 37.392, -5.979, 1.5, 'Caña Cruzcampo', 'Carta cervecería Santa Justa (2024)', ST_SetSRID(ST_MakePoint(-5.979, 37.392), 4326)),
(28, 'Bar Kiki Arroyo', 'Calle Arroyo, 50', 37.39328, -5.98276, 1.5, 'Caña Cruzcampo', 'Carta tradicional en barra (2024)', ST_SetSRID(ST_MakePoint(-5.98276, 37.39328), 4326)),
(29, 'Bar Santa Marina', 'Calle San Luis, 95', 37.40107, -5.98888, 1.5, 'Caña Cruzcampo', 'Pizarra y terraza en San Luis (2024)', ST_SetSRID(ST_MakePoint(-5.98888, 37.40107), 4326)),
(30, 'Bodeguita El Acerao', 'Calle Matahacas, 22', 37.3942, -5.986, 1.4, 'Caña Cruzcampo', 'Schlouk Map / Carta oficial (2024)', ST_SetSRID(ST_MakePoint(-5.986, 37.3942), 4326));

-- Ajuste de la secuencia para futuras inserciones
SELECT setval('bares_id_seq', (SELECT MAX(id) FROM bares));
COMMIT;
