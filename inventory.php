<html>
<head>
	<title>BCC Inventory Overview</title>
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

	$partNumberListQuery = "SELECT partNumber FROM part";
	$partNumberListResult = $conn->query($partNumberListQuery);


	if ($partNumberListResult->num_rows > 0) {
		echo "<table><th>Part Number</th><th>Description</th>";

		$invLocationQuery = "SELECT locationCode, locationName FROM inventoryLocation";
		$invLocationResult = $conn->query($invLocationQuery);
		if ($invLocationResult->num_rows > 0) {
			while($invLocation = $invLocationResult->fetch_row()) {
		        echo "<th>".$invLocation[1]."</th>";
		    }
		}

		echo "<th>Total On Hand</th>";

		while($partNumber = $partNumberListResult->fetch_row()) {
	      echo "<tr>";
				echo "<td>";
				echo "<a href=".'itemLookup.php?partNumber='.$partNumber[0].">".$partNumber[0];
				echo "</td>";

				$partDescription = valueReturn("SELECT description FROM part WHERE partNumber = ".$partNumber[0], description);
				echo "<td>".$partDescription."</td>";

	        $invLocationQuery = "SELECT locationCode FROM inventoryLocation";
			$invLocationResult = $conn->query($invLocationQuery);
			if ($invLocationResult->num_rows > 0) {
				while($invLocation = $invLocationResult->fetch_row()) {



			        $qtyLookupInQuery = "SELECT SUM(quantity) FROM inventory WHERE locationTo = ".$invLocation[0]." AND partNumber = ".$partNumber[0];
					$qtyLookupInResult = $conn->query($qtyLookupInQuery);
					if ($qtyLookupInResult->num_rows > 0) {
						while($qtyLookupIn = $qtyLookupInResult->fetch_row()) {
					        if($qtyLookupIn[0] == ""){
					        	$invIn = 0;
					        }else{
					        	$invIn = $qtyLookupIn[0];
					    	}
					    }
					}

					$qtyLookupOutQuery = "SELECT SUM(quantity) FROM inventory WHERE locationFrom = ".$invLocation[0]." AND partNumber = ".$partNumber[0];
					$qtyLookupOutResult = $conn->query($qtyLookupOutQuery);
					if ($qtyLookupOutResult->num_rows > 0) {
						while($qtyLookupOut = $qtyLookupOutResult->fetch_row()) {
					        if($qtyLookupOut[0] == ""){
					        	$invOut = 0;
					        }else{
					        	$invOut = $qtyLookupOut[0];
					    	}
					    }
					}



					if($invIn == 0 && $invOut == 0){
						$invNet = "";
					}else{
						$invNet = $invIn - $invOut;
					}
					echo "<td>".$invNet."</td>";




			    }
			}


//inv qty in/out sql lookup queries
			$qtyLookupInQuery = "SELECT SUM(quantity) FROM inventory WHERE locationTo != 6 AND partNumber = ".$partNumber[0];
			$qtyLookupInResult = $conn->query($qtyLookupInQuery);

			if ($qtyLookupInResult->num_rows > 0) {
				while($qtyTotalIn = $qtyLookupInResult->fetch_row()) {
			        if($qtyTotalIn[0] == ""){
			        	$invIn = 0;
			        }
			        else{
			        	$invIn = $qtyTotalIn[0];
			        }
			    }
			}

			$qtyLookupOutQuery = "SELECT SUM(quantity) FROM inventory WHERE locationFrom != 6 AND partNumber = ".$partNumber[0];
			$qtyLookupOutResult = $conn->query($qtyLookupOutQuery);

			if ($qtyLookupOutResult->num_rows > 0) {
				while($qtyTotalOut = $qtyLookupOutResult->fetch_row()) {
			        if($qtyTotalOut[0] == ""){
			        	$invOut = 0;
			        }
			        else{
			        	$invOut = $qtyTotalOut[0];
			        }
			    }
			}

			$invTotal = $invIn - $invOut;
			echo "<td>".$invTotal."</td>";

	        echo "</tr>";
	    }
		echo "</table>";
	}
	else{
		echo "0 results";
	}





?>
<div id="footer"></div>
</body>
</html>
