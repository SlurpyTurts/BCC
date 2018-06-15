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

	$orderNumber = $_GET["orderNumber"];
	$amount = $_GET["amount"];
	$method = $_GET["method"];
	$reference = $_GET["reference"];

	if($orderNumber != "" && $amount != "" && $method != ""){
		$paymentQuery = "INSERT INTO payment(dateAdded, amount, orderNumber, method, reference) VALUES(CURDATE(),".$amount.", ".$orderNumber.", ".$method.", ".$reference.")";
		$paymentResult = $conn->query($paymentQuery);
		//echo $paymentQuery."<br>";
		echo "Payment confirmed:";
		echo "<br><br>";
		echo "Order Number <b>".$orderNumber."</b>";
		echo "<br>";
		echo "Amount: <b>$".$amount."</b>";
		echo "<br>";
		echo "Payment method: <b>".$method."</b>";
		echo "<br>";
		echo "payment reference: <b>".$reference."</b>";
	}else{
		echo "Insufficient info";
		echo "<br><br>";

		echo "<FORM METHOD = 'LINK' ACTION = 'paymentTransact.php?orderNumber=".$orderNumber."'> ";
		echo "<INPUT TYPE='submit' VALUE = 'Go back'></FORM>";
	}

?>

<div id="footer"></div>
</body>
</html>
