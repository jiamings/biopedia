<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en">
<head>
  <script type="text/javascript" src="http://cdn.hcharts.cn/jquery/jquery-1.8.3.min.js"></script>
  <script type="text/javascript" src="http://cdn.hcharts.cn/highcharts/highcharts.js"></script>
  <!--<script type="text/javascript" src="js/themes/aa.js"></script>-->
  <script type="text/javascript" src="http://cdn.hcharts.cn/highcharts/exporting.js"></script>
  <script>
  $(function () {
	    $('#container').highcharts({
	        title: {
	            text: 'Quality score distribution over all sequences',
	            x: -20 //center
	        },
	        xAxis: {
	        	title: {
	        		text: 'Mean Sequence Quality(Phred Score)'
	            },

	            categories: ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40'
	                         ]
	        },
	        yAxis: {
	        	title: {
	                text: ''
	            },
	           plotLines: [{
	                value: 0,
	                width: 1,
	                color: '#808080'
	            }]
	        },
	        tooltip: {
	            valueSuffix: '°C'
	        },
	        legend: {
	            layout: 'vertical',
	            align: 'right',
	            verticalAlign: 'middle',
	            borderWidth: 0
	        },
	        series: [{
	        	color:"#FF0000",
	        	name: 'Average Quality per read',
	            data: [5916, 180, 188, 353, 580, 1376, 3492, 7962, 14928, 22318, 27295, 30884, 32885, 34577, 36820, 38649, 40405, 42778, 46582, 51187, 56817, 66321, 80409, 102112, 132669, 172259, 223414, 287883, 364467, 459410, 583986, 766136, 1.08709e+006, 1.85099e+006, 3.94424e+006, 8.251e+006, 1.73338e+007, 1.77179e+007, 1.35221e+006]
	        }]
	    });
	});
  </script>
</head>
<body>
  <div id="container" style="min-width:700px;height:400px"></div>
</body>
</html>
