<html>
<head>
	<title>BCC BOM</title>
	<script src="//code.jquery.com/jquery-1.10.2.js"></script>
	<script>
		$(function(){
			$("#header").load("header.html");
			$("#footer").load("footer.html");
		});
	</script>
</head>
<body>
<div id="header"></div>
<?php
//connect to DB

	$connectfile = "connect.php";
	require $connectfile;

	function bomTable($bomQuery,$level,$maxLevel){
		$connectfile = "connect.php";
		require $connectfile;
		$bomResult = $conn->query($bomQuery);
		while($bom = $bomResult->fetch_row()){
			echo "<tr>";
			echo "<td>".$level."</td>";
			echo "<td>".$bom[0]."</td>";
			//echo "<td>".$bom[1]."</td>";
			echo "<td>".$bom[4]."</td>";
			echo "<td>".$bom[2]."</td>";
			echo "<td>".$bom[3]."</td>";
			echo "</tr>";
			$subBomQuery = "SELECT bom.parent, bom.child, bom.quantity, bom.referenceDesignator, part.description FROM bom INNER JOIN part ON bom.child = part.partNumber WHERE parent = ".$bom[1];
			if($level < $maxLevel){
				bomTable($subBomQuery,$level+1,$maxLevel);
			}
		}
	}


	$partNumber = $_GET["partNumber"];
	$bomLevel = 0;
	if($partNumber == ""){
		echo "Invalid Part Number<br><br>";
		echo "<FORM METHOD = 'LINK' ACTION = 'bom.php?partNumber='>";
		echo "Part Number: <INPUT TYPE='text' NAME = 'partNumber'><br>";
		echo "<INPUT TYPE='submit' VALUE = 'Look Up'></FORM>";
	}else{
		echo "Part Number: <b>".$partNumber."</b><br><br>";
		echo "<table><th>level</th><th>child</th><th>Description</th><th>quantity</th><th>ref des</th>";
		$bomQuery = "SELECT bom.parent, bom.child, bom.quantity, bom.referenceDesignator, part.description FROM bom INNER JOIN part ON bom.child = part.partNumber WHERE parent = ".$partNumber;
		bomTable($bomQuery,0,10);
		echo "</table>";
	}

?>

<div id="footer"></div>
</body>
</html>
