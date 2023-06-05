order_pagination = document.getElementById("order_pagination");
order_table = document.getElementById("order_table");
order_body = order_table.tBodies[0];


function orderListRefresh(page_id){
    $.ajax({
        type:'POST',
        url:`/profile/order-list/${page_id}/get-data`,
        data:
        {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data){
            let json = $.parseJSON(data);
            console.log(json)
            order_pagination.innerHTML = ``

            for(let i = 1;i<=json.num_pages;i++){
                order_pagination.innerHTML += `
                <li onclick = "orderListRefresh(${i});" ${ i == page_id ? 'class="active"' : ""}><a>${i}</a></li>
                `
            }

            order_body.innerHTML = ''

            for(let i = 0;i<json.orders.length;i++){
                let order = json.orders[i];
                deliverer_section = order.deliverer !=null ?  `
                    <h5>${order.deliverer.name}</h5>
                    <h5>${order.deliverer.phone_number}</h5>
                    <h5>${order.deliverer.email}</h5>
                ` : ``;



                order_body.innerHTML += `
                <tr>
                    <td>${order.created}</td>
                    <td>${order.updated}</td>
                    <td>${order.payment_method}</td>
                    <td>${order.order_status}</td>
                    <td>${order.delivery_status}</td>
                    <td>${order.payment_status}</td>
                    <td>${order.total}</td>
                    <td>${deliverer_section}</td>
                    <td>${order.total_length}(km)</td>
                    <td><button onClick= "orderRedirect(${order.id})" class = "btn btn-primary">Xem thông tin</button></td>
                </tr>
                `;
            }

        },
        error: function(data){
           let json = $.parseJSON(data);
           //console.log(json);
        }
    })
}

function orderRedirect(id){
    window.location.replace(`/profile/orders/${id}`);
}

orderListRefresh(1)
