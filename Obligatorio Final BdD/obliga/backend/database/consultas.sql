USE gestion_salas;

# 1) Salas más reservadas
SELECT nombre_sala, edificio, COUNT(*) AS total_reservas
FROM reserva
GROUP BY nombre_sala, edificio
ORDER BY total_reservas DESC;

# 2) Turnos más demandados
SELECT t.id_turno, t.hora_inicio, t.hora_fin, COUNT(*) AS cantidad
FROM reserva r
         JOIN turno t ON r.id_turno = t.id_turno
GROUP BY t.id_turno, t.hora_inicio, t.hora_fin
ORDER BY cantidad DESC;

# 3) Promedio de participantes por sala
SELECT r.nombre_sala, r.edificio, AVG(p.cantidad) AS promedio_participantes
FROM (
         SELECT id_reserva, COUNT(*) AS cantidad
         FROM reserva_participante
         GROUP BY id_reserva
     ) p
         JOIN reserva r ON r.id_reserva = p.id_reserva
GROUP BY r.nombre_sala, r.edificio;

# 4) Cantidad de reservas por carrera y facultad
SELECT fa.nombre AS facultad,
       pa.nombre_programa AS programa,
       COUNT(*) AS total_reservas
FROM reserva r
         JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
         JOIN participante_programa_academico ppa ON ppa.ci_participante = rp.ci_participante
         JOIN programa_academico pa ON pa.nombre_programa = ppa.nombre_programa
         JOIN facultad fa ON fa.id_facultad = pa.id_facultad
GROUP BY facultad, programa
ORDER BY total_reservas DESC;

# 5) Porcentaje de ocupación de salas por edificio
SELECT e.nombre_edificio,
       COUNT(r.id_reserva) AS reservas_en_edificio,
       ROUND((COUNT(r.id_reserva) * 100.0) / (SELECT COUNT(*) FROM reserva), 2) AS porcentaje_ocupacion
FROM reserva r
         JOIN edificio e ON e.nombre_edificio = r.edificio
GROUP BY e.nombre_edificio;

# 6) Cantidad de reservas y asistencias de profesores y alumnos (grado y posgrado)
SELECT ppa.rol,
       pa.tipo AS tipo_academico,
       COUNT(DISTINCT rp.id_reserva) AS total_reservas,
       SUM(rp.asistencia = TRUE) AS total_asistencias
FROM reserva_participante rp
         JOIN participante_programa_academico ppa ON ppa.ci_participante = rp.ci_participante
         JOIN programa_academico pa ON pa.nombre_programa = ppa.nombre_programa
GROUP BY ppa.rol, pa.tipo
ORDER BY ppa.rol, pa.tipo;

# 7) Cantidad de sanciones para profesores y alumnos (grado y posgrado)
SELECT ppa.rol,
       pa.tipo AS tipo_academico,
       COUNT(*) AS total_sanciones
FROM sancion_participante sp
         JOIN participante_programa_academico ppa ON ppa.ci_participante = sp.ci_participante
         JOIN programa_academico pa ON pa.nombre_programa = ppa.nombre_programa
GROUP BY ppa.rol, pa.tipo
ORDER BY total_sanciones DESC;

# 8) % reservas utilizadas vs canceladas/no asistidas
SELECT
    (SELECT COUNT(*) FROM reserva WHERE estado = 'finalizada') AS usadas,
    (SELECT COUNT(*) FROM reserva WHERE estado IN ('cancelada', 'sin asistencia')) AS no_usadas,
    COUNT(*) AS total,
    ROUND((SELECT COUNT(*) FROM reserva WHERE estado = 'finalizada') * 100.0 / COUNT(*), 2)
        AS porcentaje_usadas
FROM reserva;

# 9) Consulta sugerida #1: Participantes que nunca faltaron
SELECT p.ci, p.nombre, p.apellido
FROM participante p
WHERE p.ci NOT IN (
    SELECT ci_participante
    FROM reserva_participante
    WHERE asistencia = FALSE
);

# 10) Consulta sugerida #2: Salas más usadas según el día de la semana
SELECT DAYNAME(fecha) AS dia, nombre_sala, COUNT(*) AS total
FROM reserva
GROUP BY dia, nombre_sala
ORDER BY dia, total DESC;

# 11) Consulta sugerida #3: Edificios con mayor actividad
SELECT edificio, COUNT(*) AS total_reservas
FROM reserva
GROUP BY edificio
ORDER BY total_reservas DESC;
