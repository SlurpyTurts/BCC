<html>
<head>
	<title>BCC Dealer List</title>
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

	$connectfile = "connect.php";
	require $connectfile;

	$list = $_GET["list"];

	if($list == ""){
		$dealerListQuery = "SELECT * FROM dealerList WHERE status = 'ACTIVE'";
		echo "<a href='dealerList.php?list=all'>View all dealers</a><br><br>";
	}else if($list == "all"){
		$dealerListQuery = "SELECT * FROM dealerList";
		echo "<a href='dealerList.php'>View active dealers</a><br><br>";
	}else{
		$dealerListQuery = "SELECT * FROM dealerList";
	}

	$dealerListResult = $conn->query($dealerListQuery);

	if ($dealerListResult->num_rows > 0) {
		echo "<table>";
		echo "<th>Dealer ID</th>";
		echo "<th>Dealer Name</th>";
		echo "<th>City</th>";
		echo "<th>State/Province</th>";
		echo "<th>Country</th>";
		while($dealerList = $dealerListResult->fetch_row()) {
			echo "<tr>";
			echo "<td>".$dealerList[0]."</td>";
			echo "<td><a href=".'orderLookup.php?dealer='.$dealerList[0].">".$dealerList[1]."</a></td>";
			echo "<td>".$dealerList[11]."</td>";
			echo "<td>".$dealerList[12]."</td>";
			echo "<td>".$dealerList[13]."</td>";
			echo "</tr>";
		}
		echo "</table>";
	}

?>

<div id="footer"></div>
</body>
</html>
