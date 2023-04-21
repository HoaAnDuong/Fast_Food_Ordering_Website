const lat = document.getElementById("lat")
const lng = document.getElementById("lng")
const address = document.getElementById("address")
const country = document.getElementById("country")
const region = document.getElementById("region")
const subregion_1 = document.getElementById("subregion_1")
const subregion_2 = document.getElementById("subregion_2")
const num_of_store = document.getElementById("num_of_store")

const apiKey = "AAPK5a1319c4648247188e709e0176c0a073pqXTy5i1h6UW8b2prBtWB59DSR7OsFx-2yGG0CpcSTeKcf8ZkrkMbg6EYLZ0p3VW";

const authentication = arcgisRest.ApiKeyManager.fromKey(apiKey);

var map = L.map('map').setView([lat.value,lng.value], 15);

//roadmap tilelayer:'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'

L.tileLayer('http://mt1.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}', {
  maxZoom: 22,
  attribution: 'Google'
}).addTo(map);


var locationTab = document.getElementById('location');
var observer1 = new MutationObserver(function(){
  map.invalidateSize();
});
observer1.observe(locationTab, {attributes: true});

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

var destination_marker = L.marker([lat.value,lng.value],{icon: greenIcon})
destination_marker.addTo(map)

var lngLatString = `${Math.round(lng.value * 100000) / 100000}, ${Math.round(lat.value * 100000) / 100000}`;
destination_marker.bindPopup(`<b>${lngLatString}</b><p>${address.value}</p>`);
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

    distance = Math.pow(Math.pow(lat.value-store_lat.value,2.) + Math.pow(lng.value-store_lng.value,2.),0.5) * 111.139
    antpaths.push(L.layerGroup());

    let polyline = L.polyline.antPath([[lat.value,lng.value],[store_lat.value,store_lng.value]], {
      "delay": 400,
      "dashArray": [
        10,
        20
      ],
      "weight": 5,
      "color": distance > 8 ? "red" : (distance > 4 ? "orange" : "green"),
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

function reverseGeocoderHandler(error,result){
    if(error){
    }else{
        console.log(result);

        address.value = result.address.LongLabel
        country.value = result.address.CntryName
        region.value = result.address.Region
        subregion_1.value = result.address.District != "" ? result.address.District : result.address.City
        subregion_2.value = result.address.Neighborhood

        lngLatString = `${Math.round(result.latlng.lng * 100000) / 100000}, ${Math.round(result.latlng.lat * 100000) / 100000}`;
        destination_marker.bindPopup(`<b>${lngLatString}</b><p>${result.address.LongLabel}</p>`);
        destination_marker.openPopup();
    }
}

function onMapClickHandler(e){
    var latlng = e.latlng;
    destination_marker.setLatLng(latlng)
    lat.value = latlng.lat;
    lng.value = latlng.lng;
    var esri_reverseGeocoder = L.esri.Geocoding.reverseGeocode({apikey: apiKey}).latlng(latlng);
    esri_reverseGeocoder.run(reverseGeocoderHandler);
    for (let i=0;i < num_of_store.value;i++){
        store_lat = document.getElementById(`store_${i}_lat`)
        store_lng = document.getElementById(`store_${i}_lng`)

        antpaths[i].clearLayers()

        distance = Math.pow(Math.pow(lat.value-store_lat.value,2.) + Math.pow(lng.value-store_lng.value,2.),0.5) * 111.319
        let polyline = L.polyline.antPath([[lat.value,lng.value],[store_lat.value,store_lng.value]], {
          "delay": 400,
          "dashArray": [
            10,
            20
          ],
          "weight": 5,
          "color": distance > 8 ? "red" : (distance > 4 ? "orange" : "#15ff00"),
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
}

map.on("click",onMapClickHandler);

