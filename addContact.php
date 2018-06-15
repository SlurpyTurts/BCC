<html>
<head>
	<title>BCC Dealer List </title>
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

	echo "poopy dicks!";

?>

<div id="footer"></div>
</body>
</html>
