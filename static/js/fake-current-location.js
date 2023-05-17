const current_lat = document.getElementById("current_lat")
const current_lng = document.getElementById("current_lng")
const timestamp = document.getElementById("timestamp")
const current_location_form = document.forms["current-location-form"]


var fake_location_map = L.map('fake_location_map').setView([current_lat.value,current_lng.value], 15);

//roadmap tilelayer:'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'

L.tileLayer('http://mt1.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}', {
  maxZoom: 22,
  attribution: 'Google'
}).addTo(fake_location_map);

var fake_location_marker = L.marker([current_lat.value,current_lng.value])

fake_location_marker.addTo(fake_location_map)

var locationTab = document.getElementById('fake_location_collapse');
var observer1 = new MutationObserver(function(){
  fake_location_map.invalidateSize();
});
observer1.observe(locationTab, {attributes: true});

var lngLatString = `${Math.round(current_lat.value * 100000) / 100000}, ${Math.round(current_lng.value * 100000) / 100000}`;
fake_location_marker.bindPopup(`<b>${lngLatString}</b>`);
fake_location_marker.openPopup();


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function onMapClickHandler(e){
    var latlng = e.latlng;
    fake_location_marker.setLatLng(latlng)
    current_lat.value = latlng.lat;
    current_lng.value = latlng.lng;
    var lngLatString = `${Math.round(current_lat.value * 100000) / 100000}, ${Math.round(current_lng.value * 100000) / 100000}`;
    fake_location_marker.bindPopup(`<b>${lngLatString}</b>`);
    fake_location_marker.openPopup();
    sleep(100)
}

async function currentLocationRefresh(){
    while(true){
         timestamp.value = Math.floor(Date.now() / 1000);
         $.ajax({
            type:'POST',
            url:'/current-location',
            data:
            {
                current_lat:current_lat.value,
                current_lng:current_lng.value,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data){
               let json = $.parseJSON(data);
               console.log(json);
               if(document.getElementById("delivery_check").value != json.delivery_check){
                   document.getElementById("delivery_check").value = json.delivery_check;
                   alert(json.delivery_check == "True" ? "Bạn đang có đơn vận chuyển mới." : "Đơn vận chuyển của bạn đã kết thúc.");
               }
            },
            error: function(data){
               let json = $.parseJSON(data);
               console.log(json);
            }
        });
        await sleep(2000);
    }
};

fake_location_map.on("click",onMapClickHandler);

currentLocationRefresh();