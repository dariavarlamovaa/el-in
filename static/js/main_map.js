// getting latitude and longitude of the place
var myIcon = L.icon({
    iconUrl: '../../../static/places/images/place.svg', iconSize: [29, 24]
})

// map init
var map = L.map('map', {attributionControl: false}).setView([65.309345, 26.278694], 5);

// osm layer
const openStreetMap = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});

openStreetMap.addTo(map);

// Carto_DB layer
const CartoDB_Dark_Matter = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19
});

CartoDB_Dark_Matter.addTo(map);

const OpenStreetMap_Mapnik = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});

const baseLayers = {
    'CartoDB': CartoDB_Dark_Matter, 'Open Street Map': OpenStreetMap_Mapnik,
}

// base layers
L.control.layers(baseLayers, {}, {}).addTo(map)
L.control.scale().addTo(map)

// places and markers in the groups
let places = JSON.parse(document.getElementById("places_json").textContent)
var markers = new L.MarkerClusterGroup();
places.forEach(place => {
    let place_marker = L.marker([place.latitude, place.longitude], {'icon': myIcon})
    let context = `<a class="popup-link" href="/places/place/${place.id}">
                        <img class="popup-image" src="${place.image}"
                        alt="${place.name}"><p class="popup-name">${place.name}</p>
                        <p class="popup-city">${place.city}</p></a>`
    place_marker.bindPopup(context)
    markers.addLayer(place_marker);
})
map.addLayer(markers);

// filter function

let filteredMarkers = new L.MarkerClusterGroup();
function filterPlaces(query) {
    filteredMarkers.clearLayers();
    places.forEach(place => {
        if (place.name.toLowerCase().includes(query) || place.city.toLowerCase().includes(query)) {
            let place_marker = L.marker([place.latitude, place.longitude], {icon: myIcon});
            let context = `<a class="popup-link" href="/places/place/${place.id}">
                            <img class="popup-image" src="${place.image}"
                            alt="${place.name}"><p class="popup-name">${place.name}</p>
                            <p class="popup-city">${place.city}</p></a>`;
            place_marker.bindPopup(context);
            filteredMarkers.addLayer(place_marker);
        }
    });
    map.addLayer(filteredMarkers);
}

// event listener for search input
document.getElementById("search-input").addEventListener("input", function () {
    let query = this.value.toLowerCase();
    map.removeLayer(markers);
    filterPlaces(query);
    if (!query) {
        map.removeLayer(filteredMarkers);
        map.addLayer(markers);
    }
});