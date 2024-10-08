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
('zh', 'chinese'),
('de', 'german'),
('es', 'spanish'),
('ru', 'russian'),
('ko', 'korean'),
('fr', 'french'),
('ja', 'japanese'),
('pt', 'portuguese'),
('tr', 'turkish'),
('pl', 'polish'),
('ca', 'catalan'),
('nl', 'dutch'),
('ar', 'arabic'),
('sv', 'swedish'),
('it', 'italian'),
('id', 'indonesian'),
('hi', 'hindi'),
('fi', 'finnish'),
('vi', 'vietnamese'),
('he', 'hebrew'),
('uk', 'ukrainian'),
('el', 'greek'),
('ms', 'malay'),
('cs', 'czech'),
('ro', 'romanian'),
('da', 'danish'),
('hu', 'hungarian'),
('ta', 'tamil'),
('no', 'norwegian'),
('th', 'thai'),
('ur', 'urdu'),
('hr', 'croatian'),
('bg', 'bulgarian'),
('lt', 'lithuanian'),
('la', 'latin'),
('mi', 'maori'),
('ml', 'malayalam'),
('cy', 'welsh'),
('sk', 'slovak'),
('te', 'telugu'),
('fa', 'persian'),
('lv', 'latvian'),
('bn', 'bengali'),
('sr', 'serbian'),
('az', 'azerbaijani'),
('sl', 'slovenian'),
('kn', 'kannada'),
('et', 'estonian'),
('mk', 'macedonian'),
('br', 'breton'),
('eu', 'basque'),
('is', 'icelandic'),
('hy', 'armenian'),
('ne', 'nepali'),
('mn', 'mongolian'),
('bs', 'bosnian'),
('kk', 'kazakh'),
('sq', 'albanian'),
('sw', 'swahili'),
('gl', 'galician'),
('mr', 'marathi'),
('pa', 'punjabi'),
('si', 'sinhala'),
('km', 'khmer'),
('sn', 'shona'),
('yo', 'yoruba'),
('so', 'somali'),
('af', 'afrikaans'),
('oc', 'occitan'),
('ka', 'georgian'),
('be', 'belarusian'),
('tg', 'tajik'),
('sd', 'sindhi'),
('gu', 'gujarati'),
('am', 'amharic'),
('yi', 'yiddish'),
('lo', 'lao'),
('uz', 'uzbek'),
('fo', 'faroese'),
('ht', 'haitian creole'),
('ps', 'pashto'),
('tk', 'turkmen'),
('nn', 'nynorsk'),
('mt', 'maltese'),
('sa', 'sanskrit'),
('lb', 'luxembourgish'),
('my', 'myanmar'),
('bo', 'tibetan'),
('tl', 'tagalog'),
('mg', 'malagasy'),
('as', 'assamese'),
('tt', 'tatar'),
('ha', 'hausa'),
('ba', 'bashkir'),
('jw', 'javanese'),
('su', 'sundanese'),
('yue', 'cantonese');
COMMIT;
