<!DOCTYPE HTML>  
<html>
<head>
<style>
.error {color: #FF0000;}
</style>
</head>
<body>  

<?php

//connect to DB

  $connectfile = "connect.php";
  require $connectfile;

  "<label for='formCountries[]'>Select the countries that you have visited:</label><br>
<select multiple="multiple" name="formCountries[]">
    <option value="US">United States</option>
    <option value="UK">United Kingdom</option>
    <option value="France">France</option>
    <option value="Mexico">Mexico</option>
    <option value="Russia">Russia</option>
    <option value="Japan">Japan</option>
</select>"

  $conn->close();
?>

</body>
</html>