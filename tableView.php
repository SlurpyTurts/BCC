<html>
<head>
<link rel="stylesheet" type="text/css" href="CSS/skeleton.css?<?php echo time(); ?>" />
</head>
<body>

<?php
//connect to DB

	$connectfile = "connect.php";
	require $connectfile;

//query DB
	$table = $_GET["table"];
	$sql = "SHOW COLUMNS FROM ".$table;
	$result = $conn->query($sql);

//check for data, populate
	if ($result->num_rows > 0) {
		//populate field list array
		$columnList = array();
		while($row = $result->fetch_assoc()) {
			$columnList[] = $row['Field'];
			//echo $row['Field']."<br>";

			
		}
//print field list array values
/*		for($x = 0; $x < count($columnList); $x++){
			//echo $x."<br>";
			print($columnList[$x])."<br>\n";

		}
*/
		$sql = "SELECT * FROM ".$table;
		$result = $conn->query($sql);

		
		echo '<table>';

		//data output loop
		for($x = 0; $x < count($columnList); $x++){
			//echo $x."<br>";
			//print($columnList[$x])."<br>\n";
			echo "<td>".$columnList[$x]."</td>";

		}

		while($row = $result->fetch_assoc()) {
			//output data row

			echo "<tr>";

			for($x = 0; $x < count($columnList); $x++){
				//echo $x."<br>";
				//print($columnList[$x])."<br>\n";
				echo "<td>".$row[$columnList[$x]]."</td>";

			}

			echo "</tr>";
		}
		echo "</table>";

	} else {
		echo "0 results";
	}

	$conn->close();
?>

<FORM METHOD="LINK" ACTION="parent.php">
<INPUT TYPE="submit" VALUE="Return Home">
</FORM>

</body>
</html>