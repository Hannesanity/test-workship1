-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 29, 2023 at 06:04 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cvtest`
--

-- --------------------------------------------------------

--
-- Table structure for table `detainees`
--

CREATE TABLE `detainees` (
  `detainee_id` int(11) NOT NULL,
  `inmate_no` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  `gender` enum('Male','Female','Non-Binary','Other') NOT NULL,
  `address` varchar(100) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `nationality` varchar(50) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `detainees`
--

INSERT INTO `detainees` (`detainee_id`, `inmate_no`, `date_of_birth`, `gender`, `address`, `phone_number`, `nationality`, `created_at`) VALUES
(1, 'a', '2002-12-12', 'Male', 'd', 'e', 'g', '2023-08-26 06:18:26'),
(2, 'D', '2021-01-01', 'Male', 'C', 'A', 'I', '2023-08-26 07:22:46'),
(3, 'Hani', '2002-12-12', 'Male', 'ab', 'cd', 'f', '2023-08-27 09:44:09'),
(4, 'tist', '2001-02-02', 'Male', 'a', 'b', 'd', '2023-08-27 09:50:59'),
(5, 'Exercise', '2002-12-12', 'Male', 'a', 'b', 'd', '2023-08-27 09:53:46'),
(6, 'Exercise', '2002-12-12', 'Male', 'a', 'b', 'd', '2023-08-27 09:53:48'),
(7, 'Test', '2002-12-12', 'Male', 'a', 'b', 'd', '2023-08-27 10:10:38'),
(8, 'Jak', '2002-11-12', 'Male', 'a', 'd', 'g', '2023-08-27 10:12:50'),
(9, 'test', '1990-01-01', 'Female', 'a', 'b', 'd', '2023-08-28 12:40:18'),
(10, '', '0000-00-00', 'Male', '', '', '', '2023-08-28 14:40:03'),
(11, 'asd', '0000-00-00', 'Male', '', '', '', '2023-08-28 14:40:09'),
(12, '[value-2]', '0000-00-00', '', '[value-5]', '[value-6]', '[value-7]', '0000-00-00 00:00:00'),
(13, '11111111111', '1111-11-11', 'Male', 'aaaaaaa', '222222222', 'aaaaaaaa', '2023-08-28 16:24:02');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `detainees`
--
ALTER TABLE `detainees`
  ADD PRIMARY KEY (`detainee_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `detainees`
--
ALTER TABLE `detainees`
  MODIFY `detainee_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
