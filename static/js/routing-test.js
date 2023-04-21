var coord_2 = [16.07387,108.14975]
var coord = [16.13613,108.11676]


var map = L.map('map').setView(coord, 15);
//roadmap tilelayer:'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'

L.tileLayer('http://mt1.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}', {
  maxZoom: 22,
  attribution: 'Google'
}).addTo(map);

const lat = document.getElementById("lat")
const lng = document.getElementById("lng")
const address = document.getElementById("address")
const choices = document.getElementById("choices")
const route_button = document.getElementById("route-button")
const distance = document.getElementById("distance")
const directions = document.getElementById("directions")

lat.value = coord[0]
lng.value = coord[1]

var option_1 = document.createElement("option");
option_1.text = "start";

var option_2 = document.createElement("option");
option_2.text = "end";

var default_option = document.createElement("option");
default_option.text = "none";

choices.add(default_option);
choices.add(option_1);
choices.add(option_2);


var marker_1 = L.marker(coord)
var marker_2 = L.marker(coord_2)

marker_1.addTo(map)
marker_2.addTo(map)

const routeLines = L.layerGroup().addTo(map);

var current_marker = null;

const apiKey = "AAPK5a1319c4648247188e709e0176c0a073pqXTy5i1h6UW8b2prBtWB59DSR7OsFx-2yGG0CpcSTeKcf8ZkrkMbg6EYLZ0p3VW";

const authentication = arcgisRest.ApiKeyManager.fromKey(apiKey);

//Geocoder

function reverseGeocodeHandler(error,result){
    if(error){
    }else{
        console.log(result);
        address.innerHTML = result.address.LongLabel
        const lngLatString = `${Math.round(result.latlng.lng * 100000) / 100000}, ${Math.round(result.latlng.lat * 100000) / 100000}`;
        current_marker.bindPopup(`<b>${lngLatString}</b><p>${result.address.LongLabel}</p>`);
        current_marker.openPopup();
    }
}

function onMapClick(e) {
    if(choices.values != "none"){
        if (choices.value === "start") current_marker = marker_1;
        else if (choices.value === "end") current_marker = marker_2;

        var latlng = e.latlng;
        current_marker.setLatLng(latlng)
        lat.value = latlng.lat;
        lng.value = latlng.lng;

        var esri_reverseGeocoder = L.esri.Geocoding.reverseGeocode({apikey: apiKey}).latlng(latlng);
        esri_reverseGeocoder.run(reverseGeocodeHandler);
    }
}

function onEnterKeyPressed(e){
    if(e.key === "Enter"){
        if(choices.values != "none"){
            if (choices.value === "start") current_marker = marker_1;
            else if (choices.value === "end") current_marker = marker_2;

            var latlng = L.latLng(lat.value,lng.value);
            current_marker.setLatLng(latlng)
            lat.value = latlng.lat;
            lng.value = latlng.lng;

            var esri_reverseGeocoder = L.esri.Geocoding.reverseGeocode({apikey: apiKey}).latlng(latlng);
            esri_reverseGeocoder.run(reverseGeocodeHandler);
        }
    }
}

map.on('click', onMapClick);
lat.addEventListener('keypress',onEnterKeyPressed);
lng.addEventListener('keypress',onEnterKeyPressed);

//Routing

function responseHandler(response) {
    console.log(response);
    routeLines.clearLayers();
    L.geoJSON(response.routes.geoJson).addTo(routeLines);

    let features = response.directions[0].features

    const directionsHTML = features.map((f) => f.attributes.text).join("<br/>");
    directions.innerHTML = directionsHTML;
    for (let i = 0;i<features.length;i++) {
        let new_marker = L.marker([features[i].geometry.paths[0][0][1],features[i].geometry.paths[0][0][0]])
        try{
            new_marker.bindPopup(`<b>${features[i].strings[0].string}</b><p>${features[i].attributes.text}</p>`)
        }catch(error) {
        }

        new_marker.addTo(routeLines)
    }
}

function makeRoute(){
    latlng_1 = marker_1.getLatLng()
    latlng_2 = marker_2.getLatLng()
    router = arcgisRest.solveRoute({
            stops: [[latlng_1.lng,latlng_1.lat],[latlng_2.lng,latlng_2.lat]],
            endpoint: "https://route-api.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve",
            authentication
          });
    router.then(responseHandler).catch((error) => {
            console.error(error);
            alert("There was a problem using the route service. See the console for details.");
    });
}
route_button.addEventListener("click",makeRoute)