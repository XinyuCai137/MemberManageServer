DROP DATABASE IF EXISTS chorus;

CREATE DATABASE chorus;

USE chorus;

GRANT SELECT, INSERT, UPDATE, DELETE ON awesome.* TO 'www-data'@'localhost' identified BY 'www-data';

CREATE TABLE interviewers (
    `stu_id` VARCHAR(10) NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    `name` VARCHAR(10) NOT NULL,
    `sex` VARCHAR(10) NOT NULL,
    `school` VARCHAR(30) NOT NULL,
    `admin` BOOL NOT NULL,
    `created_at` REAL NOT NULL,
    UNIQUE KEY `idx_email` (`email`),
    KEY `idx_created_at` (`created_at`),
    PRIMARY KEY (`stu_id`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE interviews (
	`stu_id` VARCHAR(50) NOT NULL, 
	`grade_1` INT,
	`graee_2` INT,
	`grade_3` INT,
	`graee_4` INT,
	`grade_5` INT,
	`extra` VARCHAR(500),
	PRIMARY KEY (`stu_id`)
) ENGINE=innodb DEFAULT CHARSET=utf8;
CREATE TABLE members (
    `stu_id` VARCHAR(10) NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    `passwd` VARCHAR(50) NOT NULL,
    `name` VARCHAR(10) NOT NULL,
    `sex` VARCHAR(10) NOT NULL, 
    `school` VARCHAR(30) NOT NULL,
    `grade` VARCHAR(10) NOT NULL,
    `voice_part` VARCHAR(2) NOT NULL,
    `department` VARCHAR(10) NOT NULL,
    `phone` VARCHAR(20) NOT NULL,
    `admin` BOOL NOT NULL,
    `image` VARCHAR(500) NOT NULL,
    `created_at` REAL NOT NULL,
    UNIQUE KEY `idx_email` (`email`),
    KEY `idx_created_at` (`created_at`),
    PRIMARY KEY (`stu_id`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE schools (
	`school` VARCHAR(30) NOT NULL,
	`campus` VARCHAR(10) NOT NULL,
    PRIMARY KEY (`school`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE voice_parts (
    `voice_part` VARCHAR(2) NOT NULL,
	`vp_lead1` VARCHAR(10) NOT NULL,
	`vp_lead2` VARCHAR(10),
    PRIMARY KEY (`voice_part`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE departments (
    `department` VARCHAR(10) NOT NULL,
    `dep_lead` VARCHAR(10) NOT NULL,
    PRIMARY KEY (`department`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

