-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Erstellungszeit: 16. Jun 2024 um 13:43
-- Server-Version: 5.7.39
-- PHP-Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

USE `WS-AI-VS`;

-- USER
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `password` varchar(89) NOT NULL,
  `email` varchar(256) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- VIDEOS
CREATE TABLE `videos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `path` varchar(255) NOT NULL,
  `user` int(11) NOT NULL,
  `folder` varchar(80) NOT NULL,
  `time` int(10) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user`) REFERENCES `user`(`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



-- LANGUAGE
CREATE TABLE `language` (
  `language_code` varchar(4) NOT NULL,
  `language_name` varchar(80) NOT NULL,
  PRIMARY KEY (`language_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Daten für Tabelle `language`
INSERT INTO `language` (`language_code`, `language_name`) VALUES
('en', 'english'),
('ger', 'german'),
('es', 'spanish'),
('fr', 'french'),
('pt', 'portuguese'),
('it', 'italian');
COMMIT;
