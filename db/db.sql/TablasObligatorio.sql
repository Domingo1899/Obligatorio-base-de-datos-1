CREATE DATABASE IF NOT EXISTS gestion_salas;
USE gestion_salas;

CREATE TABLE login (
    correo VARCHAR(50) PRIMARY KEY,
    contrasena VARCHAR(70)
);

CREATE TABLE participante (
    ci INT PRIMARY KEY,
    nombre VARCHAR(30),
    apellido VARCHAR(30),
    email VARCHAR(50)
);

CREATE TABLE facultad (
    id_facultad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100)
);

CREATE TABLE programa_academico (
    nombre_programa VARCHAR(100) PRIMARY KEY,
    id_facultad INT,
    tipo ENUM ('grado', 'posgrado'),
    FOREIGN KEY (id_facultad) REFERENCES facultad (id_facultad)
);

CREATE TABLE sala (
    nombre_sala VARCHAR(20) PRIMARY KEY,
    edificio VARCHAR(50),
    capacidad INT,
    tipo_sala ENUM('libre', 'posgrado', 'docente')
);

CREATE TABLE edificio (
    nombre_edificio VARCHAR(50) PRIMARY KEY,
    direccion VARCHAR(200),
    departamento VARCHAR(50)
);

CREATE TABLE turno (
    id_turno INT PRIMARY KEY,
    hora_inicio TIME,
    hora_fin TIME
);

CREATE TABLE if not exists reserva (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    nombre_sala VARCHAR(20),
    edificio VARCHAR(50),
    fecha DATE,
    id_turno INT,
    estado ENUM('activa', 'cancelada', 'sin asistencia', 'finalizada'),
    FOREIGN KEY (nombre_sala) REFERENCES sala(nombre_sala),
    FOREIGN KEY (id_turno) REFERENCES turno(id_turno)
);

CREATE TABLE reserva_participante (
    ci_participante INT,
    id_reserva INT,
    fecha_solicitud_reserva DATE,
    asistencia BOOLEAN,
    PRIMARY KEY (ci_participante, id_reserva),
    FOREIGN KEY (ci_participante) REFERENCES participante(ci),
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

CREATE TABLE sancion_participante (
    ci_participante INT,
    fecha_inicio DATE,
    fecha_fin DATE,
    PRIMARY KEY (ci_participante, fecha_inicio),
    FOREIGN KEY (ci_participante) REFERENCES participante(ci)
);