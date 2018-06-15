<html>
<head>
<link rel="stylesheet" type="text/css" href="CSS/skeleton.css?<?php echo time(); ?>" />
</head>
<body>

<?php
	$connectfile = "connect.php";
	require $connectfile;
	$transactionQuery = "INSERT INTO inventory(partNumber, quantity, transactionDate, locationFrom, locationTo, note) VALUES (9010775, 800, '2016-12-31', NULL, 4, NULL)";
	$transactionResult = $conn->query($transactionQuery);
?>

</body>
</html>