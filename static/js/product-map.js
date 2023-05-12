const store_lat = document.getElementById("store_lat")
const store_lng = document.getElementById("store_lng")
const store_address = document.getElementById("store_address")
const store_name = document.getElementById("store_name")

const destination_lat = document.getElementById("destination_lat")
const destination_lng = document.getElementById("destination_lng")
const destination_address = document.getElementById("destination_address")

var map = L.map('product_map').setView([store_lat.value,store_lng.value], 15);

//roadmap tilelayer:'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'

L.tileLayer('http://mt1.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}', {
  maxZoom: 22,
  attribution: 'Google'
}).addTo(map);

var storeIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var destinationIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

store_marker = L.marker([store_lat.value,store_lng.value],{icon: storeIcon})
store_marker.addTo(map)
lngLatString = `${Math.round(store_lng.value * 100000) / 100000}, ${Math.round(store_lat.value * 100000) / 100000}`;
store_marker.bindPopup(`<b>${lngLatString}</b><br><b>${store_name.value}</b><p>${store_address.value}</p>`);
store_marker.openPopup();

if(destination_lat !== null){
    destination_marker = L.marker([destination_lat.value,destination_lng.value],{icon: destinationIcon})
    destination_marker.addTo(map)
    lngLatString = `${Math.round(destination_lng.value * 100000) / 100000}, ${Math.round(destination_lat.value * 100000) / 100000}`;
    destination_marker.bindPopup(`<b>${lngLatString}</b><p>${destination_address.value}</p>`);
    distance = Math.pow(Math.pow(destination_lat.value-store_lat.value,2.) + Math.pow(destination_lng.value-store_lng.value,2.),0.5) * 111.319

    let polyline = L.polyline.antPath([[destination_lat.value,destination_lng.value],[store_lat.value,store_lng.value]], {
      "delay": 400,
      "dashArray": [
        10,
        20
      ],
      "weight": 5,
      "color": distance > 8 ? "red" : (distance > 5 ? "orange" : "green"),
      "pulseColor": "#FFFFFF",
      "paused": false,
      "reverse": false,
      "hardwareAccelerated": true
    })
    polyline.bindPopup(`<b>${Math.round(distance * 1000) / 1000} km</b>`);
    polyline.addTo(map);
}