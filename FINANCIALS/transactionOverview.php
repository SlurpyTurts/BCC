<html>
<head>
<link rel="stylesheet" type="text/css" href="CSS/skeleton.css?<?php echo time(); ?>" />
</head>
<body>

<?php
//connect to DB

	$connectfile = "./../connect.php";
	require $connectfile;

//query DB
	$db = "BCC";
	$sql = "SHOW TABLES FROM ".$db;
	$result = $conn->query($sql);

//check for data, populate
	if ($result->num_rows > 0) {
		//populate field list array
		$columnList = array();
		while($row = $result->fetch_assoc()) {
			$columnList[] = $row['Tables_in_bcc'];
			//echo $row['Tables_in_bcc']."<br>";

			
		}
//print field list array values
		for($x = 0; $x < count($columnList); $x++){
			//echo $x."<br>";
			//print($columnList[$x])."<br>\n";
			echo "<a href=".'tableView.php?table='.$columnList[$x].">".$columnList[$x]."</a><br>\n";

		}
/*
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
*/
	} else {
		echo "0 results";
	}

	$conn->close();
?>

<FORM METHOD="LINK" ACTION="tran.php">
<INPUT TYPE="submit" VALUE="Return Home">
</FORM>

</body>
</html>