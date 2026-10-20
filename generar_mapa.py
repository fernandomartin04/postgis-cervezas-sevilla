import json

with open('scratch_30_bares.json', 'r', encoding='utf-8') as f:
    bares = json.load(f)

json_bares_str = json.dumps(bares, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Buscador Geoespacial de Cervezas en Sevilla - PostGIS</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      display: flex;
      height: 100vh;
      background: #0f172a;
      color: #f8fafc;
      overflow: hidden;
    }
    
    /* Panel lateral de control interactivo */
    #sidebar {
      width: 380px;
      background: #1e293b;
      display: flex;
      flex-direction: column;
      border-right: 1px solid #334155;
      z-index: 1000;
      box-shadow: 4px 0 20px rgba(0,0,0,0.4);
    }
    
    .sidebar-header {
      padding: 16px 20px;
      background: #0f172a;
      border-bottom: 1px solid #334155;
    }
    .sidebar-header h1 {
      margin: 0;
      font-size: 1.15rem;
      font-weight: 700;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .sidebar-header .subtitle {
      font-size: 0.78rem;
      color: #94a3b8;
      margin-top: 4px;
    }

    .sidebar-content {
      flex: 1;
      overflow-y: auto;
      padding: 18px 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .control-card {
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 10px;
      padding: 14px;
    }
    .control-card h3 {
      margin: 0 0 10px 0;
      font-size: 0.88rem;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .input-row {
      display: flex;
      gap: 10px;
      margin-bottom: 10px;
    }
    .input-group {
      flex: 1;
    }
    .input-group label {
      display: block;
      font-size: 0.75rem;
      color: #64748b;
      margin-bottom: 4px;
    }
    .input-group input[type="number"] {
      width: 100%;
      background: #1e293b;
      border: 1px solid #475569;
      color: #fff;
      padding: 7px 10px;
      border-radius: 6px;
      font-size: 0.85rem;
    }

    .slider-container {
      margin-top: 8px;
    }
    .slider-header {
      display: flex;
      justify-content: space-between;
      font-size: 0.85rem;
      margin-bottom: 6px;
    }
    .slider-header .radius-badge {
      background: #0284c7;
      color: #fff;
      padding: 2px 8px;
      border-radius: 12px;
      font-weight: 700;
    }
    input[type="range"] {
      width: 100%;
      accent-color: #38bdf8;
      cursor: pointer;
    }

    .btn-reset {
      width: 100%;
      background: #334155;
      color: #e2e8f0;
      border: 1px solid #475569;
      padding: 8px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.82rem;
      font-weight: 600;
      transition: background 0.2s;
      margin-top: 6px;
    }
    .btn-reset:hover {
      background: #475569;
    }

    /* Tarjeta del ganador */
    .winner-card {
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(6, 78, 59, 0.3));
      border: 1px solid #10b981;
      border-radius: 10px;
      padding: 14px;
      position: relative;
    }
    .winner-badge {
      display: inline-block;
      background: #10b981;
      color: #064e3b;
      font-size: 0.7rem;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 10px;
      text-transform: uppercase;
      margin-bottom: 8px;
    }
    .winner-name {
      font-size: 1.05rem;
      font-weight: 700;
      color: #fff;
      margin-bottom: 4px;
    }
    .winner-details {
      font-size: 0.82rem;
      color: #cbd5e1;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 8px;
    }
    .winner-price {
      font-size: 1.3rem;
      font-weight: 800;
      color: #34d399;
    }

    /* Lista de resultados en radio */
    .results-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
      max-height: 280px;
      overflow-y: auto;
    }
    .bar-item {
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 10px 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      transition: border-color 0.2s, background 0.2s;
    }
    .bar-item:hover {
      background: #1e293b;
      border-color: #38bdf8;
    }
    .bar-item-info strong {
      font-size: 0.85rem;
      display: block;
      color: #f1f5f9;
    }
    .bar-item-info span {
      font-size: 0.75rem;
      color: #94a3b8;
    }
    .bar-item-price {
      text-align: right;
    }
    .bar-item-price .price-tag {
      font-weight: 700;
      font-size: 0.95rem;
      color: #f59e0b;
    }
    .bar-item-price .dist-tag {
      font-size: 0.72rem;
      color: #64748b;
      display: block;
    }

    /* Mapa */
    #map-container {
      flex: 1;
      position: relative;
    }
    #map {
      width: 100%;
      height: 100%;
    }

    .legend {
      position: absolute;
      bottom: 25px;
      right: 25px;
      background: rgba(15, 23, 42, 0.92);
      backdrop-filter: blur(8px);
      padding: 12px 16px;
      border-radius: 10px;
      border: 1px solid #334155;
      font-size: 0.78rem;
      z-index: 1000;
      box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
    }
    .legend-color {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      border: 2px solid #fff;
    }
  </style>
</head>
<body>
  <!-- Panel de control interactivo -->
  <aside id="sidebar">
    <div class="sidebar-header">
      <h1>🍻 Cervezas Sevilla</h1>
      <div class="subtitle">Ampliación de Bases de Datos · PostGIS + PostgreSQL</div>
    </div>

    <div class="sidebar-content">
      <!-- Controles de Coordenadas y Radio -->
      <div class="control-card">
        <h3>📍 Ubicación y Radio</h3>
        <div class="input-row">
          <div class="input-group">
            <label>Latitud</label>
            <input type="number" id="inputLat" step="0.0001" value="37.40193" />
          </div>
          <div class="input-group">
            <label>Longitud</label>
            <input type="number" id="inputLon" step="0.0001" value="-5.97479" />
          </div>
        </div>

        <div class="slider-container">
          <div class="slider-header">
            <span>Radio de búsqueda:</span>
            <span class="radius-badge" id="radiusBadge">500 m</span>
          </div>
          <input type="range" id="inputRadius" min="100" max="1500" step="50" value="500" />
        </div>

        <button class="btn-reset" id="btnReset">🏠 Volver a mi Casa (Valdés Leal)</button>
        <div style="font-size:0.72rem; color:#64748b; margin-top:8px; text-align:center;">
          💡 <em>Haz clic o arrastra el marcador azul en el mapa</em>
        </div>
      </div>

      <!-- Tarjeta Bar más Barato -->
      <div id="winnerContainer">
        <div class="winner-card">
          <div class="winner-badge">🏆 Más Barato en el Radio</div>
          <div class="winner-name" id="winnerName">Cargando...</div>
          <div id="winnerAddress" style="font-size:0.76rem; color:#94a3b8;">-</div>
          <div class="winner-details">
            <div class="winner-price" id="winnerPrice">0.00 €</div>
            <div id="winnerDist" style="color:#6ee7b7; font-weight:600;">-</div>
          </div>
        </div>
      </div>

      <!-- Lista de Bares en Radio -->
      <div class="control-card" style="flex:1; display:flex; flex-direction:column;">
        <h3>
          <span>Bares dentro del radio</span>
          <span id="countBadge" style="background:#334155; padding:2px 8px; border-radius:10px; font-size:0.75rem; color:#38bdf8;">0</span>
        </h3>
        <div class="results-list" id="resultsList">
          <!-- Bares dinámicos -->
        </div>
      </div>
    </div>
  </aside>

  <!-- Mapa -->
  <main id="map-container">
    <div id="map"></div>

    <div class="legend">
      <div style="font-weight:700; margin-bottom:8px; color:#38bdf8;">Precios Caña</div>
      <div class="legend-item"><span class="legend-color" style="background:#10b981;"></span> &le; 1.40 € (Económico)</div>
      <div class="legend-item"><span class="legend-color" style="background:#f59e0b;"></span> 1.50 € - 1.70 € (Estándar)</div>
      <div class="legend-item"><span class="legend-color" style="background:#ef4444;"></span> &ge; 1.80 € (Gastrobar)</div>
      <div class="legend-item" style="margin-top:8px; border-top:1px solid #334155; padding-top:6px;">
        <span style="display:inline-block; width:12px; height:12px; border:2px dashed #38bdf8; border-radius:50%;"></span>
        Radio ST_DWithin
      </div>
    </div>
  </main>

  <script>
    const HOME_LAT = 37.40193;
    const HOME_LON = -5.97479;
    const DEFAULT_RADIUS = 500;

    const bares = """ + json_bares_str + """;

    // Inicializar mapa centrado en casa
    const map = L.map('map').setView([HOME_LAT, HOME_LON], 15);

    // Capas base de mapas
    const esriStreet = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
      attribution: '&copy; Esri, DeLorme, NAVTEQ',
      maxZoom: 19
    });

    const osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19
    });

    const esriSat = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      attribution: '&copy; Esri World Imagery',
      maxZoom: 19
    });

    // Activar por defecto Esri Callejero (no bloquea peticiones locales file:// ni requiere cabecera Referer)
    esriStreet.addTo(map);

    // Selector de capas en la esquina superior derecha
    L.control.layers({
      'Callejero (Sin bloqueo)': esriStreet,
      'OpenStreetMap': osm,
      'Satélite': esriSat
    }, null, { position: 'topright' }).addTo(map);

    // Círculo de cobertura espacial (equivalente a ST_DWithin)
    let circle = L.circle([HOME_LAT, HOME_LON], {
      radius: DEFAULT_RADIUS,
      color: '#38bdf8',
      fillColor: '#38bdf8',
      fillOpacity: 0.12,
      weight: 2,
      dashArray: '5, 5'
    }).addTo(map);

    // Marcador del usuario (arrastrable)
    const userIcon = L.divIcon({
      html: '<div style="background:#0284c7; width:26px; height:26px; border-radius:50%; border:3px solid #fff; box-shadow:0 0 12px rgba(0,0,0,0.6); display:flex; align-items:center; justify-content:center; color:#fff; font-size:13px; cursor:move;">📍</div>',
      className: '',
      iconSize: [26, 26],
      iconAnchor: [13, 13]
    });

    let userMarker = L.marker([HOME_LAT, HOME_LON], { 
      icon: userIcon, 
      draggable: true 
    }).addTo(map).bindPopup('<strong>Tu Ubicación</strong><br>Arrastra este marcador o haz clic en el mapa.');

    // Almacén de marcadores de bares
    const barMarkers = [];

    bares.forEach(b => {
      let color = '#f59e0b';
      if (b.precio_cana <= 1.40) color = '#10b981';
      else if (b.precio_cana >= 1.80) color = '#ef4444';

      const icon = L.divIcon({
        html: '<div id="marker-icon-' + b.id + '" style="background:' + color + '; width:26px; height:26px; border-radius:50%; border:2px solid white; box-shadow:0 2px 6px rgba(0,0,0,0.4); display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:10px; color:white; transition:all 0.3s;">' + b.precio_cana.toFixed(2) + '€</div>',
        className: '',
        iconSize: [26, 26],
        iconAnchor: [13, 13]
      });

      const m = L.marker([b.lat, b.lon], { icon: icon }).addTo(map);
      barMarkers.push({ data: b, marker: m });
    });

    // Fórmula de Haversine idéntica al cálculo geodésico de PostGIS (ST_Distance(geom::geography))
    function calcDistance(lat1, lon1, lat2, lon2) {
      const R = 6371000; // metros
      const dLat = (lat2 - lat1) * Math.PI / 180;
      const dLon = (lon2 - lon1) * Math.PI / 180;
      const a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
        Math.sin(dLon/2) * Math.sin(dLon/2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
      return Math.round(R * c);
    }

    // Función principal de actualización espacial
    function updateSpatialQuery() {
      const uLat = parseFloat(document.getElementById('inputLat').value);
      const uLon = parseFloat(document.getElementById('inputLon').value);
      const radius = parseInt(document.getElementById('inputRadius').value);

      document.getElementById('radiusBadge').innerText = radius + ' m';

      // Actualizar posición del marcador y círculo
      userMarker.setLatLng([uLat, uLon]);
      circle.setLatLng([uLat, uLon]);
      circle.setRadius(radius);

      // Filtrar y calcular distancias (ST_DWithin + ST_Distance)
      const insideBars = [];

      barMarkers.forEach(bm => {
        const d = calcDistance(uLat, uLon, bm.data.lat, bm.data.lon);
        bm.currentDistance = d;
        const isInside = d <= radius;

        const iconEl = document.getElementById('marker-icon-' + bm.data.id);
        if (iconEl) {
          if (isInside) {
            iconEl.style.opacity = '1';
            iconEl.style.transform = 'scale(1)';
            iconEl.style.boxShadow = '0 0 10px rgba(56, 189, 248, 0.8)';
          } else {
            iconEl.style.opacity = '0.35';
            iconEl.style.transform = 'scale(0.85)';
            iconEl.style.boxShadow = 'none';
          }
        }

        // Actualizar popup del bar
        bm.marker.bindPopup(
          '<div style="font-size:13px; color:#1e293b; line-height:1.4;">' +
          '<strong style="color:#0f172a; font-size:14px;">' + bm.data.nombre + '</strong><br>' +
          '📍 ' + bm.data.direccion + '<br>' +
          '🍺 <strong>' + bm.data.precio_cana.toFixed(2) + ' €</strong> (' + bm.data.formato + ')<br>' +
          '📏 Distancia actual: <strong>' + d + ' m</strong> ' + (isInside ? '✅ <span style=\"color:#059669;\">En radio</span>' : '❌ Fuera') + '<br>' +
          '<small style="color:#64748b;">' + bm.data.fuente + '</small>' +
          '</div>'
        );

        if (isInside) {
          insideBars.push({ ...bm.data, currentDistance: d, markerObj: bm.marker });
        }
      });

      // Ordenar por precio ascendente y luego por distancia (ORDER BY precio_cana ASC, distancia ASC)
      insideBars.sort((a, b) => {
        if (a.precio_cana !== b.precio_cana) return a.precio_cana - b.precio_cana;
        return a.currentDistance - b.currentDistance;
      });

      // Actualizar tarjeta del ganador
      const winnerCard = document.getElementById('winnerContainer');
      if (insideBars.length > 0) {
        winnerCard.style.display = 'block';
        const best = insideBars[0];
        document.getElementById('winnerName').innerText = best.nombre;
        document.getElementById('winnerAddress').innerText = best.direccion;
        document.getElementById('winnerPrice').innerText = best.precio_cana.toFixed(2) + ' €';
        document.getElementById('winnerDist').innerText = 'a ' + best.currentDistance + ' metros';

        // Resaltar icono del ganador
        const bestIcon = document.getElementById('marker-icon-' + best.id);
        if (bestIcon) {
          bestIcon.style.boxShadow = '0 0 18px 4px #10b981';
          bestIcon.style.transform = 'scale(1.25)';
          bestIcon.style.zIndex = '999';
        }
      } else {
        winnerCard.style.display = 'none';
      }

      // Actualizar lista en panel lateral
      const listContainer = document.getElementById('resultsList');
      document.getElementById('countBadge').innerText = insideBars.length;
      listContainer.innerHTML = '';

      if (insideBars.length === 0) {
        listContainer.innerHTML = '<div style=\"text-align:center; color:#64748b; padding:20px; font-size:0.85rem;\">No hay bares a menos de ' + radius + ' m.<br>Prueba a ampliar el radio.</div>';
      } else {
        insideBars.forEach((bar, idx) => {
          const div = document.createElement('div');
          div.className = 'bar-item';
          div.innerHTML = `
            <div class="bar-item-info">
              <strong>${idx === 0 ? '🏆 ' : ''}${bar.nombre}</strong>
              <span>${bar.direccion}</span>
            </div>
            <div class="bar-item-price">
              <span class="price-tag" style="color:${bar.precio_cana <= 1.4 ? '#10b981' : bar.precio_cana >= 1.8 ? '#ef4444' : '#f59e0b'}">${bar.precio_cana.toFixed(2)} €</span>
              <span class="dist-tag">${bar.currentDistance} m</span>
            </div>
          `;
          div.onclick = () => {
            bar.markerObj.openPopup();
            map.panTo([bar.lat, bar.lon]);
          };
          listContainer.appendChild(div);
        });
      }
    }

    // Eventos de interacción
    document.getElementById('inputRadius').addEventListener('input', updateSpatialQuery);

    document.getElementById('inputLat').addEventListener('change', updateSpatialQuery);
    document.getElementById('inputLon').addEventListener('change', updateSpatialQuery);

    userMarker.on('drag', function(e) {
      const pos = e.target.getLatLng();
      document.getElementById('inputLat').value = pos.lat.toFixed(5);
      document.getElementById('inputLon').value = pos.lng.toFixed(5);
      updateSpatialQuery();
    });

    map.on('click', function(e) {
      document.getElementById('inputLat').value = e.latlng.lat.toFixed(5);
      document.getElementById('inputLon').value = e.latlng.lng.toFixed(5);
      updateSpatialQuery();
    });

    document.getElementById('btnReset').addEventListener('click', function() {
      document.getElementById('inputLat').value = HOME_LAT;
      document.getElementById('inputLon').value = HOME_LON;
      document.getElementById('inputRadius').value = DEFAULT_RADIUS;
      map.setView([HOME_LAT, HOME_LON], 15);
      updateSpatialQuery();
    });

    // Ejecución inicial
    updateSpatialQuery();
  </script>
</body>
</html>
"""

with open('mapa_cervezas.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print('mapa_cervezas.html actualizado con interfaz interactiva!')
