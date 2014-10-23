<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>

<title>JSChart</title>
<script type="text/javascript" src="E:/JSChart/sources/jscharts.js"></script>

</head>
<body>

<div id="graph" >Loading graph...</div>

<script type="text/javascript">
	var myData = new Array(['RNA processing and modification', 26], ['Chromatin structure and dynamics', 24.6], ['Energy production and conversion', 44.2], ['Cell cycle control, cell division', 2.6], ['Amino acid transport and metabolism', 2.1],
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
	["Function unknown",6278.61]
	);
	var colors = ['#FF0000', '#E800E8', '#FDB45C', '#0080FF', '#4D5360',
	              '#006030','#D26900','#4A4AFF','#EAC100','#FF359A',
	              "#02F78E","#408080","#984B4B","#7373B9","#0080FF",
	              "#FFFF37","#00EC00","#5B00AE","#FF0000","#FF8000",
	              "#00DB00","#949FB1","#949FB1","#FF00FF"
	              ];
	var myChart = new JSChart('graph', 'pie');
	myChart.setDataArray(myData);
	myChart.colorizePie(colors);
	myChart.setTitle('W3schools browser statistics in August 2008 (%)');
	myChart.setTitleColor('#8E8E8E');
	myChart.setTitleFontSize(11);
	myChart.setTextPaddingTop(280);
	myChart.setPieValuesDecimals(1);
	myChart.setPieUnitsFontSize(9);
	myChart.setPieValuesFontSize(8);
	myChart.setPieValuesColor('#fff');
	myChart.setPieUnitsColor('#969696');
	myChart.setSize(616, 321);
	myChart.setPiePosition(308, 145);
	myChart.setPieRadius(95);
	myChart.setFlagColor('#fff');
	myChart.setFlagRadius(4);
	myChart.setTooltip(['Firefox','Including Mozilla and all Gecko browsers']);
	myChart.setTooltip(['IE6','Including IE5 and older browsers']);
	myChart.setTooltipOpacity(1);
	myChart.setTooltipBackground('#ddf');
	myChart.setTooltipPosition('ne');
	myChart.setTooltipOffset(2);
	myChart.setBackgroundImage('chart_bg.jpg');
	myChart.draw();
</script>

</body>
</html>