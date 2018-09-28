CREATE DATABASE  IF NOT EXISTS `BCC` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `BCC`;
-- MySQL dump 10.13  Distrib 5.7.12, for osx10.9 (x86_64)
--
-- Host: 127.0.0.1    Database: BCC
-- ------------------------------------------------------
-- Server version	5.6.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bom`
--

DROP TABLE IF EXISTS `bom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bom` (
  `parent` int(7) NOT NULL,
  `parentRev` int(3) NOT NULL,
  `child` int(7) NOT NULL,
  `childRev` int(3) NOT NULL,
  `eco` int(8) DEFAULT NULL,
  `quantity` float NOT NULL,
  `referenceDesignator` varchar(30) DEFAULT NULL,
  `dateUpdated` date DEFAULT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contact` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `firstName` varchar(20) DEFAULT NULL,
  `lastName` varchar(20) DEFAULT NULL,
  `addressLine1` varchar(50) DEFAULT NULL,
  `addressLine2` varchar(50) DEFAULT NULL,
  `city` varchar(30) DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL,
  `zip` varchar(10) DEFAULT NULL,
  `country` varchar(20) DEFAULT NULL,
  `phoneNumber` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `dealerid` int(3) DEFAULT NULL,
  `supplierid` int(3) DEFAULT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `dateUpdated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `creditCheck`
--

DROP TABLE IF EXISTS `creditCheck`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `creditCheck` (
  `dealerID` int(11) DEFAULT NULL,
  `source` varchar(30) DEFAULT NULL,
  `comment` varchar(500) DEFAULT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `dateUpdated` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dealer`
--

DROP TABLE IF EXISTS `dealer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dealer` (
  `id` int(3) NOT NULL AUTO_INCREMENT,
  `dealerName` varchar(50) NOT NULL,
  `dealerWebsite` varchar(100) DEFAULT NULL,
  `billingAddressLine1` varchar(50) DEFAULT NULL,
  `billingAddressLine2` varchar(50) DEFAULT NULL,
  `billingCity` varchar(30) DEFAULT NULL,
  `billingState` varchar(20) DEFAULT NULL,
  `billingCountry` varchar(20) DEFAULT NULL,
  `billingZip` int(10) DEFAULT NULL,
  `shippingAddressLine1` varchar(50) DEFAULT NULL,
  `shippingAddressLine2` varchar(50) DEFAULT NULL,
  `shippingCity` varchar(30) DEFAULT NULL,
  `shippingState` varchar(20) DEFAULT NULL,
  `shippingCountry` varchar(20) DEFAULT NULL,
  `shippingZip` int(10) DEFAULT NULL,
  `status` varchar(30) NOT NULL DEFAULT '',
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `dateUpdated` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `derp`
--

DROP TABLE IF EXISTS `derp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `derp` (
  `id` int(3) unsigned NOT NULL AUTO_INCREMENT,
  `description` varchar(50) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `eco`
--

DROP TABLE IF EXISTS `eco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eco` (
  `number` int(8) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `dateCreated` datetime DEFAULT NULL,
  `dateSubmitted` datetime DEFAULT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `freight`
--

DROP TABLE IF EXISTS `freight`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `freight` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `carrierName` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `frequencyResponse`
--

DROP TABLE IF EXISTS `frequencyResponse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `frequencyResponse` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `serialNumber` int(11) DEFAULT NULL,
  `frequency` int(11) DEFAULT NULL,
  `measurement` int(11) DEFAULT NULL,
  `date` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventory` (
  `partNumber` int(7) NOT NULL,
  `quantity` double NOT NULL,
  `locationFrom` varchar(20) DEFAULT NULL,
  `locationTo` varchar(20) DEFAULT NULL,
  `note` varchar(100) DEFAULT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `transactionDate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inventoryLocation`
--

DROP TABLE IF EXISTS `inventoryLocation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventoryLocation` (
  `locationName` varchar(20) NOT NULL,
  `address` varchar(30) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL,
  `zip` varchar(10) DEFAULT NULL,
  `country` varchar(20) DEFAULT NULL,
  `id` int(3) NOT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `dateUpdated` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mco`
--

DROP TABLE IF EXISTS `mco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mco` (
  `number` int(8) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `dateCreated` datetime DEFAULT NULL,
  `dateSubmitted` datetime DEFAULT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orderLine`
--

DROP TABLE IF EXISTS `orderLine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orderLine` (
  `orderNumber` int(6) NOT NULL,
  `dateAdded` date NOT NULL,
  `partNumber` int(7) NOT NULL,
  `lineQuantity` int(3) NOT NULL,
  `lineDiscount` double(20,2) DEFAULT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `dateUpdated` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orderOverview`
--

DROP TABLE IF EXISTS `orderOverview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orderOverview` (
  `orderNumber` int(5) unsigned NOT NULL AUTO_INCREMENT,
  `dealerid` int(3) NOT NULL,
  `customerid` int(4) NOT NULL,
  `orderDate` date DEFAULT NULL,
  `invoiceSentDate` date DEFAULT NULL,
  `orderStatus` varchar(10) NOT NULL DEFAULT 'UNPAID',
  `termsid` int(2) NOT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  PRIMARY KEY (`orderNumber`)
) ENGINE=InnoDB AUTO_INCREMENT=1084 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orderShipping`
--

DROP TABLE IF EXISTS `orderShipping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orderShipping` (
  `orderNumber` int(5) DEFAULT NULL,
  `dateShipped` date DEFAULT NULL,
  `trackingNumber` varchar(30) DEFAULT NULL,
  `partNumber` varchar(40) DEFAULT NULL,
  `shipmentMethod` varchar(30) DEFAULT NULL,
  `price` double(11,2) DEFAULT NULL,
  `carrier` varchar(30) DEFAULT NULL,
  `productSerialNumber` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orgList`
--

DROP TABLE IF EXISTS `orgList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orgList` (
  `orgID` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `orgName` varchar(50) DEFAULT NULL,
  `website` varchar(100) DEFAULT NULL,
  `billingAddressLine1` varchar(30) DEFAULT NULL,
  `billingAddressLine2` varchar(30) DEFAULT NULL,
  `billingCity` varchar(30) DEFAULT NULL,
  `billingState` char(2) DEFAULT NULL,
  `billingZip` varchar(30) DEFAULT NULL,
  `billingCountry` varchar(30) DEFAULT NULL,
  `orgAddressLine1` varchar(30) DEFAULT NULL,
  `orgAddressLine2` varchar(30) DEFAULT NULL,
  `orgCity` varchar(30) DEFAULT NULL,
  `orgState` char(2) DEFAULT NULL,
  `orgZip` varchar(12) DEFAULT NULL,
  `orgCountry` varchar(30) DEFAULT NULL,
  `contactFirstName` varchar(30) DEFAULT NULL,
  `contactLastname` varchar(30) DEFAULT NULL,
  `paymentCardType` varchar(20) DEFAULT NULL,
  `paymentCardNumber` int(16) DEFAULT NULL,
  `paymentCardExpMonth` int(2) DEFAULT NULL,
  `paymentCardExpYear` int(2) DEFAULT NULL,
  `paymentCardCVV` int(11) DEFAULT NULL,
  PRIMARY KEY (`orgID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `part`
--

DROP TABLE IF EXISTS `part`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `part` (
  `partNumber` int(7) NOT NULL,
  `description` varchar(100) NOT NULL DEFAULT '',
  `partTypeSubClass1` varchar(20) DEFAULT NULL,
  `partTypeSubClass2` varchar(20) DEFAULT NULL,
  `partTypeSubClass3` varchar(20) DEFAULT NULL,
  `dateAdded` date NOT NULL,
  `unit` int(2) DEFAULT NULL,
  `status` int(2) DEFAULT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `standardPurchasePrice` double(12,4) DEFAULT NULL,
  `standardSellPrice` double(12,4) DEFAULT NULL,
  PRIMARY KEY (`partNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `partFamily`
--

DROP TABLE IF EXISTS `partFamily`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `partFamily` (
  `id` int(1) unsigned NOT NULL AUTO_INCREMENT,
  `description` varchar(30) DEFAULT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `partStatus`
--

DROP TABLE IF EXISTS `partStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `partStatus` (
  `id` int(2) DEFAULT NULL,
  `statusName` varchar(30) DEFAULT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `dateUpdated` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `partType`
--

DROP TABLE IF EXISTS `partType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `partType` (
  `id` int(3) DEFAULT NULL,
  `description` varchar(40) DEFAULT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `dateAdded` datetime DEFAULT NULL,
  `family` int(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `partUnitType`
--

DROP TABLE IF EXISTS `partUnitType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `partUnitType` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `description` varchar(30) DEFAULT NULL,
  `dateAdded` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment` (
  `transactionDate` date NOT NULL,
  `amount` double NOT NULL,
  `orderNumber` int(6) NOT NULL,
  `method` varchar(10) NOT NULL,
  `reference` varchar(30) DEFAULT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pricing`
--

DROP TABLE IF EXISTS `pricing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pricing` (
  `partNumber` int(7) unsigned NOT NULL,
  `umrp` float NOT NULL,
  `grossPrice` decimal(8,2) NOT NULL,
  `dealerNetPrice` decimal(8,2) NOT NULL,
  `dealerDemoNetPrice` decimal(8,2) NOT NULL,
  `distributorNetPrice` decimal(8,2) DEFAULT NULL,
  `distributorDemoNetPrice` decimal(8,2) DEFAULT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `dateUpdated` date DEFAULT NULL,
  PRIMARY KEY (`partNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `qcTestAmp`
--

DROP TABLE IF EXISTS `qcTestAmp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `qcTestAmp` (
  `serialNumber` int(6) DEFAULT NULL,
  `model` int(7) DEFAULT NULL,
  `note` varchar(200) DEFAULT NULL,
  `cosmeticDingCheck` tinyint(1) DEFAULT NULL,
  `tightnessCheck` tinyint(1) DEFAULT NULL,
  `meterCheck` tinyint(1) DEFAULT NULL,
  `volumeControlCheck` tinyint(1) DEFAULT NULL,
  `escutcheonInstallationCheck` tinyint(1) DEFAULT NULL,
  `solderCheck` tinyint(1) DEFAULT NULL,
  `dressingCheck` tinyint(1) DEFAULT NULL,
  `voltageAC10Percent` float DEFAULT NULL,
  `filament10Percent` float DEFAULT NULL,
  `bias10Percent` float DEFAULT NULL,
  `tubePlate10Percent` float DEFAULT NULL,
  `tubeScreen10Percent` float DEFAULT NULL,
  `voltageAC30Percent` float DEFAULT NULL,
  `filament30Percent` float DEFAULT NULL,
  `bias30Percent` float DEFAULT NULL,
  `tubePlate30Percent` float DEFAULT NULL,
  `tubeScreen30Percent` float DEFAULT NULL,
  `voltageAC87Percent` float DEFAULT NULL,
  `filament87Percent` float DEFAULT NULL,
  `bias87Percent` float DEFAULT NULL,
  `tubePlate87Percent` float DEFAULT NULL,
  `tubeScreen87Percent` float DEFAULT NULL,
  `voltageAC100Percent` float DEFAULT NULL,
  `filament100Percent` float DEFAULT NULL,
  `bias100Percent` float DEFAULT NULL,
  `tubePlate100Percent` float DEFAULT NULL,
  `tubeScreen100Percent` float DEFAULT NULL,
  `biasMin` float DEFAULT NULL,
  `biasMax` float DEFAULT NULL,
  `power30Hz` float DEFAULT NULL,
  `power1kHz` float DEFAULT NULL,
  `power30kHz` float DEFAULT NULL,
  `dateChecked` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `qcTestSpeaker`
--

DROP TABLE IF EXISTS `qcTestSpeaker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `qcTestSpeaker` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `serialNumber` int(6) DEFAULT NULL,
  `model` int(7) DEFAULT NULL,
  `note` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `supplier`
--

DROP TABLE IF EXISTS `supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `supplier` (
  `id` int(3) unsigned NOT NULL AUTO_INCREMENT,
  `supplierName` varchar(30) NOT NULL DEFAULT '',
  `billingAddressLine1` varchar(50) DEFAULT NULL,
  `billingAddressLine2` varchar(50) DEFAULT NULL,
  `billingCity` varchar(30) DEFAULT NULL,
  `billingState` varchar(20) DEFAULT NULL,
  `billingZip` int(10) DEFAULT NULL,
  `billingCountry` varchar(20) DEFAULT NULL,
  `shippingAddressLine1` varchar(50) DEFAULT NULL,
  `shippingAddressLine2` varchar(50) DEFAULT NULL,
  `shippingCity` varchar(30) DEFAULT NULL,
  `shippingState` varchar(20) DEFAULT NULL,
  `shippingZip` int(10) DEFAULT NULL,
  `shippingCountry` varchar(20) DEFAULT NULL,
  `website` varchar(150) DEFAULT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `dateUpdated` int(11) DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `supplierPart`
--

DROP TABLE IF EXISTS `supplierPart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `supplierPart` (
  `supplierid` int(4) NOT NULL,
  `orgPartNumber` int(7) NOT NULL,
  `supplierPartNumber` varchar(40) DEFAULT NULL,
  `supplierLink` varchar(500) DEFAULT NULL,
  `purchaseUnitPrice` double NOT NULL,
  `purchaseMOQ` double NOT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `dateUpdated` date DEFAULT NULL,
  `standardPartPrice` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `terms`
--

DROP TABLE IF EXISTS `terms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `terms` (
  `id` int(2) NOT NULL,
  `termType` varchar(20) NOT NULL,
  `defaultDescription` varchar(20) DEFAULT NULL,
  `percentDiscount` decimal(3,2) NOT NULL,
  `periodDays` int(3) NOT NULL,
  `netDays` int(3) NOT NULL,
  `termsStatus` varchar(10) NOT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `dateUpdated` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `todo`
--

DROP TABLE IF EXISTS `todo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `todo` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `category` varchar(20) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `dateUpdated` date DEFAULT NULL,
  `dateCompleted` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaction` (
  `amount` double NOT NULL,
  `supplier` varchar(40) NOT NULL,
  `category` varchar(20) NOT NULL,
  `subCategory` varchar(20) NOT NULL,
  `note` varchar(100) DEFAULT NULL,
  `dateDue` date DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `orgID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  `dateUpdated` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `userList`
--

DROP TABLE IF EXISTS `userList`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userList` (
  `userID` int(11) NOT NULL,
  `employeeReferenceNumber` varchar(30) DEFAULT NULL,
  `userFirstName` varchar(30) DEFAULT NULL,
  `userLastName` varchar(30) DEFAULT NULL,
  `userEmail` varchar(50) DEFAULT NULL,
  `orgID` int(11) DEFAULT NULL,
  `dateUpdated` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `websiteInquiries`
--

DROP TABLE IF EXISTS `websiteInquiries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `websiteInquiries` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `firstName` varchar(20) DEFAULT NULL,
  `lastName` varchar(20) DEFAULT NULL,
  `subject` varchar(50) DEFAULT NULL,
  `message` varchar(7000) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `city` varchar(30) DEFAULT NULL,
  `state` varchar(2) DEFAULT NULL,
  `country` varchar(20) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `category` varchar(30) DEFAULT NULL,
  `note` varchar(100) DEFAULT NULL,
  `mailingListStatus` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=786 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-09-27 20:00:29
