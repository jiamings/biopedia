/**
 * Spline Chart Template
 */
function getChart_06(json) {
	//alert(json);
    return {
    	chart: {
			renderTo: 'chart6',
			plotBackgroundColor: null,
			plotBorderWidth: null,
			plotShadow: false,
			plotBackgroundImage: "static/images/background.jpg"
		},
		title: {
			text: json.name
		},
		tooltip: {
			formatter: function() {
				return  '<b>'+ this.point.name +'</b>';
			}
		
		},
		legend: {
			layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: 90,
            y: 45
        },
        
		plotOptions: {
			pie: {
				allowPointSelect: true,
				cursor: 'pointer',
				dataLabels: 
				{
					enabled: false
				},
				showInLegend: true
			}
		},
	    series: [{
			type: 'pie',
			name: 'Browser share',
            dataLabels: {
                enabled: true,
                overflow:true,
                formatter: function() {
                    return Highcharts.numberFormat(this.percentage,1) +' %';
                }
            },
			data:json.data		
			}]
    };
}

function convert_to_06(id,url)
{
	//alert(url);
	$.get(url, function(data) {
		//alert(url);
	var unit = data.split("\r\n");
	var x1 = unit[0].split("\t");
	var str = new String();
	str += "{\"name\":\"" + "" + "\",\"data\":[";
	//document.write(str);
	for (var i = 1; i < unit.length; ++i)
	{
			//alert("hello");
		var x = unit[i].split("\t");
		str += "[\"" + x[0] + "\"," + x[1] + "]";	
		if (i != unit.length - 1) str += ",";
	}
	str += "]}";
	//document.write(str);
	var json = eval("("+str+")");
	$(document).ready(function() {new Highcharts.Chart(getChart_06(json));});
	});
}
function createPie_06(id,url){
	//alert("hello");
	 $.getJSON(url, function(json) {
		 //alert(json.name);
		 $(document).ready(function() {new Highcharts.Chart(getChart_06(json));});
	});
}