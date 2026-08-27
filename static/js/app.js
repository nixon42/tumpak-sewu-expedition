
    // =========================================================================
    // 1. ROUTE MAP & REACTIVE GIS STATE ENGINE (REQUIREMENT R1 & R3.2)
    // =========================================================================
    let routeMapInstance = null;
    let mapMarkers = {};
    let routePolylines = {};
    let currentMapPlan = 2; // Default Plan 2

    
    const DESTINATIONS_DATA = {
      goatetes: {
        id: 'Goa Tetes',
        latLng: [-8.2325, 112.9167],
        title: 'Opsi A: Goa Tetes (Gua Karst)',
        desc: '0 km dari Tumpak Sewu (Loop dasar tebing). Stalaktit aktif & air belerang.',
        distFromTumpak: '0 km (Loop Kaki)',
        color: '#38bdf8',
        gmapsQuery: 'Goa Tetes Sidomulyo Pronojiwo Lumajang'
      },
      terassemeru: {
        id: 'Teras Semeru',
        latLng: [-8.2160, 112.9620],
        title: 'Opsi F: Teras Semeru Sumberurip',
        desc: '±4.5 km dari Tumpak Sewu (~12 mnt). Gazebo santai & panorama megah Semeru.',
        distFromTumpak: '±4.5 km (12 mnt)',
        color: '#f43f5e',
        gmapsQuery: 'Teras Semeru Sumberurip Pronojiwo Lumajang'
      },
      kapasbiru: {
        id: 'Coban Kapas Biru',
        latLng: [-8.2255, 112.9358],
        title: 'Opsi D: Coban Kapas Biru (Gardu Panorama)',
        desc: '±4.5 km dari Tumpak Sewu (~10 mnt). View megah air terjun 100m bertingkat & Semeru.',
        distFromTumpak: '±4.5 km (10 mnt)',
        color: '#10b981',
        gmapsQuery: 'Air Terjun Kapas Biru Pronojiwo Lumajang'
      },
      kabutpelangi: {
        id: 'Kabut Pelangi',
        latLng: [-8.2435, 112.9510],
        title: 'Opsi E: Air Terjun Kabut Pelangi',
        desc: '±6.5 km dari Tumpak Sewu (~15 mnt). Fenomena pelangi abadi di kabut air terjun 100m.',
        distFromTumpak: '±6.5 km (15 mnt)',
        color: '#06b6d4',
        gmapsQuery: 'Air Terjun Kabut Pelangi Pronojiwo Lumajang'
      },
      pantaimalang: {
        id: 'Pantai Selatan Malang',
        latLng: [-8.4042, 112.5372],
        title: 'Opsi C: Pantai Balekambang / JLS Malang',
        desc: '±60 km via Dampit (1.5–2 jam). Pura pulau karang & kuliner ikan bakar.',
        distFromTumpak: '±60 km (1.5 jam)',
        color: '#f59e0b',
        gmapsQuery: 'Pantai Balekambang Malang Selatan'
      },
      bromo: {
        id: 'Bromo Sunrise',
        latLng: [-7.9425, 112.9530],
        title: 'Opsi B: Kaldera Bromo Sunrise / TNBTS',
        desc: '±75 km via Senduro (2.5–3.5 jam). Lautan pasir & golden sunrise.',
        distFromTumpak: '±75 km (2.5 jam)',
        color: '#c084fc',
        gmapsQuery: 'Gunung Bromo TNBTS Jawa Timur'
      }
    };

    let destMarkers = {};

    const REST_STOPS_DATA = {
      masjid_dampit: {
        id: 'Masjid Baiturrahim Dampit',
        latLng: [-8.2105, 112.7502],
        title: '🕌 Masjid Besar Baiturrahim Dampit',
        category: 'Tidur Pulas (Plan 2 & 3)',
        desc: 'Serambi karpet empuk, toilet bersih, tidur pulas & salat Subuh sebelum trekking.',
        color: '#10b981',
        gmapsQuery: 'Masjid Besar Baiturrahim Dampit Malang'
      },
      spbu_dampit: {
        id: 'SPBU Dampit',
        latLng: [-8.2144, 112.7505],
        title: '⛽ SPBU 54.651.17 Dampit (Rest Area 24 Jam)',
        category: 'Rest Area (Plan 2 & 3)',
        desc: 'Rest area 24 jam, pengisian Pertalite penuh, ATM, minimarket & toilet.',
        color: '#10b981',
        gmapsQuery: 'SPBU Pertamina Dampit Malang'
      },
      roketto_blitar: {
        id: 'Roketto Coffee Blitar',
        latLng: [-8.0935, 112.1760],
        title: '☕ Roketto Coffee & Co Blitar (24 Jam)',
        category: 'Kafe 24h (Plan 4)',
        desc: 'Jl. Veteran 141, kafe modern 24 jam, AC sejuk, colokan listrik & Wi-Fi kencang.',
        color: '#a855f7',
        gmapsQuery: 'Roketto Coffee Blitar'
      },
      warkop_blitar: {
        id: 'Warkop Agam Blitar',
        latLng: [-8.0990, 112.1640],
        title: '🍜 Warkop Agam Patria Blitar (24 Jam)',
        category: 'Warkop (Plan 4)',
        desc: 'Jl. Mastrip, warkop legendaris 24 jam, kopi Aceh saring & mie instan malam.',
        color: '#a855f7',
        gmapsQuery: 'Warkop Agam Blitar'
      },
      roketto_malang: {
        id: 'Roketto Coffee Malang',
        latLng: [-7.9427, 112.6225],
        title: '☕ Roketto Coffee Suhat Malang (24 Jam)',
        category: 'Kafe 24h (Plan 1)',
        desc: 'Jl. Kendalsari / Suhat, kafe 24 jam estetik, Wi-Fi kencang, AC & colokan.',
        color: '#38bdf8',
        gmapsQuery: 'Roketto Coffee Malang'
      }
    };

    let restMarkers = {};

    let destPolylines = {};

    const WAYPOINTS_DATA = {
      kediri: { 
        latLng: [-7.8166, 112.0167], 
        title: 'Titik Kumpul: Simpang Lima Gumul Kediri', 
        desc: 'Briefing, cek fisik motor & tekanan ban.',
        gmapsQuery: 'Monumen Simpang Lima Gumul Kediri'
      },
      blitar: { 
        latLng: [-8.0983, 112.1681], 
        title: 'Blitar Kota (KM 42)', 
        desc: 'Plan 4: Kafe 24 Jam Roketto / Warkop Agam. Plan 3: Refuel SPBU Garum.',
        gmapsQuery: 'Alun Alun Kota Blitar'
      },
      wlingi: { 
        latLng: [-8.0850, 112.3180], 
        title: 'Wlingi (KM 62)', 
        desc: 'Aspal datar mulus koridor Blitar Timur.',
        gmapsQuery: 'Pasar Wlingi Blitar'
      },
      karangkates: { 
        latLng: [-8.1520, 112.4480], 
        title: 'Bendungan Karangkates (KM 80)', 
        desc: 'Puncak elevasi rute selatan (hanya 350 mdpl).',
        gmapsQuery: 'Bendungan Sutami Karangkates Malang'
      },
      kepanjen: { 
        latLng: [-8.1310, 112.5720], 
        title: 'Kepanjen (KM 87)', 
        desc: 'Titik regrouping & makan malam kepulangan.',
        gmapsQuery: 'Alun Alun Kepanjen Malang'
      },
      ngantang: { 
        latLng: [-7.8427, 112.3688], 
        title: 'SPBU Pertamina Ngantang (KM 58)', 
        desc: 'Refuel bensin wajib sebelum tanjakan Pujon Pass.',
        gmapsQuery: 'SPBU Pertamina Ngantang Malang'
      },
      pujon: { 
        latLng: [-7.8547, 112.4746], 
        title: 'Pujon Pass (KM 76)', 
        desc: 'Puncak 1.180 mdpl. Awal turunan kritis 970m Batu.',
        gmapsQuery: 'Pujon Malang Jawa Timur'
      },
      malang: { 
        latLng: [-7.9797, 112.6304], 
        title: 'Malang Kota (KM 98)', 
        desc: 'Plan 1: Warkop 24 Jam Malang. Plan 2: Bypass Flyover.',
        gmapsQuery: 'Alun Alun Tugu Kota Malang'
      },
      dampit: { 
        latLng: [-8.2144, 112.7505], 
        title: 'Rest Area Dampit (KM 118)', 
        desc: 'Plan 3 & Plan 2: Rehat tidur pulas di Masjid Baiturrahim / SPBU 54.651.17.',
        gmapsQuery: 'SPBU Pertamina Dampit Malang'
      },
      pronojiwo: { 
        latLng: [-8.2315, 112.9180], 
        title: 'Base Tumpak Sewu (KM 158/180)', 
        desc: 'Tiba 06:00 WIB. Loket buka & Semeru view.',
        gmapsQuery: 'Wisata Air Terjun Tumpak Sewu Lumajang'
      }
    };

    const ROUTE_COORDS_KEDIRI_MALANG = [
      [-7.8166, 112.0167], [-7.7711, 112.1978], [-7.7889, 112.2856],
      [-7.8427, 112.3688], [-7.8547, 112.4746], [-7.8712, 112.5270],
      [-7.9797, 112.6304]
    ];

    const ROUTE_COORDS_MALANG_DAMPIT = [
      [-7.9797, 112.6304], [-8.0610, 112.6280], [-8.1630, 112.7000],
      [-8.2144, 112.7505]
    ];

    const ROUTE_COORDS_DAMPIT_PRONOJIWO = [
      [-8.2144, 112.7505], [-8.2380, 112.8250], [-8.2560, 112.8750],
      [-8.2315, 112.9180]
    ];

    const ROUTE_COORDS_KEDIRI_BLITAR_DAMPIT = [
      [-7.8166, 112.0167], [-7.9150, 112.0250], [-8.0050, 112.0850],
      [-8.0983, 112.1681], [-8.0850, 112.3180], [-8.1250, 112.3850],
      [-8.1520, 112.4480], [-8.1310, 112.5720], [-8.1750, 112.6450],
      [-8.1630, 112.7000], [-8.2144, 112.7505]
    ];

    function initRouteMap() {
      if (typeof L === 'undefined') {
        const fallback = document.getElementById('mapFallback');
        if (fallback) fallback.style.display = 'block';
        return;
      }

      try {
        routeMapInstance = L.map('routeMap', {
          center: [-8.05, 112.5],
          zoom: 9,
          scrollWheelZoom: false,
          zoomControl: false
        });
        L.control.zoom({ position: 'topright' }).addTo(routeMapInstance);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '&copy; OpenStreetMap contributors',
          maxZoom: 18
        }).addTo(routeMapInstance);

        routePolylines.pujonSeg1 = L.polyline(ROUTE_COORDS_KEDIRI_MALANG, { color: '#38bdf8', weight: 4, opacity: 0.85 }).addTo(routeMapInstance);
        routePolylines.pujonSeg2 = L.polyline(ROUTE_COORDS_MALANG_DAMPIT, { color: '#10b981', weight: 4, opacity: 0.85 }).addTo(routeMapInstance);
        routePolylines.alpineSeg = L.polyline(ROUTE_COORDS_DAMPIT_PRONOJIWO, { color: '#f59e0b', weight: 4, opacity: 0.85, dashArray: '6, 6' }).addTo(routeMapInstance);
        routePolylines.blitarSeg = L.polyline(ROUTE_COORDS_KEDIRI_BLITAR_DAMPIT, { color: '#a855f7', weight: 4, opacity: 0.85 }).addTo(routeMapInstance);

        for (const [key, wp] of Object.entries(WAYPOINTS_DATA)) {
          const marker = L.circleMarker(wp.latLng, {
            radius: (key === 'kediri' || key === 'pronojiwo' || key === 'dampit' || key === 'pujon' || key === 'blitar') ? 7 : 5,
            fillColor: (key === 'pronojiwo') ? '#fbbf24' : (key === 'dampit') ? '#10b981' : (key === 'pujon') ? '#ef4444' : (key === 'blitar') ? '#a855f7' : '#38bdf8',
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.9
          }).addTo(routeMapInstance);

          const destTarget = encodeURIComponent(wp.gmapsQuery || `${wp.latLng[0]},${wp.latLng[1]}`);
          const gmapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${destTarget}`;
          marker.bindPopup(`
            <div style="font-family: inherit;">
              <strong style="font-size: 0.82rem; color: #f8fafc; display: block; margin-bottom: 3px; font-weight: 700; line-height: 1.25;">${wp.title}</strong>
              <p style="font-size: 0.72rem; color: #94a3b8; margin: 0 0 8px 0; line-height: 1.3;">${wp.desc}</p>
              <a href="${gmapsUrl}" target="_blank" rel="noopener noreferrer" style="display: flex; align-items: center; justify-content: center; gap: 5px; width: 100%; padding: 5px 8px; background: #0284c7; color: #ffffff; text-decoration: none; border-radius: 5px; font-size: 0.72rem; font-weight: 700; box-sizing: border-box; transition: background 0.2s;">
                <svg style="width:12px;height:12px;fill:currentColor;" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                Buka Google Maps ➔
              </a>
            </div>
          `, {
            maxWidth: 210,
            minWidth: 140,
            autoPanPadding: [8, 8]
          });
          mapMarkers[key] = marker;
        }

        // 2ND DESTINATIONS CANDIDATE MARKERS & DISTANCE CONNECTORS
        const tumpakLatLng = WAYPOINTS_DATA.pronojiwo.latLng;
        for (const [dKey, dest] of Object.entries(DESTINATIONS_DATA)) {
          // Visual connector line from Tumpak Sewu to candidate destination
          const connector = L.polyline([tumpakLatLng, dest.latLng], {
            color: dest.color,
            weight: 2,
            opacity: 0.7,
            dashArray: '5, 8'
          }).addTo(routeMapInstance);
          destPolylines[dKey] = connector;

          // Custom Destination Marker (Square/Diamond distinct style)
          const destMarker = L.circleMarker(dest.latLng, {
            radius: (dKey === 'kapasbiru' || dKey === 'goatetes') ? 7 : 6,
            fillColor: dest.color,
            color: '#ffffff',
            weight: 2.5,
            opacity: 1,
            fillOpacity: 0.95
          }).addTo(routeMapInstance);

          const destTarget = encodeURIComponent(dest.gmapsQuery || `${dest.latLng[0]},${dest.latLng[1]}`);
          const gmapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${destTarget}`;

          destMarker.bindPopup(`
            <div style="font-family: inherit;">
              <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; margin-bottom: 4px;">
                <span style="font-size: 0.68rem; font-weight: 700; color: ${dest.color}; background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px; border: 1px solid ${dest.color};">Destinasi Kedua</span>
                <span style="font-size: 0.7rem; font-weight: 800; color: #f1f5f9;">📏 ${dest.distFromTumpak}</span>
              </div>
              <strong style="font-size: 0.82rem; color: #f8fafc; display: block; margin-bottom: 3px; font-weight: 700; line-height: 1.25;">${dest.title}</strong>
              <p style="font-size: 0.72rem; color: #94a3b8; margin: 0 0 8px 0; line-height: 1.3;">${dest.desc}</p>
              <a href="${gmapsUrl}" target="_blank" rel="noopener noreferrer" style="display: flex; align-items: center; justify-content: center; gap: 5px; width: 100%; padding: 5px 8px; background: #0284c7; color: #ffffff; text-decoration: none; border-radius: 5px; font-size: 0.72rem; font-weight: 700; box-sizing: border-box; transition: background 0.2s;">
                <svg style="width:12px;height:12px;fill:currentColor;" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                Buka Google Maps ➔
              </a>
            </div>
          `, {
            maxWidth: 220,
            minWidth: 150,
            autoPanPadding: [8, 8]
          });

          destMarkers[dKey] = destMarker;
        }

        // REST STOPS MARKERS
        for (const [rKey, rest] of Object.entries(REST_STOPS_DATA)) {
          const restMarker = L.circleMarker(rest.latLng, {
            radius: 6,
            fillColor: rest.color,
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.95
          }).addTo(routeMapInstance);

          const destTarget = encodeURIComponent(rest.gmapsQuery || `${rest.latLng[0]},${rest.latLng[1]}`);
          const gmapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${destTarget}`;

          restMarker.bindPopup(`
            <div style="font-family: inherit;">
              <div style="display: flex; align-items: center; justify-content: space-between; gap: 6px; margin-bottom: 4px;">
                <span style="font-size: 0.68rem; font-weight: 700; color: ${rest.color}; background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px; border: 1px solid ${rest.color};">Titik Rehat</span>
                <span style="font-size: 0.68rem; font-weight: 700; color: #cbd5e1;">${rest.category}</span>
              </div>
              <strong style="font-size: 0.82rem; color: #f8fafc; display: block; margin-bottom: 3px; font-weight: 700; line-height: 1.25;">${rest.title}</strong>
              <p style="font-size: 0.72rem; color: #94a3b8; margin: 0 0 8px 0; line-height: 1.3;">${rest.desc}</p>
              <a href="${gmapsUrl}" target="_blank" rel="noopener noreferrer" style="display: flex; align-items: center; justify-content: center; gap: 5px; width: 100%; padding: 5px 8px; background: #0284c7; color: #ffffff; text-decoration: none; border-radius: 5px; font-size: 0.72rem; font-weight: 700; box-sizing: border-box; transition: background 0.2s;">
                <svg style="width:12px;height:12px;fill:currentColor;" viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                Buka Google Maps ➔
              </a>
            </div>
          `, {
            maxWidth: 220,
            minWidth: 150,
            autoPanPadding: [8, 8]
          });

          restMarkers[rKey] = restMarker;
        }



        updateMapVisualPlan(currentMapPlan);
      } catch (e) {
        console.warn('Leaflet map initialization skipped/fallback:', e);
        const fallback = document.getElementById('mapFallback');
        if (fallback) fallback.style.display = 'block';
      }
    }

    function updateMapVisualPlan(planNum) {
      currentMapPlan = planNum;
      const indicator = document.getElementById('mapPlanIndicator');
      const badgeDetail = document.getElementById('routePlanBadgeDetail');
      const svgHazardBanner = document.getElementById('svgHazardBanner');
      const svgBlitarBanner = document.getElementById('svgBlitarBanner');
      const svgPujonArea = document.getElementById('svgPujonArea');
      const svgPujonLine = document.getElementById('svgPujonLine');
      const svgBlitarArea = document.getElementById('svgBlitarArea');
      const svgBlitarLine = document.getElementById('svgBlitarLine');
      const svgPeak = document.getElementById('svgPeak') || document.getElementById('svgElevationPeak');
      const svgDotMalang = document.getElementById('svgDotMalang');
      const svgTextMalang = document.getElementById('svgTextMalang');

      if (planNum === 1) {
        if (indicator) { indicator.innerText = 'Plan 1: Transit Warkop Malang Kota'; indicator.style.color = 'var(--sky-400)'; }
        if (badgeDetail) { badgeDetail.innerText = '☕ Transit Warkop 24h'; badgeDetail.className = 'badge badge-sky-soft'; }
        if (svgHazardBanner) svgHazardBanner.style.display = 'block';
        if (svgBlitarBanner) svgBlitarBanner.style.display = 'none';
        if (svgPujonArea) svgPujonArea.style.display = 'block';
        if (svgPujonLine) svgPujonLine.style.display = 'block';
        if (svgBlitarArea) svgBlitarArea.style.display = 'none';
        if (svgBlitarLine) svgBlitarLine.style.display = 'none';
        if (svgPeak) { svgPeak.innerText = 'Puncak: 1.180 mdpl (Pujon)'; svgPeak.style.color = 'var(--sky-400)'; svgPeak.style.borderColor = 'rgba(56,189,248,0.2)'; svgPeak.style.background = 'rgba(56,189,248,0.1)'; }
        if (svgDotMalang) svgDotMalang.style.display = 'block';
        if (svgTextMalang) { svgTextMalang.style.display = 'block'; svgTextMalang.textContent = 'Malang (Transit 2j 45m)'; }
      } else if (planNum === 2) {
        if (indicator) { indicator.innerText = 'Plan 2: Gas Terus Turen / Dampit (Pujon Pass)'; indicator.style.color = 'var(--emerald-400)'; }
        if (badgeDetail) { badgeDetail.innerText = '👑 TOP RECOMMENDED'; badgeDetail.className = 'badge badge-emerald-soft'; }
        if (svgHazardBanner) svgHazardBanner.style.display = 'block';
        if (svgBlitarBanner) svgBlitarBanner.style.display = 'none';
        if (svgPujonArea) svgPujonArea.style.display = 'block';
        if (svgPujonLine) svgPujonLine.style.display = 'block';
        if (svgBlitarArea) svgBlitarArea.style.display = 'none';
        if (svgBlitarLine) svgBlitarLine.style.display = 'none';
        if (svgPeak) { svgPeak.innerText = 'Puncak: 1.180 mdpl (Pujon)'; svgPeak.style.color = 'var(--emerald-400)'; svgPeak.style.borderColor = 'rgba(16,185,129,0.2)'; svgPeak.style.background = 'rgba(16,185,129,0.1)'; }
        if (svgDotMalang) svgDotMalang.style.display = 'block';
        if (svgTextMalang) { svgTextMalang.style.display = 'block'; svgTextMalang.textContent = 'Malang (Bypass)'; }
      } else if (planNum === 3) {
        if (indicator) { indicator.innerText = 'Plan 3: Jalur Blitar (Tidur Pulas & Pulih Fisik Dampit)'; indicator.style.color = 'var(--amber-400)'; }
        if (badgeDetail) { badgeDetail.innerText = '🛏️ Tidur Pulas Dampit'; badgeDetail.className = 'badge badge-amber-soft'; }
        if (svgHazardBanner) svgHazardBanner.style.display = 'none';
        if (svgBlitarBanner) svgBlitarBanner.style.display = 'block';
        if (svgPujonArea) svgPujonArea.style.display = 'none';
        if (svgPujonLine) svgPujonLine.style.display = 'none';
        if (svgBlitarArea) svgBlitarArea.style.display = 'block';
        if (svgBlitarLine) svgBlitarLine.style.display = 'block';
        if (svgPeak) { svgPeak.innerText = 'Puncak: 350 mdpl (Karangkates)'; svgPeak.style.color = 'var(--amber-400)'; svgPeak.style.borderColor = 'rgba(245,158,11,0.2)'; svgPeak.style.background = 'rgba(245,158,11,0.1)'; }
        if (svgDotMalang) svgDotMalang.style.display = 'none';
        if (svgTextMalang) svgTextMalang.style.display = 'none';
      } else if (planNum === 4) {
        if (indicator) { indicator.innerText = 'Plan 4: Jalur Blitar (Warkop 24 Jam & Hangout)'; indicator.style.color = '#c084fc'; }
        if (badgeDetail) { badgeDetail.innerText = '☕ Warkop 24h Blitar'; badgeDetail.className = 'badge badge-purple-soft'; }
        if (svgHazardBanner) svgHazardBanner.style.display = 'none';
        if (svgBlitarBanner) svgBlitarBanner.style.display = 'block';
        if (svgPujonArea) svgPujonArea.style.display = 'none';
        if (svgPujonLine) svgPujonLine.style.display = 'none';
        if (svgBlitarArea) svgBlitarArea.style.display = 'block';
        if (svgBlitarLine) svgBlitarLine.style.display = 'block';
        if (svgPeak) { svgPeak.innerText = 'Puncak: 350 mdpl (Karangkates)'; svgPeak.style.color = '#c084fc'; svgPeak.style.borderColor = 'rgba(168,85,247,0.2)'; svgPeak.style.background = 'rgba(168,85,247,0.1)'; }
        if (svgDotMalang) svgDotMalang.style.display = 'none';
        if (svgTextMalang) svgTextMalang.style.display = 'none';
      }

      if (routeMapInstance && typeof L !== 'undefined') {
        if (planNum === 1 || planNum === 2) {
          if (routePolylines.pujonSeg1) routePolylines.pujonSeg1.setStyle({ opacity: 0.9, weight: 5 });
          if (routePolylines.pujonSeg2) routePolylines.pujonSeg2.setStyle({ opacity: 0.9, weight: 5 });
          if (routePolylines.blitarSeg) routePolylines.blitarSeg.setStyle({ opacity: 0.2, weight: 2 });
        } else {
          if (routePolylines.pujonSeg1) routePolylines.pujonSeg1.setStyle({ opacity: 0.2, weight: 2 });
          if (routePolylines.pujonSeg2) routePolylines.pujonSeg2.setStyle({ opacity: 0.2, weight: 2 });
          if (routePolylines.blitarSeg) routePolylines.blitarSeg.setStyle({ opacity: 0.95, weight: 5 });
        }
      }
    }

    
    function focusDestination(destKey) {
      const dest = DESTINATIONS_DATA[destKey];
      if (!dest) return;
      if (routeMapInstance && typeof L !== 'undefined') {
        routeMapInstance.flyTo(dest.latLng, 11, { animate: true, duration: 1.0 });
        if (destMarkers[destKey]) {
          destMarkers[destKey].openPopup();
        }
      }
    }
    window.focusDestination = focusDestination;

    function focusRestStop(restKey) {
      const rest = REST_STOPS_DATA[restKey];
      if (!rest) return;
      if (routeMapInstance && typeof L !== 'undefined') {
        routeMapInstance.flyTo(rest.latLng, 12, { animate: true, duration: 1.0 });
        if (restMarkers[restKey]) {
          restMarkers[restKey].openPopup();
        }
      }
    }
    window.focusRestStop = focusRestStop;


    function focusWaypoint(wpKey) {
      const wp = WAYPOINTS_DATA[wpKey];
      if (!wp) return;
      if (routeMapInstance && typeof L !== 'undefined') {
        routeMapInstance.flyTo(wp.latLng, 12, { animate: true, duration: 1.0 });
        if (mapMarkers[wpKey]) {
          mapMarkers[wpKey].openPopup();
        }
      }
    }

    // =========================================================================
    // 2. TIMELINE COLLAPSIBLE TOGGLE & PLAN SWITCHING (REQUIREMENT R1 & R3)
    // =========================================================================
    let isTimelineExpanded = false;

    function toggleTimelineDetails() {
      const collapsible = document.getElementById('timelineCollapsibleSection');
      const btn = document.getElementById('btnToggleTimeline');
      const label = document.getElementById('timelineToggleLabel');
      const chevron = document.getElementById('timelineToggleChevron');
      if (!collapsible || !btn) return;

      isTimelineExpanded = !isTimelineExpanded;
      if (isTimelineExpanded) {
        collapsible.style.display = 'block';
        btn.setAttribute('aria-expanded', 'true');
        if (label) label.innerText = '🔼 Tutup Rincian Itinerary Jam per Jam';
        if (chevron) chevron.style.transform = 'rotate(180deg)';
      } else {
        collapsible.style.display = 'none';
        btn.setAttribute('aria-expanded', 'false');
        if (label) label.innerText = '🔍 Lihat Rincian Itinerary Jam per Jam';
        if (chevron) chevron.style.transform = 'rotate(0deg)';
      }
    }

    function switchPlan(planNum) {
      planNum = parseInt(planNum, 10);
      if (isNaN(planNum) || planNum < 1 || planNum > 4) return;
      try {
        const plans = [
          { num: 1, color: 'var(--sky-400)', bgRgb: '14, 165, 233' },
          { num: 2, color: 'var(--emerald-400)', bgRgb: '16, 185, 129' },
          { num: 3, color: 'var(--amber-400)', bgRgb: '245, 158, 11' },
          { num: 4, color: '#c084fc', bgRgb: '168, 85, 247' }
        ];

        plans.forEach(p => {
          const tab = document.getElementById(`tabPlan${p.num}`);
          const info = document.getElementById(`infoPlan${p.num}`);
          const tl = document.getElementById(`timelinePlan${p.num}`);

          if (tab) {
            if (p.num === planNum) {
              tab.classList.add('active');
              tab.style.background = `rgba(${p.bgRgb}, 0.2)`;
              tab.style.borderColor = p.color;
              tab.style.color = p.color;
            } else {
              tab.classList.remove('active');
              tab.style.background = 'rgba(255, 255, 255, 0.05)';
              tab.style.borderColor = 'var(--border-subtle)';
              tab.style.color = 'var(--text-secondary)';
            }
          }

          if (info) {
            if (p.num === planNum) {
              info.classList.add('active');
              info.style.display = 'flex';
            } else {
              info.classList.remove('active');
              info.style.display = 'none';
            }
          }

          if (tl) {
            tl.style.display = (p.num === planNum) ? 'flex' : 'none';
          }
        });

        updateMapVisualPlan(planNum);

        if (typeof setCalcPlan === 'function') {
          setCalcPlan(planNum, false);
        }
      } catch (e) {
        console.error("Error in switchPlan:", e);
      }
    }

    function toggleAccordion(btn) {
      if (!btn) return;
      const content = btn.nextElementSibling;
      if (!content) return;
      btn.classList.toggle('active');
      content.classList.toggle('show');
    }

    // =========================================================================
    // 3. DYNAMIC COST CALCULATOR ENGINE (REQUIREMENT R3)
    // =========================================================================
    const destMeta = {
      'A': {
        name: 'Opsi A: Tumpak Sewu + Goa Tetes (Gua Karst)',
        ticketName: 'Tiket Terpadu (Termasuk Goa Tetes)',
        ticketUnit: 0,
        mckDestUnit: 0,
        wisataPax: 29000,
        wisataPaxRange: 'Rp 29.000 – Rp 31.000',
        wisataGroup: 116000,
        wisataGroupRange: 'Rp 116.000 – Rp 124.000'
      },
      'T': {
        name: 'Opsi F: Tumpak Sewu + Teras Semeru Sumberurip',
        ticketName: 'Tiket Masuk Teras Semeru',
        ticketUnit: 5000,
        mckDestUnit: 2500,
        wisataPax: 36500,
        wisataPaxRange: 'Rp 36.500',
        wisataGroup: 146000,
        wisataGroupRange: 'Rp 146.000'
      },
      'D': {
        name: 'Opsi D: Tumpak Sewu + Panorama Kapas Biru',
        ticketName: 'Tiket Panorama Kapas Biru',
        ticketUnit: 10000,
        mckDestUnit: 2500,
        wisataPax: 41500,
        wisataPaxRange: 'Rp 41.500',
        wisataGroup: 166000,
        wisataGroupRange: 'Rp 166.000'
      },
      'B': {
        name: 'Opsi B: Tumpak Sewu + Dasar Kapas Biru / Bromo Sunrise',
        ticketName: 'Tiket Dasar Kapas Biru / Bromo',
        ticketUnit: 10000,
        mckDestUnit: 4000,
        wisataPax: 43000,
        wisataPaxRange: 'Rp 43.000',
        wisataGroup: 172000,
        wisataGroupRange: 'Rp 172.000'
      },
      'S': {
        name: 'Alternatif: Tumpak Sewu + Sarkawi Kali Kebo / Pantai',
        ticketName: 'Tiket Sarkawi / Pantai Selatan',
        ticketUnit: 10000,
        mckDestUnit: 0,
        wisataPax: 27500,
        wisataPaxRange: 'Rp 25.000 – Rp 27.500',
        wisataGroup: 110000,
        wisataGroupRange: 'Rp 100.000 – Rp 110.000'
      }
    };

    let calcState = {
      plan: 2,
      dest: 'A',
      mode: 'pax'
    };

    function setCalcPlan(planNum, triggerSwitch = true) {
      calcState.plan = planNum;
      updateCalcPlanUI(planNum);
      updateDynamicCalculator();
      if (triggerSwitch && typeof switchPlan === 'function') {
        switchPlan(planNum);
      }
    }

    function updateCalcPlanUI(planNum) {
      ['calcPlanBtn1', 'calcPlanBtn2', 'calcPlanBtn3', 'calcPlanBtn4'].forEach((btnId, idx) => {
        const btn = document.getElementById(btnId);
        if (btn) {
          if ((idx + 1) === planNum) {
            btn.classList.add('active');
          } else {
            btn.classList.remove('active');
          }
        }
      });
    }

    function setCalcDest(destCode) {
      calcState.dest = destCode;
      ['destBtnA', 'destBtnD', 'destBtnB', 'destBtnS'].forEach(btnId => {
        const btn = document.getElementById(btnId);
        if (btn) {
          if (btnId === `destBtn${destCode}`) {
            btn.classList.add('active');
          } else {
            btn.classList.remove('active');
          }
        }
      });
      updateDynamicCalculator();
    }

    function setCostMode(mode) {
      calcState.mode = mode;
      const btnPax = document.getElementById('btnPerPerson');
      const btnGrp = document.getElementById('btnTotalGroup');
      if (btnPax && btnGrp) {
        if (mode === 'pax') {
          btnPax.classList.add('active');
          btnGrp.classList.remove('active');
        } else {
          btnGrp.classList.add('active');
          btnPax.classList.remove('active');
        }
      }
      updateDynamicCalculator();
    }

    function updateDynamicCalculator() {
      const isGroup = (calcState.mode === 'group');
      const mult = isGroup ? 4 : 1;
      const dest = destMeta[calcState.dest] || destMeta['A'];

      const chkFuel = document.getElementById('chkIncludeFuel');
      const chkMeals = document.getElementById('chkIncludeMeals');
      const incFuel = chkFuel ? chkFuel.checked : true;
      const incMeals = chkMeals ? chkMeals.checked : true;

      // Base Tourism Cost
      const subtotalWisata = isGroup ? dest.wisataGroup : dest.wisataPax;

      // Fuel cost: Plan 3 & 4 (158 km) = Rp 20.000/pax, Plan 1 & 2 (180 km) = Rp 25.000/pax
      const fuelUnitRate = (calcState.plan === 3 || calcState.plan === 4) ? 20000 : 25000;
      const fuelCost = incFuel ? (fuelUnitRate * mult) : 0;
      const mealCost = incMeals ? (65000 * mult) : 0;

      const grandTotal = subtotalWisata + fuelCost + mealCost;

      // Update Summary Cards
      const sumWisata = document.getElementById('summaryWisataVal');
      const sumBbm = document.getElementById('summaryBbmVal');
      const sumMakan = document.getElementById('summaryMakanVal');
      const grandTotalEl = document.getElementById('calcGrandTotalVal');
      const resultLabel = document.getElementById('calcResultLabel');
      const statusBadge = document.getElementById('calcStatusBadge');

      if (sumWisata) sumWisata.innerText = `Rp ${subtotalWisata.toLocaleString('id-ID')}`;
      if (sumBbm) sumBbm.innerText = incFuel ? `Rp ${fuelCost.toLocaleString('id-ID')}` : 'Rp 0 (Excluded)';
      if (sumMakan) sumMakan.innerText = incMeals ? `Rp ${mealCost.toLocaleString('id-ID')}` : 'Rp 0 (Excluded)';
      if (grandTotalEl) grandTotalEl.innerText = `Rp ${grandTotal.toLocaleString('id-ID')}`;

      if (resultLabel) {
        resultLabel.innerText = `Plan ${calcState.plan} + Opsi ${calcState.dest} (${isGroup ? 'Total Rombongan / 4 Pax' : 'Per Orang / 1 Pax'})`;
      }

      if (statusBadge) {
        if (incFuel && incMeals) {
          statusBadge.innerText = 'Lengkap (All-In)';
          statusBadge.style.color = 'var(--emerald-400)';
        } else if (incFuel || incMeals) {
          statusBadge.innerText = 'Parsial';
          statusBadge.style.color = 'var(--amber-400)';
        } else {
          statusBadge.innerText = 'Wisata Saja';
          statusBadge.style.color = 'var(--sky-400)';
        }
      }

      // Populate Table Rows
      const tbody = document.getElementById('calcTableBody');
      if (tbody) {
        let rowsHtml = `
          <tr>
            <td><strong>Tiket Masuk Tumpak Sewu Terpadu</strong></td>
            <td><span class="badge badge-sky-soft">Wisata Utama</span></td>
            <td>Rp 20.000 / pax</td>
            <td><strong>Rp ${(20000 * mult).toLocaleString('id-ID')}</strong></td>
          </tr>
          <tr>
            <td>Parkir Motor Tumpak Sewu (2 Motor)</td>
            <td><span class="badge badge-tag">Parkir</span></td>
            <td>Rp 2.500 / pax (${isGroup ? 'Rp 10.000 total' : 'proporsional'})</td>
            <td>Rp ${(2500 * mult).toLocaleString('id-ID')}</td>
          </tr>
          <tr>
            <td>Toilet &amp; MCK Bilas Air Bersih</td>
            <td><span class="badge badge-tag">Fasilitas</span></td>
            <td>Rp 4.000 / pax</td>
            <td>Rp ${(4000 * mult).toLocaleString('id-ID')}</td>
          </tr>
          <tr>
            <td><strong>${dest.ticketName}</strong></td>
            <td><span class="badge badge-emerald-soft">Destinasi Kedua</span></td>
            <td>${dest.ticketUnit > 0 ? `Rp ${dest.ticketUnit.toLocaleString('id-ID')} / pax` : '<span style="color:var(--emerald-400);">GRATIS (Rp 0)</span>'}</td>
            <td><strong>Rp ${(dest.ticketUnit * mult).toLocaleString('id-ID')}</strong></td>
          </tr>
        `;

        if (incFuel) {
          rowsHtml += `
            <tr>
              <td><strong>BBM Pertalite (2 Motor, ${calcState.plan >= 3 ? '158 km' : '180 km'})</strong></td>
              <td><span class="badge badge-amber-soft">BBM Touring</span></td>
              <td>Rp ${fuelUnitRate.toLocaleString('id-ID')} / pax</td>
              <td><strong>Rp ${fuelCost.toLocaleString('id-ID')}</strong></td>
            </tr>
          `;
        }

        if (incMeals) {
          rowsHtml += `
            <tr>
              <td><strong>Makan, Minum &amp; Logistik (3x Makan + Kopi)</strong></td>
              <td><span class="badge badge-purple-soft">Konsumsi</span></td>
              <td>Rp 65.000 / pax</td>
              <td><strong>Rp ${mealCost.toLocaleString('id-ID')}</strong></td>
            </tr>
          `;
        }

        rowsHtml += `
          <tr style="background: rgba(14, 165, 233, 0.08); font-weight: 800;">
            <td colspan="3">GRAND TOTAL TERHITUNG (${isGroup ? '4 ORANG' : '1 ORANG'})</td>
            <td style="color: var(--emerald-400); font-size: 1rem;">Rp ${grandTotal.toLocaleString('id-ID')}</td>
          </tr>
        `;
        tbody.innerHTML = rowsHtml;
      }
    }

    // =========================================================================
    // 4. CHECKLIST PERSISTENCE ENGINE
    // =========================================================================
    function toggleCheck(chkId) {
      const chk = document.getElementById(chkId);
      if (chk) {
        chk.checked = !chk.checked;
        saveChecklistState();
      }
    }

    function saveChecklistState() {
      try {
        const state = {};
        for (let i = 1; i <= 15; i++) {
          const el = document.getElementById(`chk${i}`);
          if (el) state[`chk${i}`] = el.checked;
        }
        localStorage.setItem('tumpak_checklist_state', JSON.stringify(state));
      } catch (e) {
        console.warn('localStorage write unavailable:', e);
      }
    }

    function loadChecklistState() {
      try {
        const saved = localStorage.getItem('tumpak_checklist_state');
        if (saved) {
          const state = JSON.parse(saved);
          for (const [k, val] of Object.entries(state)) {
            const el = document.getElementById(k);
            if (el) el.checked = !!val;
          }
        }
      } catch (e) {
        console.warn('localStorage read unavailable:', e);
      }
    }

    // =========================================================================
    // 5. IN-CONTEXT VOTING & REST API ENGINE (REQUIREMENT R2)
    // =========================================================================
    const API_BASE_URL = window.location.origin && window.location.origin.startsWith('http') ? window.location.origin : 'http://127.0.0.1:8000';
    let currentVoterName = '';
    let pendingVoteAction = null;
    let localVotesData = null;

    const MOCK_DEFAULT_VOTES = {
      success: true,
      total_participants: 4,
      participants: ['Budi', 'Siti', 'Agus', 'Dewi'],
      routes: { 'Plan 1': 0, 'Plan 2': 1, 'Plan 3': 1, 'Plan 4': 2 },
      destinations: { 'Goa Tetes': 1, 'Coban Kapas Biru': 2, 'Pantai Selatan Malang': 1, 'Bromo Sunrise': 0 },
      votes_by_user: {
        'Budi': { route: 'Plan 4', destination: 'Coban Kapas Biru', updated_at: '2026-08-26T01:00:00Z' },
        'Siti': { route: 'Plan 4', destination: 'Coban Kapas Biru', updated_at: '2026-08-26T01:05:00Z' },
        'Agus': { route: 'Plan 3', destination: 'Goa Tetes', updated_at: '2026-08-26T01:10:00Z' },
        'Dewi': { route: 'Plan 2', destination: 'Pantai Selatan Malang', updated_at: '2026-08-26T01:15:00Z' }
      }
    };

    function initVotingSystem() {
      // Load saved voter name from localStorage
      try {
        const savedName = localStorage.getItem('tumpak_voter_name');
        if (savedName && savedName.trim()) {
          currentVoterName = savedName.trim();
          updateVoterProfileUI();
        }
      } catch (e) {
        console.warn('localStorage voter name unavailable:', e);
      }

      // Initial vote fetch
      fetchVotes();

      // Poll votes periodically every 5 seconds
      setInterval(fetchVotes, 5000);

      // Check backend health
      checkBackendHealth();
    }

    function updateVoterProfileUI() {
      const displayEl = document.getElementById('currentVoterDisplay');
      const avatarEl = document.getElementById('voterAvatarIcon');
      if (displayEl) {
        if (currentVoterName) {
          displayEl.innerText = `${currentVoterName} (Aktif)`;
          displayEl.style.color = 'var(--emerald-400)';
        } else {
          displayEl.innerText = 'Tamu Ekspedisi (Klik untuk Isi Nama)';
          displayEl.style.color = 'var(--sky-400)';
        }
      }
      if (avatarEl && currentVoterName) {
        avatarEl.innerText = currentVoterName.charAt(0).toUpperCase();
      }
    }

    function switchVoteTab(tab) {
      const routeCard = document.getElementById('voteSummaryCardRoute');
      const destCard = document.getElementById('voteSummaryCardDest');
      const btnRoute = document.getElementById('btnVoteTabRoute');
      const btnDest = document.getElementById('btnVoteTabDest');

      if (tab === 'route') {
        if (routeCard) {
          routeCard.classList.remove('tab-hidden');
          routeCard.style.display = 'flex';
        }
        if (destCard) {
          destCard.classList.add('tab-hidden');
          destCard.style.display = 'none';
        }
        if (btnRoute) {
          btnRoute.classList.add('active');
          btnRoute.setAttribute('aria-selected', 'true');
        }
        if (btnDest) {
          btnDest.classList.remove('active', 'dest-active');
          btnDest.setAttribute('aria-selected', 'false');
        }
      } else if (tab === 'dest') {
        if (routeCard) {
          routeCard.classList.add('tab-hidden');
          routeCard.style.display = 'none';
        }
        if (destCard) {
          destCard.classList.remove('tab-hidden');
          destCard.style.display = 'flex';
        }
        if (btnRoute) {
          btnRoute.classList.remove('active');
          btnRoute.setAttribute('aria-selected', 'false');
        }
        if (btnDest) {
          btnDest.classList.add('active', 'dest-active');
          btnDest.setAttribute('aria-selected', 'true');
        }
      }
    }

    function checkBackendHealth() {
      const statusDot = document.getElementById('serverStatusDot');
      const statusText = document.getElementById('serverStatusText');
      fetch(`${API_BASE_URL}/api/health`, { method: 'GET', mode: 'cors' })
        .then(res => res.json())
        .then(data => {
          if (data && data.status === 'ok') {
            if (statusDot) statusDot.className = 'status-dot';
            if (statusText) statusText.innerText = 'Sinkronisasi Real-time';
          }
        })
        .catch(() => {
          if (statusDot) statusDot.className = 'status-dot offline';
          if (statusText) statusText.innerText = 'Mode Offline (Disimpan Lokal)';
        });
    }

    async function fetchVotes() {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 3000);
        const res = await fetch(`${API_BASE_URL}/api/votes`, {
          method: 'GET',
          mode: 'cors',
          signal: controller.signal
        });
        clearTimeout(timeoutId);

        if (res.ok) {
          const data = await res.json();
          localVotesData = data;
          updateVoteUI(data);
          return;
        }
      } catch (e) {
        // Fallback to offline localStorage
      }

      // Offline Fallback Handler
      try {
        let offlineStore = localStorage.getItem('tumpak_mock_votes');
        if (!offlineStore) {
          offlineStore = JSON.stringify(MOCK_DEFAULT_VOTES);
          localStorage.setItem('tumpak_mock_votes', offlineStore);
        }
        localVotesData = JSON.parse(offlineStore);
        updateVoteUI(localVotesData);
      } catch (e) {
        updateVoteUI(MOCK_DEFAULT_VOTES);
      }
    }

    function promptVoterModal(callback) {
      if (callback) pendingVoteAction = callback;
      const modal = document.getElementById('voteNicknameModal');
      const input = document.getElementById('voterNameInput');
      const err = document.getElementById('voterNameError');
      if (input) input.value = currentVoterName || '';
      if (err) err.innerText = '';
      if (modal) modal.style.display = 'flex';
      if (input) input.focus();
    }

    function closeVoterModal() {
      const modal = document.getElementById('voteNicknameModal');
      if (modal) modal.style.display = 'none';
      pendingVoteAction = null;
    }

    function saveVoterName() {
      const input = document.getElementById('voterNameInput');
      const err = document.getElementById('voterNameError');
      const val = input ? input.value.trim() : '';

      if (!val) {
        if (err) err.innerText = 'Nama pemilih tidak boleh kosong.';
        return;
      }
      if (val.length > 50) {
        if (err) err.innerText = 'Nama maksimal 50 karakter.';
        return;
      }

      currentVoterName = val;
      try {
        localStorage.setItem('tumpak_voter_name', currentVoterName);
      } catch (e) {
        console.warn('localStorage write failed:', e);
      }

      updateVoterProfileUI();
      closeVoterModal();

      if (typeof pendingVoteAction === 'function') {
        const action = pendingVoteAction;
        pendingVoteAction = null;
        action();
      } else {
        fetchVotes();
      }
    }

    async function castVote(category, choice, event) {
      if (event) {
        event.stopPropagation();
        event.preventDefault();
      }

      if (!currentVoterName) {
        promptVoterModal(() => castVote(category, choice, null));
        return;
      }

      // Optimistic UI feedback
      const payload = {
        voter_name: currentVoterName,
        category: category,
        choice: choice
      };

      try {
        const res = await fetch(`${API_BASE_URL}/api/vote`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
          mode: 'cors'
        });

        if (res.ok) {
          const data = await res.json();
          fetchVotes();
          return;
        }
      } catch (e) {
        // Fallback offline vote recording in localStorage
      }

      // Offline Vote Update Logic
      try {
        let offlineStore = localStorage.getItem('tumpak_mock_votes');
        let voteState = offlineStore ? JSON.parse(offlineStore) : JSON.parse(JSON.stringify(MOCK_DEFAULT_VOTES));

        if (!voteState.votes_by_user) voteState.votes_by_user = {};
        if (!voteState.votes_by_user[currentVoterName]) {
          voteState.votes_by_user[currentVoterName] = {};
        }

        const oldChoice = voteState.votes_by_user[currentVoterName][category];
        voteState.votes_by_user[currentVoterName][category] = choice;
        voteState.votes_by_user[currentVoterName].updated_at = new Date().toISOString();

        // Recount tallies
        const catKey = category === 'route' ? 'routes' : 'destinations';
        if (oldChoice && voteState[catKey][oldChoice] !== undefined && voteState[catKey][oldChoice] > 0) {
          voteState[catKey][oldChoice]--;
        }
        if (voteState[catKey][choice] !== undefined) {
          voteState[catKey][choice]++;
        } else {
          voteState[catKey][choice] = 1;
        }

        const pSet = new Set(Object.keys(voteState.votes_by_user));
        voteState.total_participants = pSet.size;
        voteState.participants = Array.from(pSet);

        localStorage.setItem('tumpak_mock_votes', JSON.stringify(voteState));
        localVotesData = voteState;
        updateVoteUI(voteState);
      } catch (e) {
        console.warn('Offline vote update error:', e);
      }
    }

    function updateVoteUI(data) {
      if (!data) return;

      const routes = data.routes || { 'Plan 1': 0, 'Plan 2': 0, 'Plan 3': 0, 'Plan 4': 0 };
      const dests = data.destinations || { 'Goa Tetes': 0, 'Coban Kapas Biru': 0, 'Pantai Selatan Malang': 0, 'Bromo Sunrise': 0 };
      const userVotes = (currentVoterName && data.votes_by_user && data.votes_by_user[currentVoterName]) ? data.votes_by_user[currentVoterName] : {};

      const totalRouteVotes = Object.values(routes).reduce((a, b) => a + b, 0);
      const totalDestVotes = Object.values(dests).reduce((a, b) => a + b, 0);

      // 1. Update Route Plan Cards (Buttons & In-Card Tally)
      const routeConfigs = [
        { plan: 'Plan 1', key: 'Plan1', count: routes['Plan 1'] || 0 },
        { plan: 'Plan 2', key: 'Plan2', count: routes['Plan 2'] || 0 },
        { plan: 'Plan 3', key: 'Plan3', count: routes['Plan 3'] || 0 },
        { plan: 'Plan 4', key: 'Plan4', count: routes['Plan 4'] || 0 }
      ];

      routeConfigs.forEach(rc => {
        const pct = totalRouteVotes > 0 ? Math.round((rc.count / totalRouteVotes) * 100) : 0;
        const btn = document.querySelector(`.btn-vote-route[data-plan="${rc.plan}"]`);
        const isSelected = userVotes.route === rc.plan;

        if (btn) {
          if (isSelected) {
            btn.classList.add('has-voted');
            btn.innerHTML = '✅ Pilihan Anda (Voted)';
          } else {
            btn.classList.remove('has-voted');
            btn.innerHTML = '🗳️ Vote Rute Ini';
          }
        }

        const countLbl = document.getElementById(`voteCountLabel-route-${rc.key}`);
        const statusBdg = document.getElementById(`voteStatusBadge-route-${rc.key}`);
        const fillBar = document.getElementById(`voteProgressFill-route-${rc.key}`);

        if (countLbl) countLbl.innerText = `${rc.count} suara (${pct}%)`;
        if (statusBdg) {
          if (isSelected) {
            statusBdg.innerText = '★ Pilihan Anda';
            statusBdg.style.color = 'var(--emerald-400)';
          } else if (rc.count > 0) {
            statusBdg.innerText = `${rc.count} orang memilih`;
            statusBdg.style.color = 'var(--text-muted)';
          } else {
            statusBdg.innerText = 'Belum ada suara';
            statusBdg.style.color = 'var(--text-muted)';
          }
        }
        if (fillBar) fillBar.style.width = `${pct}%`;

        // Update Live Summary Bar
        const sumPct = document.getElementById(`summaryPct-route-${rc.key}`);
        const sumFill = document.getElementById(`summaryFill-route-${rc.key}`);
        const sumVoters = document.getElementById(`summaryVoters-route-${rc.key}`);

        if (sumPct) sumPct.innerText = `${pct}% (${rc.count} suara)`;
        if (sumFill) sumFill.style.width = `${pct}%`;

        if (sumVoters && data.votes_by_user) {
          const votersForThis = Object.entries(data.votes_by_user)
            .filter(([_, v]) => v && v.route === rc.plan)
            .map(([u, _]) => u);
          sumVoters.innerHTML = votersForThis.map(u => `<span class="voter-chip">${u}</span>`).join('');
        }
      });

      // 2. Update Destination Cards (Buttons & In-Card Tally)
      const destConfigs = [
        { dest: 'Goa Tetes', key: 'GoaTetes', count: dests['Goa Tetes'] || 0 },
        { dest: 'Coban Kapas Biru', key: 'CobanKapasBiru', summaryKey: 'KapasBiru', count: dests['Coban Kapas Biru'] || 0 },
        { dest: 'Kabut Pelangi', key: 'KabutPelangi', summaryKey: 'KabutPelangi', count: dests['Kabut Pelangi'] || 0 },
        { dest: 'Pantai Selatan Malang', key: 'PantaiSelatanMalang', summaryKey: 'PantaiSelatan', count: dests['Pantai Selatan Malang'] || 0 },
        { dest: 'Bromo Sunrise', key: 'BromoSunrise', summaryKey: 'Bromo', count: dests['Bromo Sunrise'] || 0 },
        { dest: 'Teras Semeru', key: 'TerasSemeru', summaryKey: 'TerasSemeru', count: dests['Teras Semeru'] || 0 }
      ];

      destConfigs.forEach(dc => {
        const pct = totalDestVotes > 0 ? Math.round((dc.count / totalDestVotes) * 100) : 0;
        const btn = document.querySelector(`.btn-vote-dest[data-dest="${dc.dest}"]`);
        const isSelected = userVotes.destination === dc.dest;

        if (btn) {
          if (isSelected) {
            btn.classList.add('has-voted');
            btn.innerHTML = '✅ Pilihan Anda (Voted)';
          } else {
            btn.classList.remove('has-voted');
            btn.innerHTML = '🗳️ Vote Destinasi Ini';
          }
        }

        const countLbl = document.getElementById(`voteCountLabel-dest-${dc.key}`);
        const statusBdg = document.getElementById(`voteStatusBadge-dest-${dc.key}`);
        const fillBar = document.getElementById(`voteProgressFill-dest-${dc.key}`);

        if (countLbl) countLbl.innerText = `${dc.count} suara (${pct}%)`;
        if (statusBdg) {
          if (isSelected) {
            statusBdg.innerText = '★ Pilihan Anda';
            statusBdg.style.color = 'var(--emerald-400)';
          } else if (dc.count > 0) {
            statusBdg.innerText = `${dc.count} orang memilih`;
            statusBdg.style.color = 'var(--text-muted)';
          } else {
            statusBdg.innerText = 'Belum ada suara';
            statusBdg.style.color = 'var(--text-muted)';
          }
        }
        if (fillBar) fillBar.style.width = `${pct}%`;

        // Update Live Summary Bar
        const sKey = dc.summaryKey || dc.key;
        const sumPct = document.getElementById(`summaryPct-dest-${sKey}`);
        const sumFill = document.getElementById(`summaryFill-dest-${sKey}`);
        const sumVoters = document.getElementById(`summaryVoters-dest-${sKey}`);

        if (sumPct) sumPct.innerText = `${pct}% (${dc.count} suara)`;
        if (sumFill) sumFill.style.width = `${pct}%`;

        if (sumVoters && data.votes_by_user) {
          const votersForThis = Object.entries(data.votes_by_user)
            .filter(([_, v]) => v && v.destination === dc.dest)
            .map(([u, _]) => u);
          sumVoters.innerHTML = votersForThis.map(u => `<span class="voter-chip">${u}</span>`).join('');
        }
      });

      // Update Summary Header Counts & Tab Badges
      const rTotalLbl = document.getElementById('routeVoteTotalLabel');
      const dTotalLbl = document.getElementById('destVoteTotalLabel');
      if (rTotalLbl) rTotalLbl.innerText = `${totalRouteVotes} Suara Masuk`;
      if (dTotalLbl) dTotalLbl.innerText = `${totalDestVotes} Suara Masuk`;

      const rBadgeMini = document.getElementById('routeVoteBadgeMini');
      const dBadgeMini = document.getElementById('destVoteBadgeMini');
      if (rBadgeMini) rBadgeMini.innerText = `${totalRouteVotes}`;
      if (dBadgeMini) dBadgeMini.innerText = `${totalDestVotes}`;
    }

    // =========================================================================
    // 5.5 DESTINATIONS CAROUSEL NAVIGATION (MOBILE-FIRST)
    // =========================================================================
    function scrollToDestCard(index) {
      const grid = document.getElementById('destinationsGrid');
      if (!grid) return;
      const cards = grid.querySelectorAll('.dest-card');
      if (index >= 0 && index < cards.length) {
        cards[index].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
        updateDestPillActive(index);
      }
    }

    function slideDestCard(direction) {
      const grid = document.getElementById('destinationsGrid');
      if (!grid) return;
      const cards = grid.querySelectorAll('.dest-card');
      const curIdx = parseInt(document.getElementById('destCurrentIndex')?.innerText || '1') - 1;
      let nextIdx = curIdx + direction;
      if (nextIdx < 0) nextIdx = 0;
      if (nextIdx >= cards.length) nextIdx = cards.length - 1;
      scrollToDestCard(nextIdx);
    }

    function updateDestPillActive(index) {
      const nav = document.getElementById('destCarouselNav');
      const indicator = document.getElementById('destCurrentIndex');
      if (indicator) indicator.innerText = (index + 1).toString();
      if (!nav) return;
      const pills = nav.querySelectorAll('.dest-pill-btn');
      pills.forEach((p, i) => {
        if (i === index) {
          p.classList.add('active');
          p.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
        } else {
          p.classList.remove('active');
        }
      });
    }

    function initDestinationsCarousel() {
      const grid = document.getElementById('destinationsGrid');
      if (!grid) return;

      let scrollTimeout;
      grid.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
          const cards = grid.querySelectorAll('.dest-card');
          if (!cards || cards.length === 0) return;
          const gridCenter = grid.scrollLeft + grid.offsetWidth / 2;
          let closestIndex = 0;
          let minDistance = Infinity;

          cards.forEach((card, i) => {
            const cardCenter = card.offsetLeft + card.offsetWidth / 2;
            const distance = Math.abs(gridCenter - cardCenter);
            if (distance < minDistance) {
              minDistance = distance;
              closestIndex = i;
            }
          });

          updateDestPillActive(closestIndex);
        }, 80);
      }, { passive: true });
    }

    // =========================================================================
    // 5.6 MOBILE FLOATING NAV COLLAPSIBLE CONTROLLER
    // =========================================================================
    function toggleMobileNav() {
      const nav = document.getElementById('stickyNavbar');
      const toggleBtn = document.getElementById('mobileNavToggle');
      if (!nav) return;
      const isOpen = nav.classList.toggle('open');
      if (toggleBtn) {
        toggleBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      }
    }

    function closeMobileNav() {
      const nav = document.getElementById('stickyNavbar');
      const toggleBtn = document.getElementById('mobileNavToggle');
      if (nav && nav.classList.contains('open')) {
        nav.classList.remove('open');
        if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'false');
      }
    }

    // Auto-close mobile nav when tapping outside
    document.addEventListener('click', (e) => {
      const nav = document.getElementById('stickyNavbar');
      if (nav && nav.classList.contains('open') && !nav.contains(e.target)) {
        closeMobileNav();
      }
    });

    // =========================================================================
    // 6. WINDOW INITIALIZATION
    // =========================================================================
    window.addEventListener('DOMContentLoaded', () => {
      initRouteMap();
      switchPlan(2);
      loadChecklistState();
      updateDynamicCalculator();
      initVotingSystem();
      switchVoteTab('route');
      initDestinationsCarousel();
    });
  