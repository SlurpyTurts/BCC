<html>
<head>
<link rel="stylesheet" href="style.css">
</head>
<body>
<?php	
	$servername = "localhost";
	$username = "root";
	$password = "root";
	$dbName = "BCC";

	// Create connection
	$conn = new mysqli($servername, $username, $password);

	// Check connection
	if ($conn->connect_error) {
	    die("Host Connection failed: " . $conn->connect_error). "<br>";
	} 

	else{
		//echo "Host Connection successful". "<br>";

		//connect to BCC DB
		$sql = "USE BCC";
		if ($conn->query($sql) === TRUE) {
			//echo "Connected to BCC database". "<br>";
		} else {
			echo "Error connecting to BCC" . $conn->error. "<br>";
		}
	}
?>

</body>
</html>