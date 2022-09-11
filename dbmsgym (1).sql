-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 26, 2021 at 03:47 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.2.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gym`
--

-- --------------------------------------------------------

--
-- Table structure for table `trainee`
--

CREATE TABLE `trainee` (
  `id` int(11) NOT NULL,
  `aadharid` varchar(50) NOT NULL,
  `trainingtype` varchar(50) NOT NULL,
  `tcode` varchar(50) NOT NULL,
  `weight` int(11) NOT NULL,
  `tname` varchar(50) NOT NULL,
  `tphone` varchar(12) NOT NULL,
  `taddress` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `trainee`
--

INSERT INTO `trainee` (`id`, `aadharid`, `trainingtype`, `tcode`, `weight`, `tname`, `tphone`, `taddress`) VALUES
(3, 'KA20210011', 'Premium', 'MAT123', 85, 'ARK', '9986786453', 'BANGALORE'),
(4, 'KA20210022', 'Premium', 'BBH01', 92, 'kartik', '8088131784', 'banaglore ');

-- --------------------------------------------------------

--
-- Table structure for table `trainerdata`
--

CREATE TABLE `trainerdata` (
  `id` int(11) NOT NULL,
  `tcode` varchar(200) NOT NULL,
  `tname` varchar(200) NOT NULL,
  `normal` int(11) NOT NULL,
  `premium` int(11) NOT NULL,
  `diamond` int(11) NOT NULL,
  `exclusive` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `trainerdata`
--

INSERT INTO `trainerdata` (`id`, `tcode`, `tname`, `normal`, `premium`, `diamond`, `exclusive`) VALUES
(3, 'MAT123', 'Matha Hospital', 40, 4, 4, 1);

--
-- Triggers `trainerdata`
--
DELIMITER $$
CREATE TRIGGER `Insert` AFTER INSERT ON `trainerdata` FOR EACH ROW INSERT INTO trig VALUES(null,NEW.tcode,NEW.normal,NEW.premium,NEW.diamond,NEW.exclusive,' INSERTED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `Update` AFTER UPDATE ON `trainerdata` FOR EACH ROW INSERT INTO trig VALUES(null,NEW.tcode,NEW.normal,NEW.premium,NEW.diamond,NEW.exclusive,' UPDATED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `delet` BEFORE DELETE ON `trainerdata` FOR EACH ROW INSERT INTO trig VALUES(null,OLD.tcode,OLD.normal,OLD.premium,OLD.diamond,OLD.exclusive,' DELETED',NOW())
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `trainer`
--

CREATE TABLE `trainer` (
  `id` int(11) NOT NULL,
  `tcode` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `trainer`
--

INSERT INTO `trainer` (`id`, `tcode`, `email`, `password`) VALUES
(7, 'BBH01', 'aneesrehman95567@gmail.com', 'pbkdf2:sha256:260000$im6PllE9qrd0asQY$3e62fcb9697d2b048acd83cb3658bac8ae5edb5ff58086699d134fb0ed41d788'),
(9, 'MAT123', 'arkprocoder@gmail.com', 'pbkdf2:sha256:260000$CPDXGkSY1zXsarEA$fdbec84d1b2c32e521c75f51bb917daaa4f7a53e567e4478d23ba944c53b1177');

-- --------------------------------------------------------

--
-- Table structure for table `test`
--

CREATE TABLE `test` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `test`
--

INSERT INTO `test` (`id`, `name`) VALUES
(1, 'anees'),
(2, 'rehman');

-- --------------------------------------------------------

--
-- Table structure for table `trig`
--

CREATE TABLE `trig` (
  `id` int(11) NOT NULL,
  `tcode` varchar(50) NOT NULL,
  `normal` int(11) NOT NULL,
  `premium` int(11) NOT NULL,
  `diamond` int(11) NOT NULL,
  `exclusive` int(11) NOT NULL,
  `querys` varchar(50) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `trig`
--

INSERT INTO `trig` (`id`, `tcode`, `normal`, `premium`, `diamond`, `exclusive`, `querys`, `date`) VALUES
(1, 'BBH01', 50, 9, 2, 1, ' UPDATED', '2021-11-26'),
(2, 'BBH01', 50, 9, 2, 1, ' DELETED', '2021-11-26');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `aadharid` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `dob` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `aadharid`, `email`, `dob`) VALUES
(9, 'KA20210011', 'ark@gmail.com', 'pbkdf2:sha256:260000$AhqgDCims0G1LSEi$ada839cc254cd79f9708e777ae02d83cec210677c342e01c3affd8c1358775d9'),
(10, 'KA20210022', 'rehman@gmail.com', 'pbkdf2:sha256:260000$74GEC2qyVtOiPl5s$2a95f811bbd5a50eaac0404fb8fa3682b6c3b67f4493037134c9672393136694');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `trainee`
--
ALTER TABLE `trainee`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `aadharid` (`aadharid`(20));

--
-- Indexes for table `trainerdata`
--
ALTER TABLE `trainerdata`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tcode` (`tcode`);

--
-- Indexes for table `trainer`
--
ALTER TABLE `trainer`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `test`
--
ALTER TABLE `test`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `trig`
--
ALTER TABLE `trig`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `aadharid` (`aadharid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `trainee`
--
ALTER TABLE `trainee`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `trainerdata`
--
ALTER TABLE `trainerdata`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `trainer`
--
ALTER TABLE `trainer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `test`
--
ALTER TABLE `test`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `trig`
--
ALTER TABLE `trig`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
