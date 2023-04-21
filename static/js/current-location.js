const current_lat = document.getElementById("current_lat")
const current_lng = document.getElementById("current_lng")
const timestamp = document.getElementById("timestamp")
const current_location_form = document.forms["current-location-form"]

function successCallback(e){
    console.log(e);
    current_lat.value = e.coords.latitude
    current_lng.value = e.coords.longitude
    timestamp.value = e.timestamp
};

function errorCallback(error){
    console.log(error);
};

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

$(document).on('submit','#current-location-form',function(e){
e.preventDefault();
$.ajax({
    type:'POST',
    url:'/current-location',
    data:
    {
        current_lat:$("#current_lat").val(),
        current_lng:$("#current_lng").val(),
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    }
    })
});
async function currentLocationRefresh(){
    while(true){
        navigator.geolocation.getCurrentPosition(successCallback, errorCallback);

        $.ajax({
            type:'POST',
            url:'/current-location',
            data:
            {
                current_lat:$("#current_lat").val(),
                current_lng:$("#current_lng").val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data){
               let json = $.parseJSON(data);
               console.log(json);
            },
            error: function(data){
               let json = $.parseJSON(data);
               console.log(json);
            }
        });
        await sleep(10000);
    }
};
currentLocationRefresh();