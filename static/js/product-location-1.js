const destination_lat = document.getElementById("destination_lat")
const destination_lng = document.getElementById("destination_lng")
const destination_address = document.getElementById("destination_address")
const num_of_store = document.getElementById("num_of_store")


var map = L.map('map').setView([destination_lat.value,destination_lng.value], 15);

//roadmap tilelayer:'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'

L.tileLayer('http://mt1.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}', {
  maxZoom: 22,
  attribution: 'Google'
}).addTo(map);

var greenIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var orangeIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

var destination_marker = L.marker([destination_lat.value,destination_lng.value],{icon: greenIcon})
destination_marker.addTo(map)

var lngLatString = `${Math.round(destination_lng.value * 100000) / 100000}, ${Math.round(destination_lat.value * 100000) / 100000}`;
destination_marker.bindPopup(`<b>${lngLatString}</b><p>${destination_address.value}</p>`);
destination_marker.openPopup();

antpaths = []

for (let i=0;i < num_of_store.value;i++){
    store_lat = document.getElementById(`store_${i}_lat`)
    store_lng = document.getElementById(`store_${i}_lng`)
    store_address = document.getElementById(`store_${i}_address`)
    store_name = document.getElementById(`store_${i}_name`)

    store_marker = L.marker([store_lat.value,store_lng.value],{icon: orangeIcon})
    store_marker.addTo(map)
    lngLatString = `${Math.round(store_lng.value * 100000) / 100000}, ${Math.round(store_lat.value * 100000) / 100000}`;
    store_marker.bindPopup(`<b>${lngLatString}</b><br><b>${store_name.innerHTML}</b><p>${store_address.value}</p>`);
    store_marker.openPopup();

    distance = Math.pow(Math.pow(destination_lat.value-store_lat.value,2.) + Math.pow(destination_lng.value-store_lng.value,2.),0.5) * 111.319
    antpaths.push(L.layerGroup());

    let polyline = L.polyline.antPath([[destination_lat.value,destination_lng.value],[store_lat.value,store_lng.value]], {
      "delay": 400,
      "dashArray": [
        10,
        20
      ],
      "weight": 5,
      "color": distance > 10 ? "red" : (distance > 5 ? "orange" : "green"),
      "pulseColor": "#FFFFFF",
      "paused": false,
      "reverse": false,
      "hardwareAccelerated": true
    })
    polyline.bindPopup(`<b>${Math.round(distance * 1000) / 1000} km</b>`);
    polyline.addTo(antpaths[i]);
    antpaths[i].addTo(map);
    polyline.openPopup();
}

