USE `danydonatt_gls`;
-- MySQL dump 10.13  Distrib 5.5.46, for debian-linux-gnu (i686)
--
-- Host: 127.0.0.1    Database: gls
-- ------------------------------------------------------
-- Server version	5.5.46-0ubuntu0.14.04.2

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
-- Table structure for table `DataType`
--

DROP TABLE IF EXISTS `DataType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DataType` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DataTypeName` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `DjangoFormat` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DataType`
--

LOCK TABLES `DataType` WRITE;
/*!40000 ALTER TABLE `DataType` DISABLE KEYS */;
INSERT INTO `DataType` VALUES (1,'DateTime64','BigIntegerField'),(2,'Hex1','CharField(1)'),(3,'Hex2','IntegerField'),(4,'Hex4','CharField(8)'),(5,'Hex8','BigIntegerField'),(6,'NmeaAddress','CharField(6)'),(7,'NmeaLatitude','Specific'),(8,'NmeaLongitude','Specific'),(9,'NmeaTime','Specific'),(10,'String','CharField(1) E or W');
/*!40000 ALTER TABLE `DataType` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Field_Definition_Message`
--

DROP TABLE IF EXISTS `Field_Definition_Message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Field_Definition_Message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Field_Definition_MessageName` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `XmlTag` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `LengthMin` int(11) NOT NULL,
  `LengthMax` int(11) NOT NULL,
  `DataType_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Field_Definition_Message_DataType_id_13a5adaf_fk_DataType_id` (`DataType_id`),
  CONSTRAINT `Field_Definition_Message_DataType_id_13a5adaf_fk_DataType_id` FOREIGN KEY (`DataType_id`) REFERENCES `DataType` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Field_Definition_Message`
--

LOCK TABLES `Field_Definition_Message` WRITE;
/*!40000 ALTER TABLE `Field_Definition_Message` DISABLE KEYS */;
INSERT INTO `Field_Definition_Message` VALUES (1,'Battery_Level','<batl>',1,1,2),(2,'Latitude','<la>',4,7,7),(3,'Longitude','<lg>',2,8,8),(4,'Session','<sn>',1,8,4),(5,'Sphere','<sp>',1,1,10),(6,'Status','<st>',1,1,2),(7,'NmeaAddr','<na>',6,6,6),(8,'Nmea_Status','<ns>',1,1,10),(9,'Pole','<pl>',1,1,10),(10,'Timestamp64','<t64>',1,16,1),(11,'TimestampN','<tn>',6,10,9);
/*!40000 ALTER TABLE `Field_Definition_Message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LMDM_Format`
--

DROP TABLE IF EXISTS `LMDM_Format`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LMDM_Format` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `LMDMFormatName` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LMDM_Format`
--

LOCK TABLES `LMDM_Format` WRITE;
/*!40000 ALTER TABLE `LMDM_Format` DISABLE KEYS */;
INSERT INTO `LMDM_Format` VALUES (1,'Std0'),(2,'Std1'),(3,'Std2'),(4,'NGLL');
/*!40000 ALTER TABLE `LMDM_Format` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Locate_Message_Definition_Message`
--

DROP TABLE IF EXISTS `Locate_Message_Definition_Message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Locate_Message_Definition_Message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Source` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `Format_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Locate_Message_Definition_M_Format_id_ae57b8ef_fk_LMDM_Format_id` (`Format_id`),
  CONSTRAINT `Locate_Message_Definition_M_Format_id_ae57b8ef_fk_LMDM_Format_id` FOREIGN KEY (`Format_id`) REFERENCES `LMDM_Format` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Locate_Message_Definition_Message`
--

LOCK TABLES `Locate_Message_Definition_Message` WRITE;
/*!40000 ALTER TABLE `Locate_Message_Definition_Message` DISABLE KEYS */;
INSERT INTO `Locate_Message_Definition_Message` VALUES (1,'LabD',1),(2,'LabD',2);
/*!40000 ALTER TABLE `Locate_Message_Definition_Message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Metka`
--

DROP TABLE IF EXISTS `Metka`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Metka` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` longtext COLLATE utf8_unicode_ci NOT NULL,
  `DateImport` datetime,
  `readed` tinyint(1),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Metka`
--

LOCK TABLES `Metka` WRITE;
/*!40000 ALTER TABLE `Metka` DISABLE KEYS */;
/*!40000 ALTER TABLE `Metka` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Std0`
--

DROP TABLE IF EXISTS `Std0`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Std0` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `LocateMessageDefinition` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `LabD` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Std0` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Tag_ID_Format` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Tag_ID` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `X` double DEFAULT NULL,
  `Y` double DEFAULT NULL,
  `Z` double DEFAULT NULL,
  `Battery` int(11) DEFAULT NULL,
  `Timestamp` varchar(25) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Status` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Session` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `Zone` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `DateImport` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1763 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Std0`
--

LOCK TABLES `Std0` WRITE;
/*!40000 ALTER TABLE `Std0` DISABLE KEYS */;
/*!40000 ALTER TABLE `Std0` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add metka',7,'add_metka'),(20,'Can change metka',7,'change_metka'),(21,'Can delete metka',7,'delete_metka'),(22,'Can add data type',8,'add_datatype'),(23,'Can change data type',8,'change_datatype'),(24,'Can delete data type',8,'delete_datatype'),(25,'Can add field_ definition_ message',9,'add_field_definition_message'),(26,'Can change field_ definition_ message',9,'change_field_definition_message'),(27,'Can delete field_ definition_ message',9,'delete_field_definition_message'),(31,'Can add locate_ message_ definition_ message',11,'add_locate_message_definition_message'),(32,'Can change locate_ message_ definition_ message',11,'change_locate_message_definition_message'),(33,'Can delete locate_ message_ definition_ message',11,'delete_locate_message_definition_message'),(34,'Can add lmdm format',12,'add_lmdmformat'),(35,'Can change lmdm format',12,'change_lmdmformat'),(36,'Can delete lmdm format',12,'delete_lmdmformat'),(37,'Can add std0',13,'add_std0'),(38,'Can change std0',13,'change_std0'),(39,'Can delete std0',13,'delete_std0');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `first_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$24000$PfcTBp3IxYfc$wo9hsLj95kNQ+Owq4bSRtbuNSW8gnXw81vdkedkgzwQ=','2015-12-25 11:08:28',1,'ancel','','','ancelada-music@gmail.com',1,1,'2015-12-25 05:44:49');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext COLLATE utf8_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2015-12-25 05:52:57','1','Std0',1,'Добавлено.',NULL,1),(2,'2015-12-25 05:53:05','2','Std1',1,'Добавлено.',NULL,1),(3,'2015-12-25 05:54:15','1','Locate_Message_Definition_Message object',1,'Добавлено.',11,1),(4,'2015-12-25 05:57:11','2','LabD',1,'Добавлено.',11,1),(5,'2015-12-25 05:58:23','3','Std2',1,'Добавлено.',NULL,1),(6,'2015-12-25 05:58:35','4','NGLL',1,'Добавлено.',NULL,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(8,'mainapp','datatype'),(9,'mainapp','field_definition_message'),(12,'mainapp','lmdmformat'),(11,'mainapp','locate_message_definition_message'),(7,'mainapp','metka'),(13,'mainapp','std0'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2015-12-25 05:07:38'),(2,'auth','0001_initial','2015-12-25 05:07:42'),(3,'admin','0001_initial','2015-12-25 05:07:43'),(4,'admin','0002_logentry_remove_auto_add','2015-12-25 05:07:43'),(5,'contenttypes','0002_remove_content_type_name','2015-12-25 05:07:44'),(6,'auth','0002_alter_permission_name_max_length','2015-12-25 05:07:44'),(7,'auth','0003_alter_user_email_max_length','2015-12-25 05:07:44'),(8,'auth','0004_alter_user_username_opts','2015-12-25 05:07:45'),(9,'auth','0005_alter_user_last_login_null','2015-12-25 05:07:45'),(10,'auth','0006_require_contenttypes_0002','2015-12-25 05:07:45'),(11,'auth','0007_alter_validators_add_error_messages','2015-12-25 05:07:45'),(12,'mainapp','0001_initial','2015-12-25 05:07:46'),(13,'sessions','0001_initial','2015-12-25 05:07:47'),(14,'mainapp','0002_auto_20151225_0912','2015-12-25 06:12:52'),(15,'mainapp','0003_std0','2015-12-25 11:38:02'),(16,'mainapp','0004_std0_dateimport','2016-01-04 09:29:14'),(17,'mainapp','0005_auto_20160104_1445','2016-01-04 11:45:22'),(18,'mainapp','0006_auto_20160104_1515','2016-01-04 12:16:00'),(19,'mainapp','0007_auto_20160111_0801','2016-01-11 05:01:41'),(20,'mainapp','0008_metka_dateimport','2016-01-12 09:08:58'),(21,'mainapp','0009_auto_20160112_1401','2016-01-12 11:01:53'),(22,'mainapp','0010_metka_readed','2016-01-12 11:51:53');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('85tl3jm8ryf5vcdl0butmsdlb2jenyib','NjA0MzJkY2MwNmNlNTY0MmNkYjViY2Y0MTk4ZTYwMzJlMmI3NmM4Njp7Il9hdXRoX3VzZXJfaGFzaCI6ImNmMjQwYjlhZTg5NTYyNTM1NjM5OTVlNjhmNDQzY2JlMWVlYjJjYzgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-01-08 05:45:12'),('zrmhhoy2njgwj0z85917201j5wj9esnn','NjA0MzJkY2MwNmNlNTY0MmNkYjViY2Y0MTk4ZTYwMzJlMmI3NmM4Njp7Il9hdXRoX3VzZXJfaGFzaCI6ImNmMjQwYjlhZTg5NTYyNTM1NjM5OTVlNjhmNDQzY2JlMWVlYjJjYzgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-01-08 11:08:28');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-01-12 16:49:53
