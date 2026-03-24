-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Generation Time: Mar 23, 2026 at 04:02 PM
-- Server version: 12.2.2-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ojt_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance_attendance`
--

CREATE TABLE `attendance_attendance` (
  `id` bigint(20) NOT NULL,
  `date` date NOT NULL,
  `time_in_1` time(6) DEFAULT NULL,
  `time_out_1` time(6) DEFAULT NULL,
  `time_in_2` time(6) DEFAULT NULL,
  `time_out_2` time(6) DEFAULT NULL,
  `total_hours` decimal(6,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `attendance_attendance`
--

INSERT INTO `attendance_attendance` (`id`, `date`, `time_in_1`, `time_out_1`, `time_in_2`, `time_out_2`, `total_hours`, `status`, `user_id`) VALUES
(7, '2026-03-22', '15:51:54.000000', '15:53:39.000000', '15:53:54.000000', '15:55:39.000000', 0.06, 'incomplete', 14),
(8, '2026-03-23', '08:07:56.000000', '08:08:31.000000', '08:19:12.000000', NULL, 0.01, 'incomplete', 14),
(9, '2026-03-23', '08:13:58.000000', '12:54:37.000000', '12:54:44.000000', '16:54:43.000000', 8.68, 'present', 15);

-- --------------------------------------------------------

--
-- Table structure for table `authtoken_token`
--

CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `authtoken_token`
--

INSERT INTO `authtoken_token` (`key`, `created`, `user_id`) VALUES
('23d2cac8eeb5e6e911b2fb9a8cab2938da576235', '2026-03-23 04:58:28.578827', 15),
('438cfa0f2a0cb00096a6ccf341d641cfd6cbf5fd', '2026-03-22 07:58:30.865703', 14),
('5a6df1904abcc8bd22c78d48f9643c5fa2305c44', '2026-03-22 07:45:18.847867', 12),
('86771b4734b103a1a0ca8fa7db5e216348e0e5ba', '2026-03-22 07:48:48.776284', 13);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 3, 'add_permission'),
(6, 'Can change permission', 3, 'change_permission'),
(7, 'Can delete permission', 3, 'delete_permission'),
(8, 'Can view permission', 3, 'view_permission'),
(9, 'Can add group', 2, 'add_group'),
(10, 'Can change group', 2, 'change_group'),
(11, 'Can delete group', 2, 'delete_group'),
(12, 'Can view group', 2, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add user', 7, 'add_user'),
(26, 'Can change user', 7, 'change_user'),
(27, 'Can delete user', 7, 'delete_user'),
(28, 'Can view user', 7, 'view_user'),
(29, 'Can add absence', 8, 'add_absence'),
(30, 'Can change absence', 8, 'change_absence'),
(31, 'Can delete absence', 8, 'delete_absence'),
(32, 'Can view absence', 8, 'view_absence'),
(33, 'Can add attendance', 9, 'add_attendance'),
(34, 'Can change attendance', 9, 'change_attendance'),
(35, 'Can delete attendance', 9, 'delete_attendance'),
(36, 'Can view attendance', 9, 'view_attendance'),
(37, 'Can add Token', 10, 'add_token'),
(38, 'Can change Token', 10, 'change_token'),
(39, 'Can delete Token', 10, 'delete_token'),
(40, 'Can view Token', 10, 'view_token'),
(41, 'Can add Token', 11, 'add_tokenproxy'),
(42, 'Can change Token', 11, 'change_tokenproxy'),
(43, 'Can delete Token', 11, 'delete_tokenproxy'),
(44, 'Can view Token', 11, 'view_tokenproxy'),
(45, 'Can add ojt profile', 12, 'add_ojtprofile'),
(46, 'Can change ojt profile', 12, 'change_ojtprofile'),
(47, 'Can delete ojt profile', 12, 'delete_ojtprofile'),
(48, 'Can view ojt profile', 12, 'view_ojtprofile');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(12, 'pbkdf2_sha256$1200000$PoltvAKn4ekgv9lmCQl6Id$3qQqeSZXrzQ6oKFS5/PzcUROTQmYCb2cMVEMieO4YIU=', NULL, 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2026-03-22 07:45:09.627192'),
(13, 'pbkdf2_sha256$1200000$Qet1lhIcoutNyKotiAoe9s$tHsdCQS+p+fMnYMuToIEaOic1q7iokZQxO2qasObUF0=', NULL, 0, '20001', '', '', '', 0, 1, '2026-03-22 07:47:52.270686'),
(14, 'pbkdf2_sha256$1200000$hjM91nFs82Pdz3leTHaAe6$qem2O866wyIS9EasNz1EaKQff11CI9UkTsl4NGjz8q8=', NULL, 0, '40001', '', '', 'ogalealahdin1223@gmail.com', 0, 1, '2026-03-22 07:51:03.894240'),
(15, 'pbkdf2_sha256$1200000$gzhxacnCu02aF0SakGEVS7$+F1oc0cOuWRhKWhtof89eRxAu2IEI5bdnYEc8zSktSs=', NULL, 0, '40002', '', '', '40002@gmail.com', 0, 1, '2026-03-23 00:12:46.052235');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(8, 'attendance', 'absence'),
(9, 'attendance', 'attendance'),
(2, 'auth', 'group'),
(3, 'auth', 'permission'),
(4, 'auth', 'user'),
(10, 'authtoken', 'token'),
(11, 'authtoken', 'tokenproxy'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(12, 'users', 'ojtprofile'),
(7, 'users', 'user');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-03-16 16:13:50.481001'),
(2, 'auth', '0001_initial', '2026-03-16 16:13:50.785595'),
(3, 'admin', '0001_initial', '2026-03-16 16:13:50.837545'),
(4, 'admin', '0002_logentry_remove_auto_add', '2026-03-16 16:13:50.843442'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-03-16 16:13:50.854290'),
(6, 'users', '0001_initial', '2026-03-16 16:13:50.862660'),
(8, 'contenttypes', '0002_remove_content_type_name', '2026-03-16 16:13:50.976681'),
(9, 'auth', '0002_alter_permission_name_max_length', '2026-03-16 16:13:51.004965'),
(10, 'auth', '0003_alter_user_email_max_length', '2026-03-16 16:13:51.020988'),
(11, 'auth', '0004_alter_user_username_opts', '2026-03-16 16:13:51.027793'),
(12, 'auth', '0005_alter_user_last_login_null', '2026-03-16 16:13:51.051236'),
(13, 'auth', '0006_require_contenttypes_0002', '2026-03-16 16:13:51.052884'),
(14, 'auth', '0007_alter_validators_add_error_messages', '2026-03-16 16:13:51.059254'),
(15, 'auth', '0008_alter_user_username_max_length', '2026-03-16 16:13:51.076646'),
(16, 'auth', '0009_alter_user_last_name_max_length', '2026-03-16 16:13:51.097049'),
(17, 'auth', '0010_alter_group_name_max_length', '2026-03-16 16:13:51.117995'),
(18, 'auth', '0011_update_proxy_permissions', '2026-03-16 16:13:51.127521'),
(19, 'auth', '0012_alter_user_first_name_max_length', '2026-03-16 16:13:51.145490'),
(20, 'sessions', '0001_initial', '2026-03-16 16:13:51.167192'),
(21, 'authtoken', '0001_initial', '2026-03-20 16:00:58.501290'),
(22, 'authtoken', '0002_auto_20160226_1747', '2026-03-20 16:00:58.522669'),
(23, 'authtoken', '0003_tokenproxy', '2026-03-20 16:00:58.525107'),
(24, 'authtoken', '0004_alter_tokenproxy_options', '2026-03-20 16:00:58.529326'),
(27, 'users', '0002_ojtprofile', '2026-03-20 17:07:41.291039'),
(28, 'users', '0003_delete_user', '2026-03-21 06:43:29.234153'),
(30, 'attendance', '0001_initial', '2026-03-21 09:02:37.114481'),
(31, 'users', '0004_ojtprofile_department_ojtprofile_institution_and_more', '2026-03-21 13:00:14.575582'),
(32, 'users', '0005_ojtprofile_role', '2026-03-22 00:58:56.288099');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('lpe4zeymqobey4ouwy1wpie6ga0y1kpx', '.eJxVjDsOwjAQBe_iGllr_A0lPWewdtc2DiBHipMKcXcSKQW0b2beW0RclxrXnuc4JnERSpx-N0J-5raD9MB2nyRPbZlHkrsiD9rlbUr5dT3cv4OKvW41eueNL-hAZQCjVQGjNFhFAyQbKGi0xDRoQ4YdB8jelk1jKlTONonPF74qN4k:1w3dN3:pTW31Vhpvtu_fjw9mAB43DxFjglKM4XVVpWQ89XTlSk', '2026-04-03 17:10:49.294337');

-- --------------------------------------------------------

--
-- Table structure for table `users_ojtprofile`
--

CREATE TABLE `users_ojtprofile` (
  `id` bigint(20) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `required_hours` decimal(6,2) NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `department` varchar(255) NOT NULL,
  `institution` varchar(255) NOT NULL,
  `intern_type` varchar(100) NOT NULL,
  `profile_image` varchar(100) DEFAULT NULL,
  `program` varchar(255) NOT NULL,
  `supervisor` varchar(255) NOT NULL,
  `trainee_id` varchar(100) NOT NULL,
  `role` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Dumping data for table `users_ojtprofile`
--

INSERT INTO `users_ojtprofile` (`id`, `full_name`, `required_hours`, `start_date`, `end_date`, `user_id`, `department`, `institution`, `intern_type`, `profile_image`, `program`, `supervisor`, `trainee_id`, `role`) VALUES
(10, '', 486.00, NULL, NULL, 12, '', '', '', 'profiles/BB5663E3-44BB-449D-8D40-360FE4364678.jpg', '', '', '', 'supervisor'),
(11, '', 486.00, NULL, NULL, 13, '', '', '', '', '', '', '', 'hr'),
(12, 'Alahdin Ogale', 486.00, '2026-02-02', NULL, 14, 'IT Department', 'Saint Louis College', 'Student', 'profiles/57F84A81-9696-4174-BB28-27C5BEAAB262.jpg', 'BSIT', 'Jonathan Toralba', 'TR-2026-40001', 'intern'),
(13, 'Jann Mevric', 486.00, '2026-02-02', NULL, 15, 'IT Department', 'Saint Louis College', 'Academic', 'profiles/68C5A26E-FDE6-4B82-962D-CD22C9EE635A.jpg', 'BSIT', 'Jonathan Toralba', 'TR-2026-40002', 'intern');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance_attendance`
--
ALTER TABLE `attendance_attendance`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `attendance_attendance_user_id_date_407a5a02_uniq` (`user_id`,`date`);

--
-- Indexes for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD PRIMARY KEY (`key`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `users_ojtprofile`
--
ALTER TABLE `users_ojtprofile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance_attendance`
--
ALTER TABLE `attendance_attendance`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `users_ojtprofile`
--
ALTER TABLE `users_ojtprofile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendance_attendance`
--
ALTER TABLE `attendance_attendance`
  ADD CONSTRAINT `attendance_attendance_user_id_2bd82a2c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `users_ojtprofile`
--
ALTER TABLE `users_ojtprofile`
  ADD CONSTRAINT `users_ojtprofile_user_id_2dab1fbd_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
