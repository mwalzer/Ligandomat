CREATE DATABASE  IF NOT EXISTS `LigandosphereDB_daemons` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `LigandosphereDB_daemons`;
-- MySQL dump 10.13  Distrib 5.5.37, for debian-linux-gnu (x86_64)
--
-- Host: 192.168.123.61    Database: LigandosphereDB_daemons
-- ------------------------------------------------------
-- Server version	5.5.32-0ubuntu0.13.04.1

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
-- Table structure for table `gradient`
--

DROP TABLE IF EXISTS `gradient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gradient` (
  `gradient_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE latin1_german1_ci NOT NULL,
  `tune_file` longblob,
  `method_file` longblob,
  `comment` varchar(255) COLLATE latin1_german1_ci DEFAULT NULL,
  PRIMARY KEY (`gradient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=latin1 COLLATE=latin1_german1_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hlaallele`
--

DROP TABLE IF EXISTS `hlaallele`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hlaallele` (
  `hlaallele_id` int(11) NOT NULL AUTO_INCREMENT,
  `gene_group` tinytext COLLATE latin1_german1_ci NOT NULL COMMENT '\n',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`hlaallele_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1226 DEFAULT CHARSET=latin1 COLLATE=latin1_german1_ci COMMENT='Admin maintained table - no program shall write here!!!';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `intern_data`
--

DROP TABLE IF EXISTS `intern_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `intern_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` char(255) DEFAULT NULL,
  `seq` char(15) DEFAULT NULL,
  `run` char(255) DEFAULT NULL,
  `rest` text,
  `source_id` int(11) DEFAULT NULL,
  `hla_typing` char(255) DEFAULT NULL,
  `prep_id` int(11) DEFAULT NULL,
  `mass_spec_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `log_file`
--

DROP TABLE IF EXISTS `log_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_file` (
  `log_file_id` int(11) NOT NULL AUTO_INCREMENT,
  `tmp_name` char(255) NOT NULL,
  `action` enum('upload') NOT NULL DEFAULT 'upload',
  `users_users_id` int(11) NOT NULL,
  `successful` bit(1) NOT NULL DEFAULT b'0',
  `message` text,
  PRIMARY KEY (`log_file_id`),
  KEY `users_users_id` (`users_users_id`),
  CONSTRAINT `users_users_id` FOREIGN KEY (`users_users_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mhcpraep`
--

DROP TABLE IF EXISTS `mhcpraep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mhcpraep` (
  `mhcpraep_id` int(11) NOT NULL AUTO_INCREMENT,
  `sample_mass` double DEFAULT NULL COMMENT 'used sample mass in [g]',
  `antibody_set` varchar(255) COLLATE latin1_german1_ci DEFAULT NULL COMMENT 'Obacht beim SELECT: http://dev.mysql.com/doc/refman/5.1/de/set.html',
  `antibody_mass` varchar(255) COLLATE latin1_german1_ci DEFAULT NULL,
  `magna` tinyint(1) NOT NULL DEFAULT '0',
  `comment` text COLLATE latin1_german1_ci,
  `timestamp` char(255) COLLATE latin1_german1_ci NOT NULL,
  `person_person_id` int(11) NOT NULL,
  `sample_volume` double DEFAULT NULL,
  PRIMARY KEY (`mhcpraep_id`),
  KEY `fk_mhcpraep_person1` (`person_person_id`),
  CONSTRAINT `fk_mhcpraeparat_person1` FOREIGN KEY (`person_person_id`) REFERENCES `person` (`person_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=609 DEFAULT CHARSET=latin1 COLLATE=latin1_german1_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `modification`
--

DROP TABLE IF EXISTS `modification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `modification` (
  `modification_id` int(11) NOT NULL AUTO_INCREMENT,
  `modification_type` varchar(255) COLLATE latin1_german1_ci NOT NULL,
  `comment` text COLLATE latin1_german1_ci,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `unimodid` varchar(45) COLLATE latin1_german1_ci DEFAULT NULL,
  PRIMARY KEY (`modification_id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=latin1 COLLATE=latin1_german1_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_run`
--

DROP TABLE IF EXISTS `ms_run`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_run` (
  `ms_run_id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) COLLATE latin1_german1_ci DEFAULT NULL,
  `date` date DEFAULT NULL,
  `used_share` double DEFAULT NULL COMMENT 'sample share in [%]',
  `comment` text COLLATE latin1_german1_ci,
  `timestamp` char(255) COLLATE latin1_german1_ci NOT NULL,
  `mhcpraep_mhcpraep_id` int(11) NOT NULL,
  `gradient_gradient_id` int(11) DEFAULT NULL,
  `person_person_id` int(11) NOT NULL,
  `ms_run_modification_ms_run_modification_id` int(11) DEFAULT NULL,
  `source_source_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`ms_run_id`),
  KEY `fk_mslauf_mhcpraep1` (`mhcpraep_mhcpraep_id`),
  KEY `fk_ms_run_gradient1` (`gradient_gradient_id`),
  KEY `fk_ms_run_person1` (`person_person_id`),
  KEY `fk_ms_run_ms_run_modification1` (`ms_run_modification_ms_run_modification_id`),
  KEY `fk_ms_run_source` (`source_source_id`),
  CONSTRAINT `fk_mslauf_mhcpraeparat1` FOREIGN KEY (`mhcpraep_mhcpraep_id`) REFERENCES `mhcpraep` (`mhcpraep_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_ms_run_gradient1` FOREIGN KEY (`gradient_gradient_id`) REFERENCES `gradient` (`gradient_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_ms_run_ms_run_modification1` FOREIGN KEY (`ms_run_modification_ms_run_modification_id`) REFERENCES `ms_run_modification` (`ms_run_modification_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_ms_run_person1` FOREIGN KEY (`person_person_id`) REFERENCES `person` (`person_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_ms_run_source` FOREIGN KEY (`source_source_id`) REFERENCES `source` (`source_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2420 DEFAULT CHARSET=latin1 COLLATE=latin1_german1_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ms_run_modification`
--

DROP TABLE IF EXISTS `ms_run_modification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ms_run_modification` (
  `ms_run_modification_id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) COLLATE latin1_german1_ci NOT NULL,
  `comment` text COLLATE latin1_german1_ci,
  `name` varchar(255) COLLATE latin1_german1_ci NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ms_run_modification_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_german1_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `peptide`
--

DROP TABLE IF EXISTS `peptide`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `peptide` (
  `peptide_id` int(11) NOT NULL AUTO_INCREMENT,
  `sequence` varchar(255) COLLATE latin1_german1_ci NOT NULL DEFAULT '',
  `comment` text COLLATE latin1_german1_ci,
  `timestamp` char(255) COLLATE latin1_german1_ci NOT NULL,
  `calc_weight` double DEFAULT NULL,
  PRIMARY KEY (`peptide_id`),
  UNIQUE KEY `sequence_UNIQUE` (`sequence`)
) ENGINE=InnoDB AUTO_INCREMENT=981208 DEFAULT CHARSET=latin1 COLLATE=latin1_german1_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `person` (
  `person_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) COLLATE latin1_german1_ci NOT NULL DEFAULT '',
  `last_name` varchar(50) COLLATE latin1_german1_ci NOT NULL DEFAULT '',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `accession_name` varchar(45) COLLATE latin1_german1_ci DEFAULT NULL,
  PRIMARY KEY (`person_id`),
  UNIQUE KEY `accession_name_UNIQUE` (`accession_name`)
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=latin1 COLLATE=latin1_german1_ci COMMENT='Admin maintained table - no program shall write here!!!';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `source`
--

DROP TABLE IF EXISTS `source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `source` (
  `source_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE latin1_german1_ci NOT NULL,
  `comment` text COLLATE latin1_german1_ci,
  `timestamp` char(255) COLLATE latin1_german1_ci NOT NULL,
  `organ` enum('liver','lung','blood','brain','kidney','breast','ovary','prostate','pancreas','bone marrow','colon','skin','stomach') COLLATE latin1_german1_ci NOT NULL,
  `organism` enum('human','mouse','dog') COLLATE latin1_german1_ci NOT NULL,
  `tissue` enum('tumor','adjacent benign','benign','cell line','PBMC','PML') COLLATE latin1_german1_ci NOT NULL,
  `dignity` enum('malignant','benign','infected','tumor') COLLATE latin1_german1_ci NOT NULL,
  `celltype` varchar(255) COLLATE latin1_german1_ci DEFAULT NULL,
  PRIMARY KEY (`source_id`)
) ENGINE=InnoDB AUTO_INCREMENT=450 DEFAULT CHARSET=latin1 COLLATE=latin1_german1_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `source_hlatyping`
--

DROP TABLE IF EXISTS `source_hlatyping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `source_hlatyping` (
  `source_hlatyping_id` int(11) NOT NULL AUTO_INCREMENT,
  `hlaallele_hlaallele_id` int(11) NOT NULL,
  `source_source_id` int(11) NOT NULL,
  `timestamp` char(255) COLLATE latin1_german1_ci NOT NULL,
  `specific_protein` smallint(6) DEFAULT NULL,
  `dna_coding` tinyint(4) DEFAULT NULL,
  `dna_noncoding` tinyint(4) DEFAULT NULL,
  `expression_suffix` varchar(3) COLLATE latin1_german1_ci DEFAULT NULL,
  PRIMARY KEY (`source_hlatyping_id`),
  KEY `fk_source_hlatyping_source1` (`source_source_id`),
  KEY `fk_source_hlatyping_hlaallele1` (`hlaallele_hlaallele_id`),
  CONSTRAINT `fk_source_hlatyping_hlaallele1` FOREIGN KEY (`hlaallele_hlaallele_id`) REFERENCES `hlaallele` (`hlaallele_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_source_hlatyping_source1` FOREIGN KEY (`source_source_id`) REFERENCES `source` (`source_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=16886 DEFAULT CHARSET=latin1 COLLATE=latin1_german1_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `spectrum_hit`
--

DROP TABLE IF EXISTS `spectrum_hit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spectrum_hit` (
  `spectrum_hit_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Is a unsure ligand if spectrum_hit_hlatyping exists.\nIs a sure ligand if stefan_check in spectrum_hit_hlatyping is true.',
  `RT` double DEFAULT NULL,
  `MZ` double DEFAULT NULL,
  `charge` int(11) DEFAULT NULL,
  `comment` text COLLATE latin1_german1_ci,
  `timestamp` char(255) COLLATE latin1_german1_ci NOT NULL,
  `ionscore` int(11) DEFAULT NULL,
  `e_value` double DEFAULT NULL,
  `PEP` double DEFAULT NULL,
  `q_value` double DEFAULT NULL,
  `person_person_id` int(11) NOT NULL,
  `peptide_peptide_id` int(11) NOT NULL,
  `ms_run_ms_run_id` int(11) NOT NULL,
  `precursorarea` double DEFAULT NULL,
  `injectiontime` double DEFAULT NULL,
  `first_scan` int(11) NOT NULL COMMENT '\n',
  `last_scan` int(11) NOT NULL,
  `MH` double DEFAULT NULL,
  `delta_m` double DEFAULT NULL,
  `ions_matched` varchar(255) COLLATE latin1_german1_ci DEFAULT NULL,
  `isolation_interference` tinyint(4) DEFAULT NULL,
  `rank` int(4) DEFAULT NULL,
  `search_engine_rank` int(4) DEFAULT NULL,
  `delta_score` double DEFAULT NULL,
  `delta_cn` double DEFAULT NULL,
  `missed_cleavages` int(4) DEFAULT NULL,
  PRIMARY KEY (`spectrum_hit_id`),
  KEY `fk_spectrum_hit_peptide1` (`peptide_peptide_id`),
  KEY `fk_spectrum_hit_ms_run1` (`ms_run_ms_run_id`),
  KEY `fk_spectrum_hit_person1` (`person_person_id`),
  CONSTRAINT `fk_spectrum_hit_ms_run1` FOREIGN KEY (`ms_run_ms_run_id`) REFERENCES `ms_run` (`ms_run_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_spectrum_hit_peptide1` FOREIGN KEY (`peptide_peptide_id`) REFERENCES `peptide` (`peptide_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_versuchfund_person1` FOREIGN KEY (`person_person_id`) REFERENCES `person` (`person_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=3395505 DEFAULT CHARSET=latin1 COLLATE=latin1_german1_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `spectrum_hit_has_modification`
--

DROP TABLE IF EXISTS `spectrum_hit_has_modification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spectrum_hit_has_modification` (
  `spectrum_hit_spectrum_hit_id` int(11) DEFAULT NULL,
  `modification_modification_id` int(11) DEFAULT NULL,
  `position` tinyint(4) DEFAULT NULL,
  `residue` varchar(1) DEFAULT NULL,
  KEY `spectrum_hit_spectrum_hit_id` (`spectrum_hit_spectrum_hit_id`),
  KEY `modification_modification_id` (`modification_modification_id`),
  CONSTRAINT `spectrum_hit_has_modification_ibfk_1` FOREIGN KEY (`spectrum_hit_spectrum_hit_id`) REFERENCES `spectrum_hit` (`spectrum_hit_id`),
  CONSTRAINT `spectrum_hit_has_modification_ibfk_2` FOREIGN KEY (`modification_modification_id`) REFERENCES `modification` (`modification_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `spectrum_hit_hlatyping`
--

DROP TABLE IF EXISTS `spectrum_hit_hlatyping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spectrum_hit_hlatyping` (
  `spectrum_hit_hlatyping_id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `stefan_check` tinyint(1) NOT NULL DEFAULT '0',
  `comment` text COLLATE latin1_german1_ci,
  `hlaallele_hlaallele_id` int(11) NOT NULL,
  `spectrum_hit_spectrum_hit_id` int(11) NOT NULL,
  PRIMARY KEY (`spectrum_hit_hlatyping_id`),
  KEY `fk_versuchfund_hlatyping_hlaallele1` (`hlaallele_hlaallele_id`),
  KEY `fk_spectrum_hit_hlatyping_spectrum_hit1` (`spectrum_hit_spectrum_hit_id`),
  CONSTRAINT `fk_spectrum_hit_hlatyping_spectrum_hit1` FOREIGN KEY (`spectrum_hit_spectrum_hit_id`) REFERENCES `spectrum_hit` (`spectrum_hit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_versuchfund_hlatyping_hlaallele1` FOREIGN KEY (`hlaallele_hlaallele_id`) REFERENCES `hlaallele` (`hlaallele_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_german1_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` char(255) DEFAULT NULL,
  `password` char(255) DEFAULT NULL,
  `in_group` char(255) DEFAULT NULL,
  `person_person_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `person_person_id` (`person_person_id`),
  CONSTRAINT `person_person_id` FOREIGN KEY (`person_person_id`) REFERENCES `person` (`person_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-06-11 13:21:08
