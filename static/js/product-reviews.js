reviews_section = document.getElementById('reviews_section');
review_pagination = document.getElementById('review_pagination');


function reviewsRefresh(page_id){
    $.ajax({
        type:'POST',
        url:`/current-store/product/${$("#slug").val()}/${page_id}/get-reviews`,
        data:
        {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data){
            let json = $.parseJSON(data);
            console.log(json)
            review_pagination.innerHTML = ``

            for(let i = 1;i<=json.num_pages;i++){
                review_pagination.innerHTML += `
                <li onclick = "reviewsRefresh(${i});" ${ i == page_id ? 'class="active"' : ""}><a>${i}</a></li>
                `
            }

            reviews_section.innerHTML = ''
            for(let i = 0;i < json.reviews.length;i++){
                reviews_section.innerHTML += `
                <div style = "border-style:solid; border-width: thin; padding:10px; margin:10px">
                <div style = "display:flex;justify-content: flex-start;">
                    <img src="${json.reviews[i].avatar_url}" class = "avatar" style = "margin-right:10px;">

                    <div style="position: relative;bottom:20px;">
                        <h3>${json.reviews[i].author_name}</h3>
                        <h5>${json.reviews[i].updated}</h5>

                        ${json.reviews[i].is_updated ? "<h5>Đã chỉnh sửa</h5>" : ""}
                    </div>
                </div>

                <hr style = "margin:0px; position: relative;bottom:10px;">

                <input id="rating_${i}" type="text" name = "rating" value = "${json.reviews[i].rating}">

                <hr style = "margin:0px; position: relative;bottom:10px;">

                <h5><b>${json.reviews[i].title}</b></h5>
                <h5>${json.reviews[i].review}</h5>
                <img src="${json.reviews[i].image_url !== null ? json.reviews[i].image_url : ""}" style = "${json.reviews[i].image_url !== null ? "width:30vw; height:18.54vw;" : ""}">
                </div>`
                $(`#rating_${i}`).rating({min:0, max:5, step:0.5,
                                                             size:'md',starCaptions:(val)=>{return `${val}`},
                                                             displayOnly:true});
            }
        },
        error: function(data){
           let json = $.parseJSON(data);
           //console.log(json);
        }
    })
}
reviewsRefresh(1)