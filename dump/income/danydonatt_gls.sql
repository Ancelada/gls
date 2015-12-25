-- phpMyAdmin SQL Dump
-- version 4.4.6.1
-- http://www.phpmyadmin.net
--
-- Хост: taurus.shared
-- Время создания: Дек 25 2015 г., 09:30
-- Версия сервера: 5.5.45-MariaDB
-- Версия PHP: 5.4.45-pl0-gentoo

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- База данных: `danydonatt_gls`
--

-- --------------------------------------------------------

--
-- Структура таблицы `DataType`
--

CREATE TABLE IF NOT EXISTS `DataType` (
  `id` int(11) NOT NULL,
  `DataTypeName` varchar(200) NOT NULL,
  `DjangoFormat` varchar(200) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `DataType`
--


-- --------------------------------------------------------

--
-- Структура таблицы `Field_Definition_Message`
--

CREATE TABLE IF NOT EXISTS `Field_Definition_Message` (
  `id` int(11) NOT NULL,
  `Field_Definition_MessageName` varchar(200) NOT NULL,
  `LengthMin` int(11) NOT NULL,
  `XmlTag` varchar(50) NOT NULL,
  `LengthMax` int(11) NOT NULL,
  `DataType_id` int(11) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `Field_Definition_Message`
--


-- --------------------------------------------------------

--
-- Структура таблицы `Metka`
--

CREATE TABLE IF NOT EXISTS `Metka` (
  `id` int(11) NOT NULL,
  `text` varchar(200) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `Metka`
--


--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `DataType`
--

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `DataType`
--
ALTER TABLE `DataType`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT для таблицы `Field_Definition_Message`
--
ALTER TABLE `Field_Definition_Message`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=12;
--
-- AUTO_INCREMENT для таблицы `Metka`
--
ALTER TABLE `Metka`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=4;
--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `Field_Definition_Message`
--
ALTER TABLE `Field_Definition_Message`
  ADD CONSTRAINT `Field_Definition_Mes_DataType_id_5d4b714ced2f761e_fk_DataType_id` FOREIGN KEY (`DataType_id`) REFERENCES `DataType` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
