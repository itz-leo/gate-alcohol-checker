-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 26-10-2025 a las 10:00:18
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bottle_handling`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `botellas_circulacion`
--

CREATE TABLE `botellas_circulacion` (
  `ID` int(11) NOT NULL,
  `ID_Botella` int(11) NOT NULL,
  `Aerolinea_Actual` varchar(40) NOT NULL,
  `Porcentaje_Actual` int(4) NOT NULL,
  `Estado_Sellado` varchar(100) NOT NULL,
  `Estado_etiqueta` varchar(100) NOT NULL,
  `Vuelo_entrante` varchar(10) NOT NULL,
  `Accion` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `botellas_circulacion`
--

INSERT INTO `botellas_circulacion` (`ID`, `ID_Botella`, `Aerolinea_Actual`, `Porcentaje_Actual`, `Estado_Sellado`, `Estado_etiqueta`, `Vuelo_entrante`, `Accion`) VALUES
(1, 2, 'PatoVuelo', 100, 'Buen estado', 'Nueva', '100', 'KEEP'),
(2, 3, 'EsenciaVuelos', 80, 'Buen estado', 'Poco desgastada', '100', 'FILL'),
(3, 1, 'PatoVuelo', 84, 'Mal estado', 'Muy desgastada', '1', 'DISCARD');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `botellas_nuevas`
--

CREATE TABLE `botellas_nuevas` (
  `ID` int(11) NOT NULL,
  `Nombre` varchar(40) NOT NULL,
  `Contenido_net` int(5) NOT NULL,
  `Peso` int(5) NOT NULL,
  `Categoria` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `botellas_nuevas`
--

INSERT INTO `botellas_nuevas` (`ID`, `Nombre`, `Contenido_net`, `Peso`, `Categoria`) VALUES
(1, 'Kahlúa Liqueur ', 750, 900, 'Liqueur'),
(2, 'Penfolds Wine ', 1000, 1100, 'Wine'),
(3, 'Johnnie Walker Spirits ', 1000, 1300, 'Spirits');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sla_policy`
--

CREATE TABLE `sla_policy` (
  `ID` int(11) NOT NULL,
  `Aerolinea` varchar(40) NOT NULL,
  `Estatus_Sello` varchar(30) NOT NULL,
  `Estatus_etiqueta` varchar(30) NOT NULL,
  `Limpieza` varchar(30) NOT NULL,
  `Porcentaje_Contenido` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sla_policy`
--

INSERT INTO `sla_policy` (`ID`, `Aerolinea`, `Estatus_Sello`, `Estatus_etiqueta`, `Limpieza`, `Porcentaje_Contenido`) VALUES
(1, 'PatoVuelo', 'Sellado', 'Ligero daño', 'Aceptable', '80'),
(2, 'EsenciaVuelos', 'Resellado', 'Intacto', 'Excelente', '60'),
(3, 'AguilaVuelo', 'Abierto', 'Alto daño', 'Aceptable', '70');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `full_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `full_name`) VALUES
(1, 'admin', 'admin', 'Admin User');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `botellas_circulacion`
--
ALTER TABLE `botellas_circulacion`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `ID_Botella` (`ID_Botella`);

--
-- Indices de la tabla `botellas_nuevas`
--
ALTER TABLE `botellas_nuevas`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `sla_policy`
--
ALTER TABLE `sla_policy`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `botellas_circulacion`
--
ALTER TABLE `botellas_circulacion`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `botellas_nuevas`
--
ALTER TABLE `botellas_nuevas`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `sla_policy`
--
ALTER TABLE `sla_policy`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `botellas_circulacion`
--
ALTER TABLE `botellas_circulacion`
  ADD CONSTRAINT `botellas_circulacion_ibfk_1` FOREIGN KEY (`ID_Botella`) REFERENCES `botellas_nuevas` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
