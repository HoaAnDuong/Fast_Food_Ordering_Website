product_pagination = document.getElementById("product_pagination");
product_table = document.getElementById("product_table");
product_body = product_table.tBodies[0];
product_is_filtered = false;

$("#product_filter_button").click(() => {
    product_is_filtered = !product_is_filtered
    console.log(product_is_filtered)
    if(product_is_filtered){
        $("#product_filter_button").attr("class","btn btn-danger");
        $("#product_filter_button").html("Tắt bộ lọc");
    }else{
        $("#product_filter_button").attr("class","btn btn-primary");
        $("#product_filter_button").html("Bật bộ lọc");
    }
    productRefresh(1);
});


function productRefresh(page_id){
    $.ajax({
        type:'POST',
        url:`/moderator/get-products/${page_id}`,
        data:
        product_is_filtered ?
        {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            product_name:$("#filtered_product_name").val(),
            status:$("#filtered_status").val()
        } :
        {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        }
        ,
        success: function(data){
            let json = $.parseJSON(data);
            console.log(json)
            product_pagination.innerHTML = ``

            for(let i = 1;i<=json.num_pages;i++){
                product_pagination.innerHTML += `
                <li onclick = "productRefresh(${i});" ${ i == page_id ? 'class="active"' : ""}><a>${i}</a></li>
                `
            }
            product_body.innerHTML = ''
            for(let i = 0;i<json.products.length;i++){
                product = json.products[i]
                product_body.innerHTML += `
                <tr>
                    <td><a href = "${product.url}">${product.name}</a></td>
                    <td><img src = "${product.image_url}" style = "width:100px;height:62px"></td>
                    <td>${product.category}</td>
                    <td>${product.status}</td>
                    <td>${product.price}</td>
                    <td><input id="rating_${i}" type="text" name = "rating" value = "${product.rating.rating__avg != null ? product.rating.rating__avg : 0}"></td>
                    <td><a href = "${product.url}"><button class = "btn btn-primary">Kiểm duyệt</button></a></td>
                </tr>
                `
                $(`#rating_${i}`).rating({min:0, max:5, step:0.5,
                                                             size:'xs',starCaptions:(val)=>{return `${val}`},
                                                             displayOnly:true});
            }

        },
        error: function(data){
           let json = $.parseJSON(data);
           //console.log(json);
        }
    })
}

productRefresh(1);