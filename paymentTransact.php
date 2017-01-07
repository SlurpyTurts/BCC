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
	echo "<b>Order number ".$orderNumber."</b>";
	echo "<br><br><br>";
	echo "<FORM METHOD = 'LINK' ACTION = 'paymentConfirmation.php'> ";
	if($orderNumber == ""){
		echo "Order Number: <INPUT TYPE='text' NAME = 'orderNumber'> ";
	}else{
		echo "Order Number: <INPUT TYPE='text' VALUE = ".$orderNumber." NAME = 'orderNumber'> ";
	}
	echo "Amount: <INPUT TYPE='text' NAME = 'amount'> ";
	echo "Payment Method: <INPUT TYPE='text' NAME = 'method'> ";
	echo "Reference: <INPUT TYPE='text' NAME = 'reference'><br><br>";
	echo "<INPUT TYPE='submit' VALUE = 'Submit'></FORM>";

?>

<div id="footer"></div>
</body>
</html>
