USE gestion_salas;

DELETE FROM sancion_participante;
DELETE FROM reserva_participante;
DELETE FROM reserva;
DELETE FROM login;
DELETE FROM programa_academico;
DELETE FROM sala;
DELETE FROM edificio;
DELETE FROM turno;
DELETE FROM participante;
DELETE FROM facultad;
ALTER TABLE reserva AUTO_INCREMENT = 1;
ALTER TABLE facultad AUTO_INCREMENT = 1;

INSERT INTO facultad (id_facultad, nombre)
VALUES
    (1, 'Ingeniería y Tecnologías'),
    (2, 'Ciencias de la Salud'),
    (3, 'Ciencias Empresariales'),
    (4, 'Derecho'),
    (5, 'Humanidades');

INSERT INTO programa_academico (nombre_programa, id_facultad, tipo)
VALUES
    ('Ingeniería en Informática', 1, 'grado'),
    ('Ingeniería Civil', 1, 'grado'),
    ('Maestría en Data Science', 1, 'posgrado'),
    ('Medicina', 2, 'grado'),
    ('Enfermería', 2, 'grado'),
    ('Administración de Empresas', 3, 'grado'),
    ('Ingenieria en IA', 3, 'posgrado'),
    ('Derecho', 4, 'grado'),
    ('Psicología', 5, 'grado');

INSERT INTO participante (ci, nombre, apellido, email)
VALUES
    (56599827, 'Juan', 'Pérez', 'juan.perez@ucu.edu.uy'),
    (12345678, 'María', 'Gómez', 'maria.gomez@ucu.edu.uy'),
    (87654321, 'Carlos', 'López', 'carlos.lopez@ucu.edu.uy'),
    (11223344, 'Ana', 'Rodríguez', 'ana.rodriguez@ucu.edu.uy'),
    (44332211, 'Pedro', 'Martínez', 'pedro.martinez@ucu.edu.uy'),
    (55667788, 'Laura', 'Fernández', 'laura.fernandez@ucu.edu.uy'),
    (99887766, 'Diego', 'Silva', 'diego.silva@ucu.edu.uy'),
    (33445566, 'Carmen', 'Díaz', 'carmen.diaz@ucu.edu.uy');

INSERT INTO edificio (nombre_edificio, direccion, departamento)
VALUES
    ('Central', 'Av. 8 de Octubre', 'Montevideo'),
    ('Mullin', 'Av. 8 de Octubre', 'Montevideo'),
    ('Sacre Coeur', 'Av. 8 de Octubre', 'San José'),
    ('Pocitos', 'Av. 8 de Octubre', 'Montevideo'),
    ('San Ignacio', 'Av. 8 de Octubre', 'Montevideo');

INSERT INTO sala (nombre_sala, edificio, capacidad, tipo_sala)
VALUES
    ('Sala1', 'Central', 10, 'libre'),
    ('Sala2', 'Mullin', 5, 'posgrado'),
    ('Sala3', 'San Ignacio', 8, 'docente'),
    ('Sala4', 'San Ignacio', 15, 'libre'),
    ('Sala5', 'Pocitos', 6, 'posgrado'),
    ('Sala6', 'Sacre Coeur', 12, 'docente'),
    ('Sala7', 'Mullin', 20, 'libre'),
    ('Sala8', 'San Ignacio', 4, 'posgrado');

INSERT INTO turno (id_turno, hora_inicio, hora_fin)
VALUES
    (1, '08:00:00', '09:00:00'),
    (2, '09:00:00', '10:00:00'),
    (3, '10:00:00', '11:00:00'),
    (4, '11:00:00', '12:00:00'),
    (5, '12:00:00', '13:00:00'),
    (6, '13:00:00', '14:00:00'),
    (7, '14:00:00', '15:00:00'),
    (8, '15:00:00', '16:00:00'),
    (9, '16:00:00', '17:00:00'),
    (10, '17:00:00', '18:00:00'),
    (11, '18:00:00', '19:00:00'),
    (12, '19:00:00', '20:00:00'),
    (13, '20:00:00', '21:00:00'),
    (14, '21:00:00', '22:00:00'),
    (15, '22:00:00', '23:00:00');

INSERT INTO login (correo, contrasena)
VALUES
    ('juan.perez@ucu.edu.uy', 'password123'),
    ('maria.gomez@ucu.edu.uy', 'password123'),
    ('carlos.lopez@ucu.edu.uy', 'password123'),
    ('ana.rodriguez@ucu.edu.uy', 'password123'),
    ('pedro.martinez@ucu.edu.uy', 'password123'),
    ('laura.fernandez@ucu.edu.uy', 'password123'),
    ('diego.silva@ucu.edu.uy', 'password123'),
    ('carmen.diaz@ucu.edu.uy', 'password123');

INSERT INTO reserva (nombre_sala, edificio, fecha, id_turno, estado)
VALUES
    ('Sala1', 'San Ignacio', '2025-11-01', 1, 'activa'),
    ('Sala2', 'Mullin', '2025-11-01', 2, 'activa'),
    ('Sala3', 'Sacre Coeur', '2025-11-02', 3, 'finalizada'),
    ('Sala4', 'San José', '2025-11-02', 4, 'cancelada'),
    ('Sala1', 'Sacre Coeur', '2025-11-03', 5, 'activa'),
    ('Sala5', 'Pocitos', '2025-11-03', 6, 'sin asistencia'),
    ('Sala6', 'San Ignacio', '2025-11-04', 7, 'activa'),
    ('Sala7', 'Mullin', '2025-11-04', 8, 'finalizada');

INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia)
VALUES
    (56599827, 1, '2025-10-30', FALSE),
    (12345678, 1, '2025-10-30', FALSE),
    (87654321, 2, '2025-10-29', TRUE),
    (11223344, 3, '2025-10-28', TRUE),
    (44332211, 3, '2025-10-28', FALSE),
    (55667788, 4, '2025-10-27', FALSE),
    (99887766, 5, '2025-10-26', TRUE),
    (33445566, 6, '2025-10-25', FALSE),
    (56599827, 7, '2025-10-24', TRUE),
    (12345678, 8, '2025-10-23', TRUE);

INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin)
VALUES
    (55667788, '2025-10-01', '2025-12-01'),
    (33445566, '2025-09-15', '2025-11-15');
