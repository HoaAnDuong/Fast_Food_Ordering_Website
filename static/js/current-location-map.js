


var current_location_map = L.map('current_location_map').setView([lat.value,lng.value], 15);

//roadmap tilelayer:'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'

L.tileLayer('http://mt1.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}', {
  maxZoom: 22,
  attribution: 'Google'
}).addTo(current_location_map);

var locationTab = document.getElementById('deliverer-profile');
var observer1 = new MutationObserver(function(){
  map.invalidateSize();
});

var current_location_marker = L.marker([lat.value,lng.value])

current_location_marker.addTo(current_location_map)

var current_lngLatString = `${Math.round(lng.value * 100000) / 100000}, ${Math.round(lat.value * 100000) / 100000}`;
current_location_marker.bindPopup(`<b>${lngLatString}</b><p>${address.value}</p>`);
current_location_marker.openPopup();

//function reverseGeocoderHandlerCurrentLocation(error,result){
//    if(error){
//    }else{
//        console.log(result);
//        lngLatString = `${Math.round(result.latlng.lng * 100000) / 100000}, ${Math.round(result.latlng.lat * 100000) / 100000}`;
//        current_location_marker.bindPopup(`<b>${lngLatString}</b><p>${result.address.LongLabel}</p>`);
//        current_location_marker.openPopup();
//    }
}



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

var observer = new MutationObserver(function(mutations, observer) {
    console.log(mutations)
    $(timestamp).trigger("change");
});
observer.observe(timestamp, {
    attributes: true
});
$(timestamp).change(changeCurrentLocationMarker);

changeCurrentLocationMarker();
