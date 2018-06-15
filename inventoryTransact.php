<html>
<head>
	<title>Part Transaction</title>
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

	function valueReturn($query, $column)
	{
		$connectfile = "connect.php";
		require $connectfile;
		$result = $conn->query($query);
		$value = $result->fetch_assoc();
		return $value[$column];
	}

	$partNumber = $_GET["partNumber"];
	$quantity = $_GET["quantity"];
	$invLocationFrom = $_GET["invLocationFrom"];
	$invLocationTo = $_GET["invLocationTo"];
	$transactDate = $_GET["transactDate"];

	if($partNumber != "" && $quantity != "" && $invLocationTo != "" && $transactDate != "" && $invLocationFrom != $invLocationTo){

		$transactionPeriod = 30;
		$recentTransactionListQuery = "SELECT transactionDate, locationFrom, locationTo, quantity FROM inventory WHERE partNumber = ".$partNumber." AND transactionDate BETWEEN DATE_SUB(CURDATE(), INTERVAL ".$transactionPeriod." DAY) AND CURDATE()";
		$recentTransactionListResult = $conn->query($recentTransactionListQuery);

		if($invLocationFrom == ""){
			$invLocationFromCode = "NULL";
		}else{
			$invLocationFromCode = valueReturn("SELECT locationCode FROM inventoryLocation WHERE locationName = ".$invLocationFrom, "locationCode");
		}
		if($invLocationTo == ""){
			$invLocationToCode = "NULL";
		}else{
			$invLocationToCode = valueReturn("SELECT locationCode FROM inventoryLocation WHERE locationName = ".$invLocationTo, "locationCode");
		}

		$transactionQuery = "INSERT INTO inventory(partNumber, quantity, transactionDate, locationFrom, locationTo, note) VALUES (".$partNumber.", ".$quantity.", CURDATE(), ".$invLocationFromCode.", ".$invLocationToCode.", NULL)";
		$transactionResult = $conn->query($transactionQuery);

		echo "<br><br><br>";
		echo "<b>Transaction Processed Successfully:</b><br><br>";

		echo "<table>";
		echo "<tr><td><b>Part Number</b></td><td>".$partNumber."</td></tr>";
		echo "<tr><td><b>Quantity</b></td><td>".$quantity."</td></tr>";
		echo "<tr><td><b>Inventory Location From</b></td><td>".$invLocationFrom."</td></tr>";
		echo "<tr><td><b>Inventory Location To</b></td><td>".$invLocationTo."</td></tr>";
		echo "<tr><td><b>Transaction Date</b></td><td>".$transactDate."</td></tr>";
		echo "</table>";
		echo "<br>";

		if ($recentTransactionListResult->num_rows > 0) {
			echo "<br><br><br><br>";
			echo "<b>Previous ".$transactionPeriod." day transaction history:</b><br><br>";
			echo "<table><th>transaction date</th><th>location from</th><th>location to</th><th>qty</th>";
			echo "<tr>";
	        echo "<td><b>NOW, ".$transactDate."</b></td>";
			echo "<td><b>".$invLocationFrom."</b></td>";
			echo "<td><b>".$invLocationTo."</b></td>";
			echo "<td><b>".$quantity."</b></td>";
	        echo "</tr>";
			while($transaction = $recentTransactionListResult->fetch_row()) {
		        echo "<tr>";
		        echo "<td>".$transaction[0]."</td>";
		        if($transaction[1] == ""){
		        	echo "<td></td>";
		        }else{
		        	echo "<td>".valueReturn("SELECT locationName FROM inventoryLocation WHERE locationCode = ".$transaction[1], "locationName")."</td>";
		        }
				echo "<td>".valueReturn("SELECT locationName FROM inventoryLocation WHERE locationCode = ".$transaction[2], "locationName")."</td>";
				echo "<td>".$transaction[3]."</td>";
		        echo "</tr>";
		    }
			echo "</table>";
		}
		else{
			echo "<br>No transactions in previous ".$transactionPeriod." days";
		}
	}else{

		echo "<br><br><br><br>";
		echo "<FORM METHOD = 'LINK' ACTION = 'inventoryTransact.php'>";
		if($partNumber == ""){
			echo "Part Number: <INPUT TYPE='text' NAME = 'partNumber'><br>";
		}else{
			echo "Part Number: <INPUT TYPE='text' VALUE = ".$partNumber." NAME = 'partNumber'><br>";
		}
		echo "Quantity: <INPUT TYPE='text' NAME = 'quantity'><br>";

		echo "Inventory Location From: <input list='invLocationFromList' name='invLocationFrom'>
		  <datalist id='invLocationFromList'><br>";
		$locationNameQuery = "SELECT locationCode, locationName FROM inventoryLocation";
		$locationNameResult = $conn->query($locationNameQuery);
		if ($locationNameResult->num_rows > 0) {
			while($invLocation = $locationNameResult->fetch_row()) {
				echo "<option value=".$invLocation[1].">";
			}
		}
		echo"</datalist><br>";

		echo "Inventory Location To: <input list='invLocationToList' name='invLocationTo'>
		  <datalist id='invLocationToList'>";
		$locationNameQuery = "SELECT locationCode, locationName FROM inventoryLocation";
		$locationNameResult = $conn->query($locationNameQuery);
		if ($locationNameResult->num_rows > 0) {
			while($invLocation = $locationNameResult->fetch_row()) {
				echo "<option value=".$invLocation[1].">";
			}
		}
		echo"</datalist><br>";

		echo "Date: <INPUT TYPE = 'text' VALUE = ".date("Y-m-d")." NAME = 'transactDate'><br>";
		echo "<br><br><br>";
		echo "<INPUT TYPE='submit' VALUE = 'Transact'></FORM>";
	}
?>
<br><br>

<div id="footer"></div>
</body>
</html>
