$(window).on('load', function() {
   $('#check_in_modal').modal('show');
});

$(document).on('submit','#check_in_form',function(e){
    e.preventDefault();
    $.ajax({
    type:'POST',
    url:'/check-in',
    data:
    {
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        end_time:$('#end_time').val()
    },
    success:function (data){
        location.reload();
    },
    error: function (jqXHR, textStatus, errorThrown) {
        alert('Giờ kết thúc không hợp lệ');
        console.log(errorThrown);
    }
    });
});