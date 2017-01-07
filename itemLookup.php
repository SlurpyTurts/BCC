<html>
<head>
	<title>Item Lookup</title>
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

	function bomTable($bomQuery,$level,$maxLevel){
			$connectfile = "connect.php";
			require $connectfile;
			$bomResult = $conn->query($bomQuery);
			while($bom = $bomResult->fetch_row()){
				echo "<tr>";
				echo "<td>".$level."</td>";
				echo '<td><a href=itemLookup.php?partNumber='.$bom[1].'>'.$bom[1].'</td>';
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

	if($partNumber ==""){
		echo "Enter part number";
	}else{

		if(valueReturn("SELECT description FROM part WHERE partNumber = ".$partNumber, "description") == ""){
			echo "Part number ".$partNumber." does not exist";
		}else{

			$bomLevel = 1;
			$maxBomLevel = $_GET["maxBomLevel"];
			if($maxBomLevel == ""){
				$maxBomLevel = 1;
			}
			echo "Part number: <b>".$partNumber."</b>";
			echo "<br>";
			echo "Description: <b>".valueReturn("SELECT description FROM part WHERE partNumber = ".$partNumber, "description")."</b>";
			echo "<br>";
			echo "Unit Price: <b></b>";
			echo "<br><br>";
			echo '<b>Part BOM</b> <a href=bomUpdate.php?partNumber='.$partNumber.'>Edit</a>';



			echo "<FORM METHOD = 'LINK' ACTION = 'itemLookup.php?partNumber='>";
			echo "Parent: <INPUT TYPE='text' VALUE = ".$partNumber." NAME = 'partNumber'><br>";
			echo "BOM Level Depth: <input list='bomLevelList' name='maxBomLevel'>
			  <datalist id='bomLevelList'><br>";
			echo "<option value=0>";
			echo "<option value=1>";
			echo "<option value=2>";
			echo "<option value=3>";
			echo "<option value=4>";
			echo "<option value=5>";
			echo "<option value=6>";
			echo "<option value=7>";
			echo "<option value=8>";
			echo "<option value=9>";
			echo "<option value=10>";
			echo"</datalist><br>";

			echo "<INPUT TYPE='submit' VALUE = 'Update'></FORM>";









			echo "<br><br>";
			echo "<table><th>level</th><th>child</th><th>Description</th><th>quantity</th><th>ref des</th>";
			$bomQuery = "SELECT bom.parent, bom.child, bom.quantity, bom.referenceDesignator, part.description FROM bom INNER JOIN part ON bom.child = part.partNumber WHERE parent = ".$partNumber;
			bomTable($bomQuery,$bomLevel,$maxBomLevel);
			echo "</table>";
			echo "<br><br>";


			$locationNameQuery = "SELECT locationCode, locationName FROM inventoryLocation";
			$locationNameResult = $conn->query($locationNameQuery);


			echo "<b>On-hand Inventory</b>";
			if ($locationNameResult->num_rows > 0) {
				echo "<table><th>location</th><th>quantity</th>";
				while($invLocation = $locationNameResult->fetch_row()) {
			        echo "<tr>";
			        echo "<td>".$invLocation[1]."</td>";



		//inv qty in/out sql lookup queries
					$qtyLookupIn = "SELECT SUM(quantity) FROM inventory WHERE locationTo = ".$invLocation[0]." AND partNumber = ".$partNumber;
					$qtyLookupResultIn = $conn->query($qtyLookupIn);

					$qtyLookupOut = "SELECT SUM(quantity) FROM inventory WHERE locationFrom = ".$invLocation[0]." AND partNumber = ".$partNumber;
					$qtyLookupResultOut = $conn->query($qtyLookupOut);

		//return qty in and out
					if ($qtyLookupResultIn->num_rows > 0) {
						while($qtyIn = $qtyLookupResultIn->fetch_row()) {
					        if($qtyIn[0]==""){
					        	$invIn = 0;
					        }else{
								$invIn = $qtyIn[0];
					        }
					    }
					}

					if ($qtyLookupResultOut->num_rows > 0) {
						while($qtyOut = $qtyLookupResultOut->fetch_row()) {
					        if($qtyOut[0]==""){
					        	$invOut = 0;
					        }else{
								$invOut = $qtyOut[0];
					        }
					    }
					}

					$invCount = $invIn - $invOut;

					echo "<td>".$invCount."</td>";

			        echo "</tr>";
			    }
				echo "</table>";
			}
			else{
				echo "0 results";
			}

			echo "<br><br>";
			echo "<b>Recent transactions </b><a href=inventoryTransact.php?partNumber=".$partNumber.">New Transaction</a>";
			echo "<br><br>";
			$transactionPeriod = 30;
			$recentTransactionListQuery = "SELECT transactionDate, locationFrom, locationTo, quantity FROM inventory WHERE partNumber = ".$partNumber." AND transactionDate BETWEEN DATE_SUB(CURDATE(), INTERVAL ".$transactionPeriod." DAY) AND CURDATE()";
			$recentTransactionListResult = $conn->query($recentTransactionListQuery);
			if ($recentTransactionListResult->num_rows > 0) {
				echo "<table><th>transaction date</th><th>location from</th><th>location to</th><th>qty</th>";
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
			echo "<br><br><b>Where used</b><br><br>";
			$whereUsedQuery = "SELECT bom.parent, part.description FROM bom INNER JOIN part ON part.partNumber = bom.parent WHERE bom.child = ".$partNumber;
			$whereUsedResult = $conn->query($whereUsedQuery);
			echo "<table><th>Part Number</th><th>Description</th>";
			if ($whereUsedResult->num_rows > 0) {
				while($whereUsed = $whereUsedResult->fetch_row()) {
					echo '<tr><td><a href=itemLookup.php?partNumber='.$whereUsed[0].'>'.$whereUsed[0].'</td><td>'.$whereUsed[1].'</td></tr>';
				}
			}
			echo "</table>";
		}
	}
	echo "<br><br>";

?>

<FORM METHOD="LINK" ACTION="itemLookup.php">
<INPUT TYPE="text" name="partNumber">
<INPUT TYPE="submit" VALUE="Look up part">
</FORM>
<br>
<br>

<div id="footer"></div>
</body>
</html>
