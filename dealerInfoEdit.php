<html>
<head>
	<title>BCC Dealer Info Edit</title>
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

	header("Cache-Control: no-cache, no-store, must-revalidate");
	$connectfile = "connect.php";
	require $connectfile;
	$dealer = $_GET["dealer"];
	$dealerName = $_GET["dealerName"];
	$website = $_GET["website"];
	$billAddressLine1 = $_GET["billAddressLine1"];
	$billAddressLine2 = $_GET["billAddressLine2"];
	$billCity = $_GET["billCity"];
	$billState = $_GET["billState"];
	$billCountry = $_GET["billCountry"];
	$billZip = $_GET["billZip"];
	$shipAddressLine1 = $_GET["shipAddressLine1"];
	$shipAddressLine2 = $_GET["shipAddressLine2"];
	$shipCity = $_GET["shipCity"];
	$shipState = $_GET["shipState"];
	$shipCountry = $_GET["shipCountry"];
	$shiZip = $_GET["shipZip"];
	$dateAdded = $_GET["dateAdded"];
	$dealerStatus = $_GET["status"];
	//echo $dealer;

	$dealerInfoQuery = "SELECT * FROM dealerList WHERE id = ".$dealer;
	//echo $dealerInfoQuery;
	$dealerInfoResult = $conn->query($dealerInfoQuery);

	if($dealerInfoResult->num_rows > 0){
		$dealerInfo = $dealerInfoResult->fetch_row();
		$dealerInfoUpdateQuery = "UPDATE dealerList SET ";
		if($dealer == ""){
			$dealerInfoUpdateQuery .= "id=NULL, ";
		}else{
			$dealerInfoUpdateQuery .= "id=".$dealer.", ";
		}
		if($dealerName == ""){
			$dealerInfoUpdateQuery .= "dealerName=NULL, ";
		}else{
			$dealerInfoUpdateQuery .= "dealerName='".$dealerName."', ";
		}
		if($website == ""){
			$dealerInfoUpdateQuery .= "dealerWebsite=NULL, ";
		}else{
			$dealerInfoUpdateQuery .= "dealerWebsite='".$website."', ";
		}
		if($billAddressLine1 == ""){
			$dealerInfoUpdateQuery .="billingAddressLine1=NULL, ";
		}else{
			$dealerInfoUpdateQuery .="billingAddressLine1='".$billAddressLine1."', ";
		}
		if($billAddressLine2 == ""){
			$dealerInfoUpdateQuery .="billingAddressLine2=NULL, ";
		}else{
			$dealerInfoUpdateQuery .="billingAddressLine2='".$billAddressLine2."', ";
		}
		if($billCity == ""){
			$dealerInfoUpdateQuery .="billingCity=NULL, ";
		}else{
			$dealerInfoUpdateQuery .="billingCity='".$billCity."', ";
		}
		if($billState == ""){
			$dealerInfoUpdateQuery .="billingState=NULL, ";
		}else{
			$dealerInfoUpdateQuery .="billingState='".$billState."', ";
		}
		if($billCountry == ""){
			$dealerInfoUpdateQuery .="billingCountry=NULL, ";
		}else{
			$dealerInfoUpdateQuery .="billingCountry='".$billCountry."', ";
		}
		if($billZip == ""){
			$dealerInfoUpdateQuery .="billingZip=NULL, ";
		}else{
			$dealerInfoUpdateQuery .="billingZip='".$billZip."', ";
		}
		if($shipAddressLine1 == ""){
			$dealerInfoUpdateQuery .="shippingAddressLine1=NULL, ";
		}else{
			$dealerInfoUpdateQuery .="shippingAddressLine1='".$shipAddressLine1."', ";
		}
		if($shipAddressLine2 == ""){
			$dealerInfoUpdateQuery .="shippingAddressLine2=NULL, ";
		}else{
			$dealerInfoUpdateQuery .="shippingAddressLine2='".$shipAddressLine2."', ";
		}
		if($shipCity == ""){
			$dealerInfoUpdateQuery .="shippingCity=NULL, ";
		}else{
			$dealerInfoUpdateQuery .="shippingCity='".$shipCity."', ";
		}
		if($shipState == ""){
			$dealerInfoUpdateQuery .="shippingState=NULL, ";
		}else{
			$dealerInfoUpdateQuery .="shippingState='".$shipState."', ";
		}
		if($shipCountry == ""){
			$dealerInfoUpdateQuery .="shippingCountry=NULL, ";
		}else{
			$dealerInfoUpdateQuery .="shippingCountry='".$shipCountry."', ";
		}
		if($shipZip == ""){
			$dealerInfoUpdateQuery .="shippingZip=NULL, ";
		}else{
			$dealerInfoUpdateQuery .="shippingZip='".$shipZip."', ";
		}
		if($dateAdded == ""){
			$dealerInfoUpdateQuery .="dateAdded=NULL, ";
		}else{
			$dealerInfoUpdateQuery .="dateAdded='".$dateAdded."', ";
		}
		if($dealerStatus == ""){
			$dealerInfoUpdateQuery .="status=NULL ";
		}else{
			$dealerInfoUpdateQuery .="status='".$dealerStatus."' ";
		}

		$dealerInfoUpdateQuery .="WHERE id = ".$dealer;

		echo $dealerInfoUpdateQuery;

		echo "<FORM METHOD = 'LINK' ACTION = 'dealerInfoEdit.php'>";
		if($dealerInfo[0] == ""){
			echo "Dealer Code: <INPUT TYPE='text' NAME = 'dealer'><br>";
		}else{
			echo "Dealer Code: <INPUT TYPE='text' VALUE = '".$dealerInfo[0]."' NAME = 'dealer'><br>";
		}
		if($dealerInfo[1] == ""){
			echo "Dealer Name: <INPUT TYPE='text' NAME = 'dealerName'><br>";
		}else{
			echo "Dealer Name: <INPUT TYPE='text' VALUE = '".$dealerInfo[1]."' NAME = 'dealerName'><br>";
		}
		if($dealerInfo[2] == ""){
			echo "Website: <INPUT TYPE='text' NAME = 'website'><br>";
		}else{
			echo "Website: <INPUT TYPE='text' VALUE = '".$dealerInfo[2]."' NAME = 'website'><br>";
		}



		echo "<br><br><b>Billing Info:</b><br>";
		if($dealerInfo[3] == ""){
			echo "Address Line 1: <INPUT TYPE='text' NAME = 'billAddressLine1'><br>";
		}else{
			echo "Address Line 1: <INPUT TYPE='text' VALUE = '".$dealerInfo[3]."' NAME = 'billAddressLine1'><br>";
		}
		if($dealerInfo[4] == ""){
			echo "Address Line 2: <INPUT TYPE='text' NAME = 'billAddressLine2'><br>";
		}else{
			echo "Address Line 2: <INPUT TYPE='text' VALUE = '".$dealerInfo[4]."' NAME = 'billAddressLine2'><br>";
		}
		if($dealerInfo[5] == ""){
			echo "City: <INPUT TYPE='text' NAME = 'billCity'><br>";
		}else{
			echo "City: <INPUT TYPE='text' VALUE = '".$dealerInfo[5]."' NAME = 'billCity'><br>";
		}
		if($dealerInfo[6] == ""){
			echo "State: <INPUT TYPE='text' NAME = 'billState'><br>";
		}else{
			echo "State: <INPUT TYPE='text' VALUE = '".$dealerInfo[6]."' NAME = 'billState'><br>";
		}
		if($dealerInfo[7] == ""){
			echo "Country: <INPUT TYPE='text' NAME = 'billCountry'><br>";
		}else{
			echo "Country: <INPUT TYPE='text' VALUE = '".$dealerInfo[7]."' NAME = 'billCountry'><br>";
		}
		if($dealerInfo[8] == ""){
			echo "Zip: <INPUT TYPE='text' NAME = 'billZip'><br>";
		}else{
			echo "Zip: <INPUT TYPE='text' VALUE = '".$dealerInfo[8]."' NAME = 'billZip'><br>";
		}

		echo "<br><br><b>Shipping Info:</b><br>";
		if($dealerInfo[9] == ""){
			echo "Address Line 1: <INPUT TYPE='text' NAME = 'addressLine1'><br>";
		}else{
			echo "Address Line 1: <INPUT TYPE='text' VALUE = '".$dealerInfo[9]."' NAME = 'addressLine1'><br>";
		}
		if($dealerInfo[10] == ""){
			echo "Address Line 2: <INPUT TYPE='text' NAME = 'addressLine2'><br>";
		}else{
			echo "Address Line 2: <INPUT TYPE='text' VALUE = '".$dealerInfo[10]."' NAME = 'addressLine2'><br>";
		}
		if($dealerInfo[11] == ""){
			echo "City: <INPUT TYPE='text' NAME = 'city'><br>";
		}else{
			echo "City: <INPUT TYPE='text' VALUE = '".$dealerInfo[11]."' NAME = 'city'><br>";
		}
		if($dealerInfo[12] == ""){
			echo "State: <INPUT TYPE='text' NAME = 'state'><br>";
		}else{
			echo "State: <INPUT TYPE='text' VALUE = '".$dealerInfo[12]."' NAME = 'state'><br>";
		}
		if($dealerInfo[13] == ""){
			echo "Country: <INPUT TYPE='text' NAME = 'country'><br>";
		}else{
			echo "Country: <INPUT TYPE='text' VALUE = '".$dealerInfo[13]."' NAME = 'country'><br>";
		}
		if($dealerInfo[14] == ""){
			echo "Zip: <INPUT TYPE='text' NAME = 'zip'><br>";
		}else{
			echo "Zip: <INPUT TYPE='text' VALUE = '".$dealerInfo[14]."' NAME = 'zip'><br>";
		}


		echo "<br><br><br>";
		if($dealerInfo[16] == ""){
			echo "Status: <INPUT TYPE='text' NAME = 'zip'><br>";
		}else{
			echo "Status: <INPUT TYPE='text' VALUE = '".$dealerInfo[16]."' NAME = 'status'><br>";
		}

		echo "<br><br><br><INPUT TYPE='submit' VALUE='Update'></FORM>";

	}

?>

<div id="footer"></div>
</body>
</html>
