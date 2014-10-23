<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<title>Highcharts Example</title>
		<!-- 1. Add these JavaScript inclusions in the head of your page -->
		<script type="text/javascript" src="E:/Jquery/jquery-1.7.2.min.js"></script>
		<script type="text/javascript" src="E:/Highcharts/js/highcharts.js"></script>
		<script type="text/javascript" src="E:/Highcharts/js/modules/exporting.js"></script>
		<script type="text/javascript">
			var chart;
			$(document).ready(function() {
				chart = new Highcharts.Chart({
					chart: {
						renderTo: 'container',
						plotBackgroundColor: null,
						plotBorderWidth: null,
						plotShadow: false
					},
					title: {
						text: 'Browser market shares at a specific website, 2010'
					},
					tooltip: {
						formatter: function() {
							return '<b>'+ this.point.name +'</b>: '+ this.y +' %';
						}
					},
					plotOptions: {
						pie: {
							allowPointSelect: true,
							cursor: 'pointer',
							dataLabels: {
								enabled: false
							},
							showInLegend: true
						}
					},
				    series: [{
						type: 'pie',
						name: 'Browser share',
						data: [
					              ['RNA processing and modification', 26], ['Chromatin structure and dynamics', 24.6], ['Energy production and conversion', 44.2], ['Cell cycle control, cell division', 2.6], ['Amino acid transport and metabolism', 2.1],
									['Nucleotide transport and metabolism',1.9],['Carbohydrate transport and metabolism',2943.68],
						['Coenzyme transport and metabolism',1599.0],
						["Lipid transport and metabolism",857.8],
						['Translation, ribosomal structure and biogenesis',4129.2],
						["Transcription",1793.61],
						["Replication, recombination and repair",3307.43],
						["Cell wall/membrane/envelope biogenesis",2956.17],
						["Cell motility",42.7174],
						["Posttranslational modification, protein turnover, chaperones",1660.83],
						["Inorganic ion transport and metabolism",2003.9],
						["Secondary metabolites biosynthesis, transport and catabolism",449.644],
						["General function prediction only",4901.16],
						["Signal transduction mechanisms",791.628],
						["Intracellular trafficking, secretion, and vesicular transport",803.987],
						["Defense mechanisms",1273.44],
						["Extracellular structures",61.0684713],
						["Cytoskeleton",3.43022],
						["Function unknown",6278.61]]
					}]
				});
			});
				
		</script>
	</head>
	<body>
		
		<!-- 3. Add the container -->
		<div id="container" style="width: 1000px; height: 600px; margin: 0 auto"></div>
	</body>
</html>
