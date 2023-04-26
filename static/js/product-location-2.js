const lat = document.getElementById("lat")
const lng = document.getElementById("lng")
const address = document.getElementById("address")
const country = document.getElementById("country")
const region = document.getElementById("region")
const subregion_1 = document.getElementById("subregion_1")
const subregion_2 = document.getElementById("subregion_2")
const num_of_store = document.getElementById("num_of_store")

const MAX_DISTANCE = 8

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

var destination_marker = L.marker([lat.value,lng.value],{icon: destinationIcon})
destination_marker.addTo(map)

var lngLatString = `${Math.round(lng.value * 100000) / 100000}, ${Math.round(lat.value * 100000) / 100000}`;
destination_marker.bindPopup(`<b>${lngLatString}</b><p>${address.value}</p>`);
destination_marker.openPopup();

antpaths = []

const routeLines = L.layerGroup().addTo(map);

store_marker = []


destination_latlng = L.latLng({lat:lat.value,lng:lng.value});

stores_latlng = [];

function calDistance(point_1,point_2){
    return Math.pow(Math.pow(point_1.lat-point_2.lat,2.) + Math.pow(point_1.lng-point_2.lng,2.),0.5) * 111.319
}

function permute(arr) {
    let result = [];
    if (arr.length === 0) return [];
    if (arr.length === 1) return [arr];
    for (let i = 0; i < arr.length; i++) {
        let current = arr[i];
        let remaining = arr.slice(0, i).concat(arr.slice(i + 1));
        let remainingPermuted = permute(remaining);
        for (let j = 0; j < remainingPermuted.length; j++) {
            let permutedArray = [current].concat(remainingPermuted[j]);
            result.push(permutedArray);
        }
    }
    return result;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


for (let i=0;i < num_of_store.value;i++){
    store_lat = document.getElementById(`store_${i}_lat`)
    store_lng = document.getElementById(`store_${i}_lng`)
    store_address = document.getElementById(`store_${i}_address`)
    store_name = document.getElementById(`store_${i}_name`)

    stores_latlng[i] = L.latLng({lat:store_lat.value,lng:store_lng.value})

    store_marker[i] = L.marker([store_lat.value,store_lng.value],{icon: storeIcon})
    store_marker[i].addTo(map)
    lngLatString = `${Math.round(store_lng.value * 100000) / 100000}, ${Math.round(store_lat.value * 100000) / 100000}`;
    store_marker[i].bindPopup(`<b>${lngLatString}</b><br><b>${store_name.innerHTML}</b><p>${store_address.value}</p>`);
    store_marker[i].openPopup();

    distance = calDistance(destination_latlng,stores_latlng[i])
    antpaths.push(L.layerGroup());

    let polyline = L.polyline.antPath([[lat.value,lng.value],[store_lat.value,store_lng.value]], {
      "delay": 400,
      "dashArray": [
        10,
        20
      ],
      "weight": 5,
      "color": distance > MAX_DISTANCE ? "red" : (distance > MAX_DISTANCE/2 ? "orange" : "green"),
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

stores_list_permutation = permute(stores_latlng)

function routeHandler(response){
    routeLines.clearLayers();
    let path = [].concat(...response.routes.geoJson.features[0].geometry.coordinates)
    path.forEach((item) => {
        item.reverse();
    })
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
    document.getElementById("total_length").value = response.routes.geoJson.features[0].properties.Total_Kilometers
    document.getElementById("total_length_label").innerHTML = `<label>Tổng chiều dài: ${response.routes.geoJson.features[0].properties.Total_Kilometers} km</label>`
}

function shortest_path(){
    let = min_length = Infinity

    min_path = []
    for(let i = 0;i < stores_list_permutation.length;i++){
        total_length = 0
        let chosen_path = [...stores_list_permutation[i]]
        chosen_path.push(destination_latlng)
        for(let j = 0;j < chosen_path.length-1;j++){
            total_length += calDistance(chosen_path[j],chosen_path[j+1]);
        }
        if(total_length < min_length){
            min_path = chosen_path
            min_length = total_length
        }
    }
    for(let i = 0;i < min_path.length; i++){
        min_path[i] = [min_path[i].lng,min_path[i].lat]
    }
    console.log(min_path)
    router = arcgisRest.solveRoute({
            stops: min_path,
            endpoint: "https://route-api.arcgis.com/arcgis/rest/services/World/Route/NAServer/Route_World/solve",
            authentication
    });
    router.then(routeHandler).catch((error) => {
            console.error(error);
            alert("There was a problem using the route service. See the console for details.");
    });

    return {route:min_path,total_length:document.getElementById("total_length").value}

}

console.log(shortest_path())

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

function mapChangeHandler(e){
    var latlng = e.latlng;
    destination_marker.setLatLng(latlng)
    destination_latlng.lat = latlng.lat;
    destination_latlng.lng = latlng.lng;
    lat.value = latlng.lat;
    lng.value = latlng.lng;
    var esri_reverseGeocoder = L.esri.Geocoding.reverseGeocode({apikey: apiKey}).latlng(latlng);
    esri_reverseGeocoder.run(reverseGeocoderHandler);
    for (let i=0;i < num_of_store.value;i++){
        store_lat = document.getElementById(`store_${i}_lat`)
        store_lng = document.getElementById(`store_${i}_lng`)

        antpaths[i].clearLayers()

        //distance = Math.pow(Math.pow(lat.value-store_lat.value,2.) + Math.pow(lng.value-store_lng.value,2.),0.5) * 111.319
        distance = calDistance(destination_latlng,stores_latlng[i])
        let polyline = L.polyline.antPath([[lat.value,lng.value],[store_lat.value,store_lng.value]], {
          "delay": 400,
          "dashArray": [
            10,
            20
          ],
          "weight": 5,
          "color": distance > MAX_DISTANCE ? "red" : (distance > MAX_DISTANCE/2 ? "orange" : "#15ff00"),
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
    shortest_path();
    sleep(1000);
}

store_table = document.getElementById("store_table");

map.on("click",mapChangeHandler);

var store_table_observer = new MutationObserver(function(mutations, observer) {
    console.log(mutations)
    $(store_table).trigger("change");
});


store_table_observer.observe(store_table, {
    attributes: true
});
$(store_table).change(mapChangeHandler);


$(document).on('submit','#location',function(e){
    e.preventDefault();
    let inner_country = "";
    let inner_region = "";
    let inner_subregion_1 = "";
    let inner_subregion_2 = "";
    let inner_total_length = 0;
    var esri_reverseGeocoder = L.esri.Geocoding.reverseGeocode({apikey: apiKey}).latlng({lat:$("#lat").val(),lng:$("#lng").val()});
    esri_reverseGeocoder.run((error,result)=>{
        if(error){
            console.error(error)
        }else{
            console.log(result);

            inner_country.value = result.address.CntryName
            inner_region.value = result.address.Region
            inner_subregion_1.value = result.address.District != "" ? result.address.District : result.address.City
            inner_subregion_2.value = result.address.Neighborhood
        }
    });
    shortest_path()

    $.ajax({
        type:'POST',
        url:'/current-order/',
        data:
        {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            method_tag:"location",
            lat:$("#lat").val(),
            lng:$("#lng").val(),
            address:$("#address").val(),
            country:inner_country,
            region:inner_region,
            subregion_1:inner_subregion_1,
            subregion_2:inner_subregion_2,
            total_length:$("#total_length").val()
        }
    })
    location.reload()
});
$(document).on('submit','#submit_order_form',function(e){
    e.preventDefault();

    shortest_path()

    $.ajax({
        type:'POST',
        url:'/current-order/',
        data:
        {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            method_tag:"submit_order",
            password:$("#password").val()
            total_length:$("#total_length").val()
        }
    })
    location.reload()
});



