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
<div id="header"></div>
<?php
//connect to DB

	$connectfile = "connect.php";
	require $connectfile;

	$dealer = $_GET["dealer"];

	if($dealer == ""){
		$sql =
			"SELECT orderOverview.number AS 'Order Number', dealerList.dealerName AS 'Dealer', CONCAT(contact.firstName, ' ', contact.lastName) AS 'Customer', orderOverview.orderDate AS 'Order Date', orderOverview.invoiceSentDate AS 'Invoice Sent', orderOverview.invoiceStatus AS 'Invoice Status', terms.description AS 'Description', SUM(payment.amount) AS 'Amount Paid'
			FROM (payment
			INNER JOIN orderOverview
			ON payment.orderNumber = orderOverview.number
			LEFT JOIN dealerList
			ON orderOverview.dealerid = dealerList.id
			LEFT JOIN contact
			ON orderOverview.customerid = contact.id
			LEFT JOIN terms
			ON orderOverview.termsid = terms.id)
			GROUP BY orderOverview.number
			HAVING SUM(payment.amount) > 0";
	}else{
		$dealerContactQuery = "SELECT * FROM dealerList WHERE id = ".$dealer;
		$dealerContactResult = $conn->query($dealerContactQuery);
		$sql =
		"SELECT orderOverview.number AS 'Order Number', dealerList.dealerName AS 'Dealer', CONCAT(contact.firstName, ' ', contact.lastName) AS 'Customer', orderOverview.orderDate AS 'Order Date', orderOverview.invoiceSentDate AS 'Invoice Sent', orderOverview.invoiceStatus AS 'Invoice Status', terms.description AS 'Description', SUM(payment.amount) AS 'Amount Paid'
		FROM (payment
		INNER JOIN orderOverview
		ON payment.orderNumber = orderOverview.number
		LEFT JOIN dealerList
		ON orderOverview.dealerid = dealerList.id
		LEFT JOIN contact
		ON orderOverview.customerid = contact.id
		LEFT JOIN terms
		ON orderOverview.termsid = terms.id)
		WHERE dealerList.id = ".$dealer."
		GROUP BY orderOverview.number
		HAVING SUM(payment.amount) > 0";

		if ($dealerContactResult->num_rows > 0) {

			while($dealerContactInfo = $dealerContactResult->fetch_row()){
				echo "<b>Dealer Info:</b><br><br>";
				echo "Dealer Name: <b>".$dealerContactInfo[1]."</b><br>";
				if($dealerContactInfo[2] == ""){
					echo "Website: <b>none</b><br>";
				}else{
					echo "Website: <b><a href=".$dealerContactInfo[2]." target='_blank'>".$dealerContactInfo[2]."</a></b><br>";
				}
				echo "Dealer since: <b>".$dealerContactInfo[15]."</b>";
				echo "<br><br><br>";

				echo "<p>";
					$contactQuery = "SELECT * FROM contact WHERE dealerid = ".$dealerContactInfo[0];
					$contactResult = $conn->query($contactQuery);
					echo "<b>Contact info:</b><br><br>";
					if($contactResult->num_rows > 0){
						while($contact = $contactResult->fetch_row()){
							echo "<b>Name: </b>".$contact[1]." ".$contact[2]."<br>";
							echo "<b>Phone: </b>".$contact[9]."<br>";
							echo "<b>Email: </b>".$contact[10]."<br>";
							echo "<br>";
						}
					}else{
						echo "<b>No contact info found.</b><br><br>";
					}
					echo "<a href='addContact.php'> Add contact</a>";
					echo "<br><br>";





					echo "<table>";
					echo "<th><a href='dealerInfoEdit.php?dealer=".$dealer."'>Edit</a></th><th>Billing info</th><th>Shipping info</th>";
					echo "<tr><td>Address Line 1</td><td>".$dealerContactInfo[3]."</td><td>".$dealerContactInfo[9]."</td></tr>";
					echo "<tr><td>Address Line 2</td><td>".$dealerContactInfo[4]."</td><td>".$dealerContactInfo[10]."</td></tr>";
					echo "<tr><td>City</td><td>".$dealerContactInfo[5]."</td><td>".$dealerContactInfo[11]."</td></tr>";
					echo "<tr><td>State</td><td>".$dealerContactInfo[6]."</td><td>".$dealerContactInfo[12]."</td></tr>";
					echo "<tr><td>Country</td><td>".$dealerContactInfo[7]."</td><td>".$dealerContactInfo[13]."</td></tr>";
					echo "<tr><td>Zip</td><td>".$dealerContactInfo[8]."</td><td>".$dealerContactInfo[14]."</td></tr>";
					echo "</table>";

					echo "<br><br>";

					$creditCheckQuery = "SELECT * FROM creditCheck WHERE dealerID = ".$dealerContactInfo[0];
					$creditCheckResult = $conn->query($creditCheckQuery);
					echo "<b>Credit Check:</b><br><br>";
					if($creditCheckResult->num_rows > 0){
						while($creditCheck = $creditCheckResult->fetch_row()){
							echo "<b>Source: </b>".$creditCheck[1]."<br>";
							echo "<b>Date: </b>".$creditCheck[3]."<br>";
							echo "<b>Comment: </b>".$creditCheck[2]."<br>";
							echo "<br>";
						}
					}else{
						echo "<b>No credit check found.</b>";
					}



				echo "<br><br>";
				echo "</p>";

				echo "<button id='hide'>Hide</button>";
				echo "<button id='show'>Expand</button>";

				echo "<hr>";
				echo "<br><br>";
			}
		}
	}

	$result = $conn->query($sql);
	echo "<b>Orders:</b>";
	echo "<br><br>";
	if ($result->num_rows > 0) {

		echo "<table>";
		echo "<tr>";
		while($fieldinfo = $result->fetch_field()){

			$header = "SELECT dealerName from dealerList";
			$headerResult = $conn->query($header);
			echo "<td>".$fieldinfo->name."<br>";
			echo "</td>";

		}
		echo "</tr>";

		while($row = $result->fetch_row()) {
	        echo "<tr>";
	        echo "<td><a href=".'orderView.php?order='.$row[0].">".$row[0]."</a></td>";
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
	    echo "No orders";
	}
?>

<div id="footer"></div>
</body>
</html>
