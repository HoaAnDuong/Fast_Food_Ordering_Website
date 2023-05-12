//Initialize

const num_points = document.getElementById("num_points")
const num_of_stores = document.getElementById("num_of_stores")
const start_lat = document.getElementById("start_lat")
const start_lng = document.getElementById("start_lng")
const destination_lat = document.getElementById("destination_lat")
const destination_lng = document.getElementById("destination_lng")
const destination_address = document.getElementById("destination_address")
const deliverer_lat = document.getElementById("deliverer_lat")
const deliverer_lng = document.getElementById("deliverer_lng")



//Map
var map = L.map('map').setView([destination_lat.value,destination_lng.value], 15);

//roadmap tilelayer:'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'

L.tileLayer('http://mt1.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}', {
  maxZoom: 22,
  attribution: 'Google'
}).addTo(map);

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


var locationTab = document.getElementById('delivery_location');
var observer1 = new MutationObserver(function(){
  map.invalidateSize();
});
observer1.observe(locationTab, {attributes: true});

//Markers

var startIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

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

var delivererIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

stores_latLng = []

start_latLng = L.latLng([start_lat.value,start_lng.value])

var start_marker = L.marker(start_latLng,{icon: startIcon})
start_marker.addTo(map)

var lngLatString = `${Math.round(start_lng.value * 100000) / 100000}, ${Math.round(start_lat.value * 100000) / 100000}`;
start_marker.bindPopup(`<b>${lngLatString}</b><br><b>Vị trí bắt đầu</b>`);
start_marker.openPopup();


destination_latLng = L.latLng([destination_lat.value,destination_lng.value])

var destination_marker = L.marker(destination_latLng,{icon: destinationIcon})
destination_marker.addTo(map)

var destination_circle_marker = L.circle(destination_latLng,{radius:100,color:"#2A81CB"});
    destination_circle_marker.addTo(map);

lngLatString = `${Math.round(destination_lat.value * 100000) / 100000}, ${Math.round(destination_lng.value * 100000) / 100000}`;
destination_marker.bindPopup(`<b>${lngLatString}</b><p>${destination_address.value}</p><br><b>Vị trí giao hàng</b>`);
destination_marker.openPopup();

deliverer_latLng = L.latLng([deliverer_lat.value,deliverer_lng.value])

var deliverer_marker = L.marker(deliverer_latLng,{icon: delivererIcon})
deliverer_marker.addTo(map)

lngLatString = `${Math.round(deliverer_lat.value * 100000) / 100000}, ${Math.round(deliverer_lng.value * 100000) / 100000}`;
deliverer_marker.bindPopup(`<b>${lngLatString}</b><br><b>Vị trí người giao hàng</b>`);
deliverer_marker.openPopup();

for(let i = 0;i<num_points.value;i++){
    let point_lat = document.getElementById(`point_${i}_lat`);
    let point_lng = document.getElementById(`point_${i}_lng`);

    stores_latLng.push(L.latLng([point_lat.value,point_lng.value]))
    var store_marker = L.marker(stores_latLng[i],{icon: storeIcon})
    store_marker.addTo(map)
}

for (let i=0;i < num_of_store.value;i++){
    store_lat = document.getElementById(`store_${i}_lat`);
    store_lng = document.getElementById(`store_${i}_lng`);
    store_address = document.getElementById(`store_${i}_address`);
    store_name = document.getElementById(`store_${i}_name`);
    store_marker = L.marker([store_lat.value,store_lng.value],{icon: storeIcon});
    store_marker.addTo(map);
    lngLatString = `${Math.round(store_lng.value * 100000) / 100000}, ${Math.round(store_lat.value * 100000) / 100000}`;
    store_marker.bindPopup(`<b>${lngLatString}</b><br><b>${store_name.innerHTML}</b><p>${store_address.value}</p>`);
    store_marker.openPopup();
    circle_marker = L.circle([store_lat.value,store_lng.value],{radius:100,color:"#CB8427"});
    circle_marker.addTo(map);
}

const routeLines = L.layerGroup().addTo(map);

function responseHandler(response) {
    console.log(response);
    routeLines.clearLayers();
    let path = [].concat(...response.routes.geoJson.features[0].geometry.coordinates)
    path.forEach((item) => {
        item.reverse();
    })
    console.log(path)
    L.polyline.antPath(path, {
      "delay": 400,
      "dashArray": [
        10,
        20
      ],
      "weight": 5,
      "color": "#0388fc",
      "pulseColor": "#FFFFFF",
      "paused": false,
      "reverse": false,
      "hardwareAccelerated": true
    }).addTo(routeLines);
}


route_latLng = []
//route_latLng.push(start_latLng)
//route_latLng.concat(stores_latLng)
//route_latLng.push(destination_latLng)


route_latLng.push([start_latLng.lng,start_latLng.lat])
for(let i = 0;i<stores_latLng.length;i++){
    route_latLng.push([stores_latLng[i].lng,stores_latLng[i].lat])
}
route_latLng.push([destination_latLng.lng,destination_latLng.lat])

router = arcgisRest.solveRoute({
        stops: route_latLng,
        endpoint: "https://route-api.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve",
        authentication
});
router.then(responseHandler).catch((error) => {
        console.error(error);
        alert("There was a problem using the route service. See the console for details.");
});

router = arcgisRest.solveRoute({
        stops: route_latLng.slice(1,route_latLng.length),
        endpoint: "https://route-api.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve",
        authentication
});
router.then((response) => {
    console.log(response);
}).catch((error) => {
        console.error(error);
        alert("There was a problem using the route service. See the console for details.");
});

async function delivererLocationRefresh(){
    while(true){
        $.ajax({
            type:'GET',
            url:'/current-order/deliverer-location',
            data:
            {
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data){
               let json = $.parseJSON(data);
               console.log(json);
               deliverer_marker.setLatLng([json.deliverer_lat,json.deliverer_lng]);
               deliverer_lat.value = json.deliverer_lat
               deliverer_lng.value = json.deliverer_lng

               lngLatString = `${Math.round(deliverer_lat.value * 100000) / 100000}, ${Math.round(deliverer_lng.value * 100000) / 100000}`;
                deliverer_marker.bindPopup(`<b>${lngLatString}</b><br><b>Vị trí người giao hàng</b>`);
            },
            error: function(data){
               let json = $.parseJSON(data);
               console.log(json);
            }
        });
        await sleep(5000);
    }
}

delivererLocationRefresh();


