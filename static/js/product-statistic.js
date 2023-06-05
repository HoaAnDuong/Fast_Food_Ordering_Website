var picker = undefined;

var cmbChartType = document.getElementById('cmbChartType');

var chart_section = document.getElementById('chart_section');

var order_product_chart = undefined;

var picker = undefined;

var cmbChartType = document.getElementById('cmbChartType');

var chart_section = document.getElementById('chart_section');

var order_product_chart = undefined;

var order_product_pie_chart = undefined;

function createGraph(){
    switch(cmbChartType.value){
        case "hour":
            chart_section.innerHTML =
            `
                <h4>Chọn ngày</h4>
                <input type = "date" name = "picker" id = "picker">
                <button class = "btn" id = "today-refresh">Đặt lại về hôm nay</button>
                <canvas id="order_product_chart"></canvas>
                <div style = "width: 60vw; height:40vw;display:flex;justify-content:space-between">
                <canvas id="order_product_pie_chart" ></canvas>
                </div>
            `
            picker = document.getElementById('picker');

            picker.valueAsDate = new Date(Date.now());

            var labels = ["00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00"]

            var data = {
              labels: labels,
              datasets: [
              {
                label: 'Doanh thu(Đang được đặt)',
                data: [],
                backgroundColor:
                  '#f0f564',
                order:1,
                yAxisID: 'y',
              },
              {
                label: 'Doanh thu(Đã nhận hàng)',
                data: [],
                backgroundColor:
                  '#1cb305',
                order:1,
                yAxisID: 'y',
              },
              {
                label: 'Doanh thu(Bị hủy)',
                data: [],
                backgroundColor:
                  '#de0909',
                order:1,
                yAxisID: 'y',
              },{
                label: 'Số lượng(Đang được đặt)',
                data: [],
                borderColor:
                  '#f0f564',
                backgroundColor:
                  '#f0f564',
                order:0,
                type:"line",
                yAxisID: 'y2',
              },
              {
                label: 'Số lượng(Đã nhận hàng)',
                data: [],
                borderColor:
                  '#1cb305',
                backgroundColor:
                  '#1cb305',
                order:0,
                type:"line",
                yAxisID: 'y2',
              },
              {
                label: 'Số lượng(Bị hủy)',
                data: [],
                borderColor:
                  '#de0909',
                backgroundColor:
                  '#de0909',
                order:0,
                type:"line",
                yAxisID: 'y2',
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
                            text: 'Doanh thu theo giờ trong ngày',
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
                        stacked: true,
                        display: true,
                        title: {
                          display: true,
                          text: 'Doanh thu(VND)',
                          font: {
                            size: 15,
                            lineHeight: 1.2,
                            weight: 'bold',
                          },
                          padding: {top: 0, left: 0, right: 0, bottom: 0}
                        }
                      },
                      y2: {
                        startAtZero: true,
                        stacked: true,
                        display: true,
                        position: 'right',
                        title: {
                          display: true,
                          text: 'Số lượng(VND)',
                          font: {
                            size: 15,
                            lineHeight: 1.2,
                            weight: 'bold',
                          },
                          padding: {top: 0, left: 0, right: 0, bottom: 0}
                        }
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
                <div style = "width: 60vw; height:40vw;display:flex;justify-content:space-between">
                <canvas id="order_product_pie_chart" ></canvas>
                </div>
            `
            picker = document.getElementById('picker');

            picker.valueAsDate = new Date(Date.now());

            var labels = [];

            for (var i = 1; i < new Date(picker.valueAsDate.getYear(), picker.valueAsDate.getMonth() + 1, 0).getDate()+1; i++) {
              labels.push(i);
            }

            var data = {
              labels: labels,
              datasets: [
              {
                label: 'Doanh thu(Đang được đặt)',
                data: [],
                backgroundColor:
                  '#f0f564',
                order:1,
                yAxisID: 'y',
              },
              {
                label: 'Doanh thu(Đã nhận hàng)',
                data: [],
                backgroundColor:
                  '#1cb305',
                order:1,
                yAxisID: 'y',
              },
              {
                label: 'Doanh thu(Bị hủy)',
                data: [],
                backgroundColor:
                  '#de0909',
                order:1,
                yAxisID: 'y',
              },{
                label: 'Số lượng(Đang được đặt)',
                data: [],
                borderColor:
                  '#f0f564',
                backgroundColor:
                  '#f0f564',
                order:0,
                type:"line",
                yAxisID: 'y2',
              },
              {
                label: 'Số lượng(Đã nhận hàng)',
                data: [],
                borderColor:
                  '#1cb305',
                backgroundColor:
                  '#1cb305',
                order:0,
                type:"line",
                yAxisID: 'y2',
              },
              {
                label: 'Số lượng(Bị hủy)',
                data: [],
                borderColor:
                  '#de0909',
                backgroundColor:
                  '#de0909',
                order:0,
                type:"line",
                yAxisID: 'y2',
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
                            text: 'Doanh thu theo ngày trong tháng',
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
                        stacked: true,
                        display: true,
                        title: {
                          display: true,
                          text: 'Doanh thu(VND)',
                          font: {
                            size: 15,
                            lineHeight: 1.2,
                            weight: 'bold',
                          },
                          padding: {top: 0, left: 0, right: 0, bottom: 0}
                        }
                      },
                      y2: {
                        startAtZero: true,
                        stacked: true,
                        display: true,
                        position: 'right',
                        title: {
                          display: true,
                          text: 'Số lượng(VND)',
                          font: {
                            size: 15,
                            lineHeight: 1.2,
                            weight: 'bold',
                          },
                          padding: {top: 0, left: 0, right: 0, bottom: 0}
                        }
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
                <div style = "width: 60vw; height:40vw;display:flex;justify-content:space-between">
                <canvas id="order_product_pie_chart" ></canvas>
                </div>
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
                label: 'Doanh thu(Đang được đặt)',
                data: [],
                backgroundColor:
                  '#f0f564',
                order:1,
                yAxisID: 'y',
              },
              {
                label: 'Doanh thu(Đã nhận hàng)',
                data: [],
                backgroundColor:
                  '#1cb305',
                order:1,
                yAxisID: 'y',
              },
              {
                label: 'Doanh thu(Bị hủy)',
                data: [],
                backgroundColor:
                  '#de0909',
                order:1,
                yAxisID: 'y',
              },{
                label: 'Số lượng(Đang được đặt)',
                data: [],
                borderColor:
                  '#f0f564',
                backgroundColor:
                  '#f0f564',
                order:0,
                type:"line",
                yAxisID: 'y2',
              },
              {
                label: 'Số lượng(Đã nhận hàng)',
                data: [],
                borderColor:
                  '#1cb305',
                backgroundColor:
                  '#1cb305',
                order:0,
                type:"line",
                yAxisID: 'y2',
              },
              {
                label: 'Số lượng(Bị hủy)',
                data: [],
                borderColor:
                  '#de0909',
                backgroundColor:
                  '#de0909',
                order:0,
                type:"line",
                yAxisID: 'y2',
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
                            text: 'Doanh thu theo các tháng trong năm',
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
                        stacked: true,
                        display: true,
                        position: 'right',
                        title: {
                          display: true,
                          text: 'Doanh thu(VND)',
                          font: {
                            size: 15,
                            lineHeight: 1.2,
                            weight: 'bold',
                          },
                          padding: {top: 0, left: 0, right: 0, bottom: 0}
                        }
                      },
                      y2: {
                        startAtZero: true,
                        stacked: true,
                        display: true,
                        title: {
                          display: true,
                          text: 'Số lượng(VND)',
                          font: {
                            size: 15,
                            lineHeight: 1.2,
                            weight: 'bold',
                          },
                          padding: {top: 0, left: 0, right: 0, bottom: 0}
                        }
                      }
                    }
                },
            };
            break;

    }
    var data2 = {
      labels: ['Đang được đặt(Sản phẩm này)', 'Đang được đặt(Còn lại)',
      'Đã được đặt(Sản phẩm này)', 'Đã được đặt(Còn lại)',
      'Bị hủy(Sản phẩm này)', 'Bị hủy(Còn lại)'],
      datasets: [
        {
          label: 'Doanh thu(VND)',
          data: [],
          borderColor: [
            "rgba(255, 215, 0, 1)",
            "rgba(255, 215, 0, 1)",
            "rgba(255, 215, 0, 1)",
            "rgba(255, 215, 0, 1)",
            "rgba(255, 215, 0, 1)",
            "rgba(255, 215, 0, 1)"
           ],
          backgroundColor: [
            "rgba(240, 245, 100,1)",
            "rgba(240, 245, 100,0.5)",
            "rgba(28, 179, 5, 1)",
            "rgba(28, 179, 5, 0.5)",
            "rgba(222, 9, 9, 1)",
            "rgba(222, 9, 9, 0.5)"
           ],
        },
        {
          label: 'Số lượng đơn',
          data:[],
          borderColor: [
          "rgba(255, 255, 255, 1)",
          "rgba(255, 255, 255, 1)",
          "rgba(255, 255, 255, 1)",
          "rgba(255, 255, 255, 1)",
          "rgba(255, 255, 255, 1)",
          "rgba(255, 255, 255, 1)"
          ],
          backgroundColor: [
          "rgba(240, 245, 100,0.5)",
          "rgba(240, 245, 100,1)",
          "rgba(28, 179, 5, 0.5)",
          "rgba(28, 179, 5, 1)",
          "rgba(222, 9, 9, 0.5)",
          "rgba(222, 9, 9, 1)"
          ],
        }
      ]
    };
    var config2 = {
      type: 'pie',
      data: data2,
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
                display: true,
                text: 'Biều đồ tỉ lệ doanh thu và số lượng đơn hàng của sản phẩm so với các sản phẩm còn lại của cửa hàng',
                font:{
                    size:25
                }
          },
        subtitle: {
            display: true,
            text: "",
            font:{
                size:20
            }
        }
        }
      },
    };

    // Get a reference to the canvas element
    var ctx = document.getElementById('order_product_chart').getContext('2d');

    // Create a new chart instance using the config object
    order_product_chart = new Chart(ctx, config);

    // Get a reference to the canvas element
    var ctx2 = document.getElementById('order_product_pie_chart').getContext('2d');

    // Create a new chart instance using the config object
    order_product_pie_chart = new Chart(ctx2, config2);
}



function updateGraph(){
    if(cmbChartType.value == "hour"){
        order_product_chart.options.plugins.subtitle.text = picker.valueAsDate.toDateString();
    }

    if(cmbChartType.value == "day"){
        order_product_chart.data.labels = []
        order_product_chart.options.plugins.subtitle.text = picker.valueAsDate.toDateString();
        for (var i = 1; i < new Date(picker.valueAsDate.getYear(), picker.valueAsDate.getMonth() + 1, 0).getDate()+1; i++) {
            order_product_chart.data.labels.push(i);
        }

    }

    if(cmbChartType.value == "month"){
        order_product_chart.options.plugins.subtitle.text = picker.value;
    }

    order_product_chart.update();

}

function getStatisticData(){
    $.ajax({
        type:'POST',
        url:`/current-store/product/${$("#slug").val()}/get-statistic`,
        data:
        {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            statistic_tag:cmbChartType.value,
            statistic_data: cmbChartType.value != "month" ? picker.valueAsDate.toISOString() : picker.value
        },
        success: function(data){
            let json = $.parseJSON(data);

            console.log(json);

            order_product_chart.data.datasets[0].data = [];
            order_product_chart.data.datasets[1].data = [];
            order_product_chart.data.datasets[2].data = [];
            order_product_chart.data.datasets[3].data = [];
            order_product_chart.data.datasets[4].data = [];
            order_product_chart.data.datasets[5].data = [];

            json.data.forEach(element => {
                order_product_chart.data.datasets[0].data.push(element.submitted.total);
                order_product_chart.data.datasets[1].data.push(element.completed.total);
                order_product_chart.data.datasets[2].data.push(-element.cancelled.total);
                order_product_chart.data.datasets[3].data.push(element.submitted.quantity);
                order_product_chart.data.datasets[4].data.push(element.completed.quantity);
                order_product_chart.data.datasets[5].data.push(-element.cancelled.quantity);
            });

            order_product_pie_chart.data.datasets[0].data = [
                json.statistic.submitted.total,
                json.statistic.submitted.store_total-json.statistic.submitted.total,
                json.statistic.completed.total,
                json.statistic.completed.store_total-json.statistic.completed.total,
                json.statistic.cancelled.total,
                json.statistic.cancelled.store_total-json.statistic.cancelled.total,
            ]
            order_product_pie_chart.data.datasets[1].data = [
                json.statistic.submitted.order_count,
                json.statistic.submitted.store_order_count-json.statistic.submitted.order_count,
                json.statistic.completed.order_count,
                json.statistic.completed.store_order_count-json.statistic.completed.order_count,
                json.statistic.cancelled.order_count,
                json.statistic.cancelled.store_order_count-json.statistic.cancelled.order_count,
            ]

            console.log(order_product_chart.data.datasets)

            order_product_chart.update();
            order_product_pie_chart.update();

        },
        error: function(data){
           let json = $.parseJSON(data);
           console.log(json);
        }
    });

}

$("#cmbChartType").on('change',()=>{
    createGraph();
    $("#picker").on('change',()=>{
        updateGraph();
        getStatisticData();
    });
    $("#today-refresh").on('click',() => {
        picker.valueAsDate = new Date(Date.now());
        updateGraph();
        getStatisticData();
    })
    updateGraph();
    getStatisticData();
})



createGraph();

$("#refresh-button").on('click',() => {
    updateGraph();
    getStatisticData();
})

$("#picker").on('change',()=>{
    updateGraph();
    getStatisticData();
});
$("#today-refresh").on('click',() => {
    picker.valueAsDate = new Date(Date.now());
    updateGraph();
    getStatisticData();
})
getStatisticData();
