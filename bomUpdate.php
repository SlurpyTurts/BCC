<html>
<head>
	<title>BCC BOM Update</title>
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
<script>
function myFunction() {
    var person = prompt("Please enter your name", "partNumber");

    if (person != null) {
        document.getElementById("demo").innerHTML =
        "Hello " + person + "! How are you today?";
    }
}
</script>

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
			echo "<td>";
			echo "<button onclick='myFunction()'>edit</button>";
			echo "</td>";
			echo "</tr>";
			$subBomQuery = "SELECT bom.parent, bom.child, bom.quantity, bom.referenceDesignator, part.description FROM bom INNER JOIN part ON bom.child = part.partNumber WHERE parent = ".$bom[1];
			if($level < $maxLevel){
				bomTable($subBomQuery,$level+1,$maxLevel);
			}
		}
	}


	$partNumber = $_GET["partNumber"];
	$newPart = $_GET["newPart"];
	$quantity = $_GET["quantity"];
	$refDes = $_GET["refDes"];
	$bomLevel = 0;
	if($partNumber == ""){
		echo "No valid part number";
	}else{
		if($newPart == "" || $quantity == ""){
			echo "Part Number: <b>".$partNumber."</b><br><br>";
			echo "<table><th>level</th><th>child</th><th>Description</th><th>quantity</th><th>ref des</th><th></th>";
			$bomQuery = "SELECT bom.parent, bom.child, bom.quantity, bom.referenceDesignator, part.description FROM bom INNER JOIN part ON bom.child = part.partNumber WHERE parent = ".$partNumber;
			bomTable($bomQuery,0,10);
			echo "</table>";

			echo "<FORM METHOD = 'LINK' ACTION = 'bomUpdate.php'>";
			echo "Parent part: <INPUT TYPE='text' VALUE = ".$partNumber." NAME = 'partNumber'><br>";
			echo "New Part Number: <INPUT TYPE='text' NAME = 'newPart'><br>";
			echo "Quantity: <INPUT TYPE='text' NAME = 'quantity'><br>";
			echo "Reference Designator: <INPUT TYPE='text' NAME = 'refDes'><br>";
			echo '<INPUT TYPE="submit" VALUE="Update"></FORM>';



		}else{
			if($refDes == ""){
				$refDes = "NULL";
			}
			$bomUpdateQuery = "INSERT INTO bom(parent, child, quantity, referenceDesignator) VALUES (".$partNumber.", ".$newPart.", ".$quantity.", ".$refDes.")";
			$bomUpdateResult = $conn->query($bomUpdateQuery);
			echo "Update Successful on Part <b>".$partNumber."</b>";
		}
	}

?>

<div id="footer"></div>
</body>
</html>
