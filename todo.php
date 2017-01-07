<html>
<head>
	<title>Order Overview</title>
	<script src="//code.jquery.com/jquery-1.10.2.js"></script>
	<script>
		$(function(){
			$("#header").load("header.html");
			$("#footer").load("footer.html");
		});
	</script>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
	<script>
		$(document).ready(function(){
		    $("#hide").click(function(){
		        $("p").hide();
		    });
		    $("#show").click(function(){
		        $("p").show();
		    });
		});
	</script>
</head>
<body>
<?php
//connect to DB

	$connectfile = "connect.php";
	require $connectfile;

  $todoQuery = "SELECT * FROM todo ORDER BY dateCompleted DESC, dateAdded ASC";
  $todoResult = $conn->query($todoQuery);

  if($todoResult->num_rows > 0){
    echo "<table>";
    echo "<th>Description</th><th>Date Added</th><th>Date Completed</th>";
    while($todo = $todoResult->fetch_row()){
      echo "<tr><td>".$todo[1]."</td><td>".$todo[2]."</td><td>".$todo[3]."</td></tr>";
    }
    echo "</table>";

    echo "<a href='dealerInfoEdit.php'></a>";

  }
?>

</body>
</html>
