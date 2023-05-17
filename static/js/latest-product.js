function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function latestProductRefresh(){
    while(true){
        $.ajax({
            type:'POST',
            url:'/current-store/latest-order-product',
            data:
            {
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data){
                let json = $.parseJSON(data);
                //console.log(json);
                latest_order_product_name = document.getElementById("latest_order_product_name");
                latest_order_product_price = document.getElementById("latest_order_product_price");
                latest_order_product_status = document.getElementById("latest_order_product_status");
                latest_order_product_updated = document.getElementById("latest_order_product_updated");
                latest_order_product_quantity = document.getElementById("latest_order_product_quantity");
                if(json.updated != latest_order_product_updated.value){
                    //if(latest_order_product_updated.value !== "")
                    switch (json.status) {
                        case "submitted":
                            alert(`${json.updated}: Món ăn ${json.product_name} đã được đặt với số lượng ${json.quantity}`);
                            break;
                        case "delivering":
                            alert(`${json.updated}: Món ăn ${json.product_name} đã được nhận và đang được giao tới khách hàng.`);
                            break;
                        case "cancelled":
                            alert(`${json.updated}: Món ăn ${json.product_name} đã bị hủy.`);
                            break;
                    }
                    latest_order_product_name.value = json.product_name
                    latest_order_product_price.value = json.price;
                    latest_order_product_status.value = json.status;
                    latest_order_product_updated.value = json.updated;
                    latest_order_product_quantity.value = json.quantity;
                }
            },
            error: function(data){
               let json = $.parseJSON(data);
               //console.log(json);
            }
        })
        await sleep(10000);
    }
};

latestProductRefresh();