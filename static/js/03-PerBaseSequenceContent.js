function getChart_03(s) {
	//alert(s.categories);
    return {
        title: {
	            text: '',
	            align: 'center',
	            style:{
	            	fontSize: '13px',
	            	fontWeight: 'lighter'
	            	}
	        },
	        xAxis: {
	        	title: {
	        		text: 'Position in read(bp)'
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
	            categories:s.categories
	        },
	        yAxis: {
	        	lineColor:'#6C6C6C',
		        lineWidth:2,
	            min:0,
	            gridLineColor: '#ADADAD',
	            gridLineDashStyle: 'solid',
	            gridLineWidth: 2,
	        	max:100,
	            title: {
	                text: ''
	            },
	            plotLines: [{
	                value: 0,
	                width: 1,
	                color: '#808080'
	            }]
	        },
	        legend: {
	            layout: 'vertical',
	            align: 'right',
	            verticalAlign: 'middle',
	            borderWidth: 0
	        },
	        series: s.series
    };
}
function convert_to_03(id,url)
{
	$.get(url, function(data) {
		var name = new Array();
		var str = new String();
		str = "{\"categories\":[";
		var categories = new Array();
		var unit = data.split("\r\n");
		var x1 = unit[0].split("\t");
		for (var i = 1; i < x1.length; ++i)
		{
			name[i - 1] = x1[i];
			//alert(name[i - 1]);
		}
		
		for (var i = 1; i < unit.length; ++i)
		{
			var x = unit[i].split("\t");
			str += "\"" + x[0] + "\"";
			if (i != unit.length - 1) str += ",";
			else str += "],\"series\": [{";
		}
		//alert(unit.length);
		for (var j = 1; j < x1.length; j++)
		{
			str += "\"name\":\"%" + name[j - 1] + "\",\"data\": [";
			for (var i = 1; i < unit.length; ++i)
			{
				var x = unit[i].split("\t");
				str += x[j];
				if (i != unit.length - 1) str += ",";
				else str += "]";
			}
			if (j != x1.length - 1) str += "}, {";
			else str += "}]}";
		}
		//document.write(str);
		var s = eval("("+str+")");
		//alert("hello");
		//document.write(s);
		$(id).highcharts(getChart_03(s));
	});
}

function createSpline_03(id,url){
		//alert("hello");
	 $.getJSON(url, function(json) {
		 $(id).highcharts(getChart_03(json));
	});
}