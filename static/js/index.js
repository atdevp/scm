var csrftoken = getCookie('csrftoken');

// 统计主机状况 图一
function show_host_info(series, drilldown_series){
    Highcharts.chart('image1', {
        chart: {
            type: 'column'
        },
        title: {
            text: '服务器统计'
        },
        xAxis: {
            type: 'category'
        },
        yAxis: {
            title: {
                text: '个数'
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    //format: '{point.y:.1f}'
                }
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.1f}</b> of total<br/>'
        },
        series: image1_series,
        drilldown: {
            series: drilldown_series,
        }
    });
}

// 展示业务详情(项目&集群) 图一
function show_bussiness_details(series, drilldown_series){
    Highcharts.chart('image2', {
        chart: {
            type: 'column'
        },
        title: {
            text: '项目&集群'
        },
        xAxis: {
            type: 'category'
        },
        yAxis: {
            title: {
                text: '个数'
            }
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    //format: '{point.y:.1f}'
                }
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.1f}</b> of total<br/>'
        },
        series: series,
        drilldown: {
            series: drilldown_series,
        }
    });
};

// 展示整体发布状况 图三
function show_total_deploy_info(xAxis, series){
    $('#image3').highcharts({
        chart:{
            type: 'line'
        },
        title:{
            text: '整体发布'
        },
        xAxis:{
            categories: xAxis
        },
        yAxis:{
            title:{
                text:'次数'
            }
        },
        plotOptions:{
            line:{
                dataLables:{
                    enabled:true
                },
                enableMouseTracking: false
            }
        },
        series: series,
        // series:[{
        //     name: '总体发布',
        //     data: [1.0,8.0,23.0,34.0,34.2,45.0,23.9,4.9,29.0,89.0,27.9,45.9]
        // }]
    })
}

// 展示业务分布占比状况(图4)
function show_business_distrbuted_info(series){
    Highcharts.getOptions().colors = Highcharts.map(Highcharts.getOptions().colors, function (color) {
        return {
            radialGradient: { cx: 0.5, cy: 0.3, r: 0.7 },
            stops: [
                [0, color],
                [1, Highcharts.Color(color).brighten(-0.3).get('rgb')] // darken
            ]
        };
    });
    // 构建图表
    $('#image4').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false
        },
        title: {
            text: '线上、测试服务分布占比'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    },
                    connectorColor: 'silver'
                }
            }
        },
        series: [{
            type: 'pie',
            name: '环境: ',
            data: series
        }]
    });
}

// 请求index接口
// $(function(){
//     cur_url = window.location.pathname
//     if (cur_url == "/"){
//         $.ajax({
//             url: '/api/index',
//             type: 'get',
//             dataType: 'json',
//             async: false,
//             headers: {
//                 "X-CSRFToken": csrftoken,
//                 "Content-Type": "application/json"
//             },
//             success:function(data, textStatus, xhr){
//                 image1_series = data.image1_series
//                 image1_drilldown_series = data.image1_drilldown_series
//                 image2_series = data.image2_series
//                 image2_drilldown_series = data.image2_drilldown_series
//                 image4_series = data.image4_series
//                 image3_xAxis = data.image3_xAxis
//                 image3_series = data.image3_series
//                 show_host_info(image1_series, image1_drilldown_series)
//                 show_bussiness_details(image2_series, image2_drilldown_series)
//                 show_total_deploy_info(image3_xAxis, image3_series)
//                 show_business_distrbuted_info(image4_series)
//             },
//             error:function(data, textStatus, xhr){
//                 show_business_distrbuted_info([])
//             }
//         })
//     }
// })
// End