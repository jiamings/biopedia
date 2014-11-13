/**
 * Spline Chart Template
 */
function getChart_01(json) {
	//alert(json);
    return {
    	   title: {
               text: ''
           },

           legend: {
               enabled: false
           },

           xAxis: {
        	   min:0,
        	   lineColor:'#000000',
               categories: json.categories,
               title: {
                   text: 'Position in read(bp).'
               },
               gridLineColor:"RGB(207,205,210)",
               gridLineWidth:15
           },

           yAxis: {
        	   min:0,
        	   max:50,
               title: {
                   text: ''
               },
               plotBands: [{
                   from: 0,
                   to: 20,
                   color: "RGB(234,125,162)"
               },
               {
                   from: 20,
                   to: 28,
                   color: 'RGB(228,215,117)'
               },
               {
                   from: 28,
                   to: 50,
                   //borderColor:"FF0000",
                   //borderWidth:100
                   color: 'RGB(143,230,140)'
               }],
               lineColor:'#000000',
   	        	lineWidth:1,
   	        	startOnTick:true,
   	        	//minorTickInterval: 'auto',//
   	         //tickmarkPlacement: 'between',
   	        	//tickPixelInterval:10,
                //tickColor:"000000",
               plotLines: [{
                   value: 35,
                   /*color: 'red',*/
                   width: 1,
                   label: {
                       /*text: 'Theoretical mean: 932',*/
                       align: 'center',
                       style: {
                           color: 'gray'
                       }
                   }
               }]
           },
          

           series: [{
               type:'boxplot',
               name: 'Observations',
               color:"#000000",
               lineWidth:0.5,
               fillColor:"RGB(255,255,0)",
               data: json.data,
               tooltip: {
                   headerFormat: '<em>Experiment No {point.key}</em><br/>'
               }
           },  
                    
                    {
               type: 'spline',
               name: 'mean',
               lineWidth: 0.5,
               color:"#0000C6",
               data: json.mean
           },
                    
                    {
               name: 'Outlier',
               color: Highcharts.getOptions().colors[0],
               type: 'scatter',
               data: [ // x, y positions where 0 is the first category
                   [0, 644],
                   [4, 718],
                   [4, 951],
                   [4, 969]
               ],
               marker: {
                   fillColor: 'white',
                   lineWidth: 1,
                   lineColor: Highcharts.getOptions().colors[0]
               },
               tooltip: {
                   pointFormat: 'Observation: {point.y}'
               }
           }]
    };
}

function convert_to_01(id,url)
{
	//alert(url);
	$.get(url, function(data) {
		var str = new String();
		str = "{\"categories\":[";
		var unit = data.split("\r\n");
		
		for (var i = 1; i < unit.length; ++i)
		{
			var x = unit[i].split("\t");
			str += "\"" + x[0] + "\"";
			if (i != unit.length - 1) str += ",";
			else str += "],";
		}
		str += "\"mean\":[";
		for (var i = 1; i < unit.length; ++i)
		{
			var x = unit[i].split("\t");
			str +=  x[1];
			if (i != unit.length - 1) str += ",";
			else str += "],";
		}
		//alert(str);
		var num = [5,3,2,4,6];
		//alert (num[0]);
		str += "\"data\": [";
		for (var i = 1; i < unit.length; ++i)
		{
			str += "[";
			for (var j = 0; j < 5; j++)
			{
				var x = unit[i].split("\t");
				str += x[num[j]];
				if (j != 4) str += ",";
				else str += "]";
			}
			if (i != unit.length - 1) str += ",";
		}
		str += "]}";
		//document.write(str);
		var s = eval("("+str+")");
		//alert("hello");
		//document.write(s);
		$(id).highcharts(getChart_01(s));
	});
}
function createSpline_01(id,url){
	 $.getJSON(url, function(json) {
		 /*alert(json.name);
			alert(json.color);
			alert(json.data);
			alert(json.categories);*/
		 $(id).highcharts(getChart_01(json));
	});
}