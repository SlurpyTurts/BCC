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

	$orderNumber = $_GET["order"];
	$sql =
		"SELECT orderLine.orderNumber, orderLine.dateAdded, orderLine.partNumber, part.description, orderLine.lineQuantity, orderLine.lineDiscount, pricing.dealerNetPrice, (pricing.dealerNetPrice-orderLine.lineDiscount)*orderLine.lineQuantity AS 'lineTotal'
		FROM orderLine
		INNER JOIN part
		ON orderLine.partNumber = part.partNumber
		INNER JOIN pricing
		ON orderLine.partNumber = pricing.partNumber
		WHERE orderLine.orderNumber = ".$orderNumber;
	$result = $conn->query($sql);




	if ($result->num_rows > 0) {


		echo "<br><br>INVOICE LINE ITEMS<br><br>";
		echo "<table>";

/*
        echo "<tr>";
		while($fieldinfo = $result->fetch_field()){
			echo "<td>".$fieldinfo->name."</td>";
		}
		echo "</tr>";
*/


		echo "<tr>";
		while($fieldinfo = $result->fetch_field()){

			$header = "SELECT dealerName from dealerList";
			$headerResult = $conn->query($header);


			echo "<td>".$fieldinfo->name."<br>";

/*
			echo "<select>";


				echo "<option value = 'name'>"."ALL"."</option>";
				while($newrow = $headerResult->fetch_row()) {
			        echo "<option value = 'name'>".$newrow[0]."</option>";
			    }

		    echo "</select>";
*/

			echo "</td>";


		}
		echo "</tr>";






		while($row = $result->fetch_row()) {
	        echo "<tr>";
	        echo "<td>".$row[0]."</td>";
	        echo "<td>".$row[1]."</td>";
	        echo "<td>".$row[2]."</td>";
	        echo "<td>".$row[3]."</td>";
	        echo "<td>".$row[4]."</td>";
	        echo "<td>".$row[5]."</td>";
	        echo "<td>".$row[6]."</td>";
	        echo "<td>".$row[7]."</td>";
	        echo "</tr>";
	    }



	    echo "</table>";
	} else {
	    echo "0 results";
	}


	$sql = "SELECT SUM(pricing.dealerNetPrice)
			FROM orderLine
			INNER JOIN pricing
			ON orderLine.partNumber = pricing.partNumber
			WHERE orderNumber = ".$orderNumber;
	$result = $conn->query($sql);

	echo "<br><br><br>";
	echo "<u>TOTAL INVOICE AMOUNT: <b>$";
	while($row = $result->fetch_row()) {
		echo $row[0];
	}
	echo "</b></u>";





	$sql =
		"SELECT * FROM payment WHERE payment.orderNumber = ".$orderNumber;
	$result = $conn->query($sql);




	if ($result->num_rows > 0) {
		echo "<br><br><br><br>PAYMENTS LIST<br><br>";
		echo "<table>";
		echo "<tr>";
		while($fieldinfo = $result->fetch_field()){
			echo "<td>".$fieldinfo->name."<br>";
			echo "</td>";
		}
		echo "</tr>";
		while($row = $result->fetch_row()) {
	        echo "<tr>";
	        echo "<td>".$row[0]."</td>";
	        echo "<td>".$row[1]."</td>";
	        echo "<td>".$row[2]."</td>";
	        echo "<td>".$row[3]."</td>";
	        echo "<td>".$row[4]."</td>";
	        echo "</tr>";
	    }
	    echo "</table>";
	} else {
	    echo "0 results";
	}

	$sql = "SELECT SUM(payment.amount)
			FROM payment
			WHERE payment.orderNumber = ".$orderNumber;
	$result = $conn->query($sql);


	if ($result->num_rows > 0) {
		echo "<br><br><br>";
		echo "<u>TOTAL INVOICE AMOUNT: <b>$";
		while($row = $result->fetch_row()) {
			echo $row[0];
		}
		echo "</b></u>";
	} else {
	    echo "0 results";
	}
	echo "<br><br>";
	echo "<a href=paymentTransact.php?orderNumber=".$orderNumber.">Make Payment</a>";

?>
<br><br>
<div id="footer"></div>
</body>
</html>
