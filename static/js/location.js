
const lat = document.getElementById("lat")
const lng = document.getElementById("lng")
const address = document.getElementById("address")
const country = document.getElementById("country")
const region = document.getElementById("region")
const subregion_1 = document.getElementById("subregion_1")
const subregion_2 = document.getElementById("subregion_2")


var map = L.map('map').setView([lat.value,lng.value], 15);

//roadmap tilelayer:'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'

L.tileLayer('http://mt1.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}', {
  maxZoom: 22,
  attribution: 'Google'
}).addTo(map);

var location_marker = L.marker([lat.value,lng.value])

location_marker.addTo(map)

var locationTab = document.getElementById('location');
var observer1 = new MutationObserver(function(){
  location_map.invalidateSize();
});
observer1.observe(locationTab, {attributes: true});

var lngLatString = `${Math.round(lng.value * 100000) / 100000}, ${Math.round(lat.value * 100000) / 100000}`;
location_marker.bindPopup(`<b>${lngLatString}</b><p>${address.value}</p>`);
location_marker.openPopup();

const apiKey = "AAPK5a1319c4648247188e709e0176c0a073pqXTy5i1h6UW8b2prBtWB59DSR7OsFx-2yGG0CpcSTeKcf8ZkrkMbg6EYLZ0p3VW";

const authentication = arcgisRest.ApiKeyManager.fromKey(apiKey);

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
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
        location_marker.bindPopup(`<b>${lngLatString}</b><p>${result.address.Match_addr}</p>`);
        location_marker.openPopup();
    }
}

function onMapClickHandler(e){
    var latlng = e.latlng;
    location_marker.setLatLng(latlng)
    lat.value = latlng.lat;
    lng.value = latlng.lng;
    var esri_reverseGeocoder = L.esri.Geocoding.reverseGeocode({apikey: apiKey}).latlng(latlng);
    esri_reverseGeocoder.run(reverseGeocoderHandler);
    sleep(100)
}



map.on("click",onMapClickHandler);