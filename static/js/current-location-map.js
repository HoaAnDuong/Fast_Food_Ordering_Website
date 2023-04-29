


var current_location_map = L.map('current_location_map').setView([lat.value,lng.value], 15);

//roadmap tilelayer:'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'

L.tileLayer('http://mt1.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}', {
  maxZoom: 22,
  attribution: 'Google'
}).addTo(current_location_map);

var locationTab = document.getElementById('deliverer-profile');
var observer1 = new MutationObserver(function(){
  current_location_map.invalidateSize();
});

observer1.observe(locationTab, {attributes: true});

var delivererIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});


var current_location_marker = L.marker([lat.value,lng.value],{icon: delivererIcon})

current_location_marker.addTo(current_location_map)

var current_lngLatString = `${Math.round(lng.value * 100000) / 100000}, ${Math.round(lat.value * 100000) / 100000}`;
current_location_marker.bindPopup(`<b>${lngLatString}</b><br><b>Vị trí hiện tại</b>`);
current_location_marker.openPopup();

//function reverseGeocoderHandlerCurrentLocation(error,result){
//    if(error){
//    }else{
//        console.log(result);
//        lngLatString = `${Math.round(result.latlng.lng * 100000) / 100000}, ${Math.round(result.latlng.lat * 100000) / 100000}`;
//        current_location_marker.bindPopup(`<b>${lngLatString}</b><p>${result.address.LongLabel}</p>`);
//        current_location_marker.openPopup();
//    }
//}



//current_location_map.locate(
//    {setView:true}
//);
//
//current_location_map.on('locationfound',onLocationFoundHandler);

//function successCallback(e){
//    console.log(e);
//    var latlng = L.latLng({lat:current_lat.value,
//                            lng:current_lng.value});
//    current_location_marker.setLatLng(latlng)
//    lngLatString = `${Math.round(latlng.lng * 100000) / 100000}, ${Math.round(latlng.lat * 100000) / 100000}`;
//    current_location_marker.bindPopup(`<b>${lngLatString}</b>`);
//};
//
//function errorCallback(error){
//  console.log(error);
//};
//navigator.geolocation.getCurrentPosition(successCallback, errorCallback);

function changeCurrentLocationMarker(){

    var latlng = L.latLng({lat:current_lat.value,
                            lng:current_lng.value});
    current_location_marker.setLatLng(latlng)
    lngLatString = `${Math.round(latlng.lng * 100000) / 100000}, ${Math.round(latlng.lat * 100000) / 100000}`;
    current_location_marker.bindPopup(`<b>${lngLatString}</b>`);
};

var current_lat_observer = new MutationObserver(function(mutations, observer) {
    console.log(mutations)
    $(current_lat).trigger("change");
});
current_lat_observer.observe(current_lng, {
    attributes: true
});
$(current_lat).change(changeCurrentLocationMarker);

var current_lng_observer = new MutationObserver(function(mutations, observer) {
    console.log(mutations)
    $(current_lng).trigger("change");
});
current_lng_observer.observe(current_lng, {
    attributes: true
});
$(current_lng).change(changeCurrentLocationMarker);

changeCurrentLocationMarker();
