reviews_section = document.getElementById('reviews_section');
review_pagination = document.getElementById('review_pagination');
is_filtered = false

const labels = [5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1, 0.5, 0];
const data = {
  labels: labels,
  datasets: [
    {
      label: 'Số lượt đánh giá',
      data: [],
      color: "#0390fc",
    },
  ]
};

const config = {
  type: 'bar',
  data: data,
  options: {
    indexAxis: 'y',
    // Elements options apply to all of the options unless overridden in a dataset
    // In this case, we are setting the border of each horizontal bar to be 2px wide
    elements: {
      bar: {
        borderWidth: 2,
      }
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Điểm đánh giá',
          font: {
            size: 15,
            lineHeight: 1.2,
            weight: 'bold',
          },
          padding: {top: 0, left: 0, right: 0, bottom: 0}
        }
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Số lượt đánh giá',
          font: {
            size: 15,
            lineHeight: 1.2,
            weight: 'bold',
          },
          padding: {top: 0, left: 0, right: 0, bottom: 0}
        }
      }
    },
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Số lượng đánh giá'
      }
    }
  },
};

// Get a reference to the canvas element
var ctx = document.getElementById('rating_chart').getContext('2d');

// Create a new chart instance using the config object
rating_chart = new Chart(ctx, config);

$("#filter_button").click(() => {
    is_filtered = !is_filtered
    console.log(is_filtered)
    if(is_filtered){
        $("#filter_button").attr("class","btn btn-danger");
        $("#filter_button").html("Tắt bộ lọc");
    }else{
        $("#filter_button").attr("class","btn btn-primary");
        $("#filter_button").html("Bật bộ lọc");
    }
    reviewsRefresh(1);
});


function reviewsRefresh(page_id){
    $.ajax({
        type:'POST',
        url:`/moderator/products/${$("#slug").val()}/${page_id}/get-reviews`,
        data:
        is_filtered ?
        {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            filtered_author:$('#filtered_author').val(),
            filtered_rating:$('#filtered_rating').val(),
        }:
        {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
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
                <input type = "hidden" id = "review_${i}_id" value = ${json.id}>
                </div>`
                $(`#rating_${i}`).rating({min:0, max:5, step:0.5,
                                                             size:'md',starCaptions:(val)=>{return `${val}`},
                                                             displayOnly:true});

                rating_chart.data.datasets[0].data = json.statistic;
                rating_chart.update();
            }
        },
        error: function(data){
           let json = $.parseJSON(data);
           //console.log(json);
        }
    })
}

reviewsRefresh(1)