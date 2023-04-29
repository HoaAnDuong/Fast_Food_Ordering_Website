function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function orderDataRefresh(){
    while(true){
        $.ajax({
            type:'GET',
            url:'/current-delivery/get-data',
            data:
            {
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data){
                let json = $.parseJSON(data);
                console.log(json)
                if(json.store_list.length != document.getElementById("num_of_store").value){
                    location.reload();
                }
                if(document.getElementById("order_status").innerHTML != json.order_status){
                    location.reload();
                }
                document.getElementById("delivery_status").innerHTML = json.delivery_status
                document.getElementById("payment_status").innerHTLM = json.payment_status
                document.getElementById("product_total").innerHTML = json.product_total
                document.getElementById("delivery_fee").innerHTML = json.delivery_fee
                document.getElementById("nighttime_fee").innerHTML = json.nighttime_fee
                document.getElementById("total").innerHTML = json.total
                order_product_table = document.getElementById("order_product_table")
                order_product_rows = order_product_table.tBodies[0].rows


                for(let i = 0; i < json.order_product.length;i++){
                    if(order_product_rows[i] != undefined){
                        if(order_product_rows[i].cells[0].innerHTML != json.order_product[i].name){
                            location.reload();
                        }
                        if(order_product_rows[i].cells[6].innerHTML != json.order_product[i].updated){
                            order_product_rows[i].cells[0].innerHTML = `${json.order_product[i].name}`
                            order_product_rows[i].cells[1].innerHTML = `<img style = "width:100px; height:62px;" src = "${json.order_product[i].image_url}">`
                            order_product_rows[i].cells[2].innerHTML = json.order_product[i].price;
                            order_product_rows[i].cells[3].innerHTML = json.order_product[i].quantity;
                            order_product_rows[i].cells[4].innerHTML = json.order_product[i].total;
                            order_product_rows[i].cells[5].innerHTML = json.order_product[i].status;
                            order_product_rows[i].cells[6].innerHTML = json.order_product[i].updated;
                            order_product_rows[i].cells[7].innerHTML = json.order_product[i].note;
                        }
                    }else{
                        location.reload();
                    }

                }
                order_product_table.tFoot.rows[0].cells[4] = json.product_total

                log_table = document.getElementById("log_table")
                log_table_body = log_table.tBodies[0]
                log_table_rows = log_table.tBodies[0].rows
                if(log_table_rows.length < json.logs.length){
                    alert(json.logs[json.logs.length-1].log);
                    for(let i = log_table_rows.length; i < json.logs.length; i++){
                        let row = log_table_body.insertRow(i);
                        let cell0 = row.insertCell(0);
                        let cell1 = row.insertCell(1);
                        cell0.innerHTML = json.logs[i].created;
                        cell1.innerHTML = json.logs[i].log;
                    }
                }
            },
            error: function(data){
               let json = $.parseJSON(data);
               console.log(json);
            }
        });
        await sleep(10000);
    }
}




orderDataRefresh();