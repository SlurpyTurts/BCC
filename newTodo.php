<html>
<head>
	<title>Order Overview</title>
	<script src="//code.jquery.com/jquery-1.10.2.js"></script>
	<script>
		$(function(){
			$("#header").load("header.html");
			$("#footer").load("footer.html");
      $("#todo").load("todo.php");
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
  <div id="header"></div>
  <div id="todo"></div>

  <?php
  //connect to DB

  	$connectfile = "connect.php";
  	require $connectfile;

    echo "BOOOSHHHH";

    echo "<FORM METHOD = 'LINK' ACTION = 'todo.php'>";
    echo "Category <input list='invLocationFromList' name='invLocationFrom'>
		  <datalist id='invLocationFromList'><br>";
		$locationNameQuery = "SELECT locationCode, locationName FROM inventoryLocation";
		$locationNameResult = $conn->query($locationNameQuery);
		if ($locationNameResult->num_rows > 0) {
			while($invLocation = $locationNameResult->fetch_row()) {
				echo "<option value=".$invLocation[1].">";
			}
		}
		echo"</datalist><br>";
    echo "New Part Number: <INPUT TYPE='text' NAME = 'newPart'><br>";
    echo "Quantity: <INPUT TYPE='text' NAME = 'quantity'><br>";
    echo "Reference Designator: <INPUT TYPE='text' NAME = 'refDes'><br>";
    echo '<INPUT TYPE="submit" VALUE="Update"></FORM>';



  ?>
  <div id="footer"></div>

</body>
</html>
