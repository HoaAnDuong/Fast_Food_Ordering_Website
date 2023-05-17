// Create a data object with labels and values

var picker = undefined;

var cmbChartType = document.getElementById('cmbChartType');

var chart_section = document.getElementById('chart_section');

var order_product_chart = undefined;



function createGraph(){
    switch(cmbChartType.value){
        case "hour":
            chart_section.innerHTML =
            `
                <h4>Chọn ngày</h4>
                <input type = "date" name = "picker" id = "picker">
                <button class = "btn" id = "today-refresh">Đặt lại về hôm nay</button>
                <canvas id="order_product_chart"></canvas>
            `
            picker = document.getElementById('picker');

            picker.valueAsDate = new Date(Date.now());

            var labels = ["00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00"]

            var data = {
              labels: labels,
              datasets: [
              {
                label: 'Đang được đặt',
                data: [],
                backgroundColor:
                  '#f0f564',
                order:0,
              },
              {
                label: 'Đã nhận hàng',
                data: [],
                backgroundColor:
                  '#1cb305',
                order:1,
              },
              {
                label: 'Bị hủy',
                data: [],
                backgroundColor:
                  '#de0909',
                order:2,
              }]
            };

            // Create a config object with type and options
            var config = {
                type: 'bar',
                data: data,
                options: {
                     plugins: {
                        title: {
                            display: true,
                            text: 'Số lượng các món được đặt',
                            font:{
                                size:25
                            }
                        },
                        subtitle: {
                            display: true,
                            text: picker.valueAsDate.toDateString(),
                            font:{
                                size:20
                            }
                        }
                    },
                    scales: {
                      x: {
                        stacked: true,
                      },
                      y: {
                        startAtZero: true,
                        stacked: true
                      }
                    }
                },
            };
            break;
        case "day":
            chart_section.innerHTML =
            `
                <h4>Chọn tháng</h4>
                <input type = "month" name = "picker" id = "picker">
                <button class = "btn" id = "today-refresh">Đặt lại về tháng này</button>
                <canvas id="order_product_chart"></canvas>
            `
            picker = document.getElementById('picker');

            picker.valueAsDate = new Date(Date.now());

            var labels = [];

            for (var i = 1; i <= new Date(picker.valueAsDate.getYear(), picker.valueAsDate.getMonth(), 0).getDate()+1; i++) {
              labels.push(i);
            }

            var data = {
              labels: labels,
              datasets: [
              {
                label: 'Đang được đặt',
                data: [],
                backgroundColor:
                  '#f0f564',
                order:0,
              },
              {
                label: 'Đã nhận hàng',
                data: [],
                backgroundColor:
                  '#1cb305',
                order:1,
              },
              {
                label: 'Bị hủy',
                data: [],
                backgroundColor:
                  '#de0909',
                order:2,
              }]
            };

            // Create a config object with type and options
            var config = {
                type: 'bar',
                data: data,
                options: {
                     plugins: {
                        title: {
                            display: true,
                            text: 'Số lượng các món được đặt',
                            font:{
                                size:25
                            }
                        },
                        subtitle: {
                            display: true,
                            text: picker.valueAsDate.toDateString(),
                            font:{
                                size:20
                            }
                        }
                    },
                    scales: {
                      x: {
                        stacked: true,
                      },
                      y: {
                        startAtZero: true,
                        stacked: true
                      }
                    }
                },
            };
            break;

        case "month":
            chart_section.innerHTML =
            `
                <h4>Chọn năm</h4>
                <input type = "number" name = "picker" id = "picker">
                <button class = "btn" id = "today-refresh">Đặt lại về năm nay</button>
                <canvas id="order_product_chart"></canvas>
            `
            picker = document.getElementById('picker');

            picker.value = new Date(Date.now()).getYear() + 1900;

            var labels = ["January", "February", "March", "April", "May", "June",
                          "July", "August", "September", "October", "November", "December"
                        ];
            var data = {
              labels: labels,
              datasets: [
              {
                label: 'Đang được đặt',
                data: [],
                backgroundColor:
                  '#f0f564',
                order:0,
              },
              {
                label: 'Đã nhận hàng',
                data: [],
                backgroundColor:
                  '#1cb305',
                order:1,
              },
              {
                label: 'Bị hủy',
                data: [],
                backgroundColor:
                  '#de0909',
                order:2,
              }]
            };

            // Create a config object with type and options
            var config = {
                type: 'bar',
                data: data,
                options: {
                     plugins: {
                        title: {
                            display: true,
                            text: 'Số lượng các món được đặt',
                            font:{
                                size:25
                            }
                        },
                        subtitle: {
                            display: true,
                            text: picker.value,
                            font:{
                                size:20
                            }
                        }
                    },
                    scales: {
                      x: {
                        stacked: true,
                      },
                      y: {
                        startAtZero: true,
                        stacked: true
                      }
                    }
                },
            };
            break;

    }



    // Get a reference to the canvas element
    var ctx = document.getElementById('order_product_chart').getContext('2d');

    // Create a new chart instance using the config object
    order_product_chart = new Chart(ctx, config);


}




function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function getOrderProductData(){
    $.ajax({
        type:'POST',
        url:`/current-store/order-product/${$("#page_id").val()}/get-data`,
        data:
        {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            statistic_tag:cmbChartType.value,
            statistic_data: cmbChartType.value != "month" ? picker.valueAsDate.toISOString() : picker.value
        },
        success: function(data){
            let json = $.parseJSON(data);
            console.log(json);

            document.getElementById("num_submitted_product").innerHTML = json.num_submitted_product

            order_product_table = document.getElementById("order_product_table");
            order_product_rows = order_product_table.tBodies[0].rows;

            for(let i = 0; i < json.order_product.length;i++){
                    if(order_product_rows[i] != undefined){
                        if(order_product_rows[i].cells[0].childNodes[0].innerHTML != json.order_product[i].name){
                            location.reload();
                        }
                        if(order_product_rows[i].cells[6].innerHTML != json.order_product[i].updated){
                            order_product_rows[i].cells[0].innerHTML = `<a href = "/product/${json.order_product[i].slug}">${json.order_product[i].name}</a>`
                            order_product_rows[i].cells[1].innerHTML = `<img style = "width:100px; height:62px;" src = "${json.order_product[i].image_url}">`
                            order_product_rows[i].cells[2].innerHTML = json.order_product[i].quantity;
                            order_product_rows[i].cells[3].innerHTML = json.order_product[i].price;
                            order_product_rows[i].cells[4].innerHTML = json.order_product[i].total;
                            order_product_rows[i].cells[5].innerHTML = json.order_product[i].created;
                            order_product_rows[i].cells[6].innerHTML = json.order_product[i].updated;
                            order_product_rows[i].cells[7].innerHTML = json.order_product[i].status;
                            order_product_rows[i].cells[8].innerHTML = json.order_product[i].address;
                        }
                    }else{
                        location.reload();
                }
            }



            num_submitted = []
            num_completed = []
            num_cancelled = []
            json.statistic.forEach(hour => {
                num_submitted.push(hour.submitted);
                num_completed.push(hour.completed);
                num_cancelled.push(hour.cancelled);
            });
            order_product_chart.data.datasets[0].data = num_submitted;
            order_product_chart.data.datasets[1].data = num_completed;
            order_product_chart.data.datasets[2].data = num_cancelled;


            order_product_chart.update();

        },
        error: function(data){
           let json = $.parseJSON(data);
           console.log(json);
        }
    });

}

async function orderProductRefresh(){
    while(true){
        getOrderProductData();
        await sleep(5000);
    }
};

createGraph()

function updateGraph(){
    if(cmbChartType.value == "hour"){
        order_product_chart.options.plugins.subtitle.text = picker.valueAsDate.toDateString();
    }

    if(cmbChartType.value == "day"){
        order_product_chart.data.labels = []
        order_product_chart.options.plugins.subtitle.text = picker.valueAsDate.toDateString();
        for (var i = 1; i <= new Date(picker.valueAsDate.getYear(), picker.valueAsDate.getMonth(), 0).getDate()+1; i++) {
            order_product_chart.data.labels.push(i);
        }

    }

    if(cmbChartType.value == "month"){
        order_product_chart.options.plugins.subtitle.text = picker.valueAsDate.toDateString();
    }

    order_product_chart.update();

}

$("#cmbChartType").on('change',()=>{
    createGraph();
    $("#picker").on('change',()=>{
            updateGraph();
            getOrderProductData();
    })
    updateGraph();
    getOrderProductData();
})




$("#today-refresh").on('click',() => {
    picker.valueAsDate = new Date(Date.now());
    createGraph();
    updateGraph();
    getOrderProductData();
})


orderProductRefresh();

