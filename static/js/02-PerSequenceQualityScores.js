/**
 * Spline Chart Template
 */
function getChart_02(json) {
	//alert(json);
    return {
        title: {
            text: '',

        },
        xAxis: {
        	min:0,
        	title: {
        		text: 'Mean Sequence Quality(Phred Score)'
            },
            plotBands: [{
                from: 2.5,
                to: 3.5,
                color: '#E0E0E0'
            },
            {
                from: 0.5,
                to: 1.5,
                color: '#E0E0E0'
            },
            {
                from: 6.5,
                to: 7.5,
                color: '#E0E0E0'
            },
            {
                from: 8.5,
                to: 9.5,
                color: '#E0E0E0'
            },
            {
                from: 10.5,
                to: 11.5,
                color: '#E0E0E0'
            },
            {
                from: 12.5,
                to: 13.5,
                color: '#E0E0E0'
            },
            {
                from: 14.5,
                to: 15.5,
                color: '#E0E0E0'
            },
            {
                from: 16.5,
                to: 17.5,
                color: '#E0E0E0'
            },
            {
                from: 18.5,
                to: 19.5,
                color: '#E0E0E0'
            },
            {
                from: 20.5,
                to: 21.5,
                color: '#E0E0E0'
            },
            {
                from: 22.5,
                to: 23.5,
                color: '#E0E0E0'
            },
            {
                from: 24.5,
                to: 25.5,
                color: '#E0E0E0'
            },
            {
                from: 26.5,
                to: 27.5,
                color: '#E0E0E0'
            },
            {
                from: 28.5,
                to: 29.5,
                color: '#E0E0E0'
            },
            {
                from: 30.5,
                to: 31.5,
                color: '#E0E0E0'
            },
            {
                from: 32.5,
                to: 33.5,
                color: '#E0E0E0'
            },
            {
                from: 34.5,
                to: 35.5,
                color: '#E0E0E0'
            },
            {
                from: 36.5,
                to: 37.5,
                color: '#E0E0E0'
            },
            {
                from: 4.5,
                to: 5.5,
                color: '#E0E0E0'
            }],
            categories: json.categories
        },
        yAxis: {
        	title: {
                text: ''
            },
            lineColor:'#6C6C6C',
	        lineWidth:2,
            min:0,
            gridLineColor: '#ADADAD',//�����������ɫ
            gridLineDashStyle: 'solid',//�����������ʽ
            gridLineWidth: 2//��������߿��
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
        	color:json.color,
        	name: json.name,
            data: json.data
        }]
    };
}

function convert_to_02(id,url)
{
	//alert(url);
	var obj = new Object();
	obj.name = "Average Quality per read";
	obj.color = "#FF0000";
	obj.data = new Array();
	obj.categories = new Array();
	//alert(obj.name);
	$.get(url, function(data) {
	//alert("hello");
	var unit = data.split("\r\n");
	for (var i = 1; i < unit.length; ++i)
	{
			//alert("hello");
		var x = unit[i].split("\t");
		obj.data[i - 1] = x[1] * 1.0;
		obj.categories[i - 1] = x[0];
	}
	//alert(obj.data);
	//alert(obj.categories);
	var json_str = JSON.stringify(obj); 
	//alert(json_str);
	//document.write(json_str);
	var json = eval('(' + json_str + ')');
	//alert(json.name);
	//alert(json.color);
	//alert(json.data);
	//alert(json.categories);
	$(id).highcharts(getChart_02(json));
	});
}
function createSpline_02(id,url){
	 $.getJSON(url, function(json) {
		 /*alert(json.name);
			alert(json.color);
			alert(json.data);
			alert(json.categories);*/
		 $(id).highcharts(getChart_02(json));
	});
}