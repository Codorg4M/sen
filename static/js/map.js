/**
 * RideShare - Leaflet & OpenStreetMap Integration (Section 23)
 * Non-blocking, zero-cost, privacy-friendly map visualization.
 */

function initRideShareMap(containerId = 'map-container', pickupCoords = [28.6139, 77.2090], destCoords = [28.7041, 77.1025]) {
    const mapElement = document.getElementById(containerId);
    if (!mapElement) return;

    if (typeof L === 'undefined') {
        mapElement.innerHTML = `
            <div style="padding: 2rem; text-align: center; background: #f8fafc; color: #64748b; border: 1px dashed #cbd5e1; border-radius: 8px;">
                <p>🗺️ Map preview is running in offline simulation mode.</p>
                <small>Leaflet & OpenStreetMap will render when internet connection is available.</small>
            </div>
        `;
        return;
    }

    try {
        const map = L.map(containerId).setView(pickupCoords, 12);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Marker for Pickup
        const pickupMarker = L.marker(pickupCoords).addTo(map)
            .bindPopup("<b>Pickup Location</b>").openPopup();

        // Marker for Destination
        const destMarker = L.marker(destCoords).addTo(map)
            .bindPopup("<b>Destination</b>");

        // Route line connecting the two points
        const latlngs = [pickupCoords, destCoords];
        const polyline = L.polyline(latlngs, { color: '#1e3a8a', weight: 4, opacity: 0.8, dashArray: '8, 8' }).addTo(map);
        
        map.fitBounds(polyline.getBounds(), { padding: [50, 50] });
    } catch (e) {
        console.warn("Leaflet initialization fallback:", e);
    }
}
