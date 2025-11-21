USE gestion_salas;
#Top salas mas reservadas:
#Agrupa por sala y usa COUNT(*) para saber cuántas reservas tuvo cada una.
SELECT nombre_sala, edificio, COUNT(*) AS total_reservas
FROM reserva
GROUP BY nombre_sala, edificio
ORDER BY total_reservas DESC
LIMIT 10;

#Turnos mas demandados:
#Hace JOIN con turno para obtener el horario y COUNT(*) para medir cuántas veces se reservó.
SELECT t.id_turno, t.hora_inicio, t.hora_fin, COUNT(*) AS cantidad
FROM reserva r
         JOIN turno t ON r.id_turno = t.id_turno
GROUP BY t.id_turno, t.hora_inicio, t.hora_fin
ORDER BY cantidad DESC;

#Promedio de Participantes por sala:
#Usa una subconsulta para contar participantes por reserva y luego AVG() para sacar el promedio por sala.
SELECT r.nombre_sala, r.edificio, AVG(cantidad) AS promedio_participantes
FROM (
         SELECT id_reserva, COUNT(*) AS cantidad
         FROM reserva_participante
         GROUP BY id_reserva
     ) p
         JOIN reserva r ON r.id_reserva = p.id_reserva
GROUP BY r.nombre_sala, r.edificio;

#Participantes con mas reservas:
#Une reservas con participantes vía JOIN y usa COUNT(*) para ver quién reservó más.
SELECT p.ci, p.nombre, p.apellido, COUNT(*) AS total_reservas
FROM participante p
         JOIN reserva_participante rp ON p.ci = rp.ci_participante
GROUP BY p.ci, p.nombre, p.apellido
ORDER BY total_reservas DESC;

#Salas con mas ocupacion:
#Cuenta participantes por reserva (subconsulta), une con salas y calcula el promedio de ocupación con AVG().
SELECT r.nombre_sala, r.edificio,
       AVG(p.cant) AS ocupacion_promedio
FROM reserva r
         JOIN (
    SELECT id_reserva, COUNT(*) AS cant
    FROM reserva_participante
    GROUP BY id_reserva
) p ON p.id_reserva = r.id_reserva
GROUP BY r.nombre_sala, r.edificio
ORDER BY ocupacion_promedio DESC;

###Salas mas usadas segun el dia de la semana:
#Usa DAYNAME() para agrupar reservas por día.
SELECT DAYNAME(fecha) AS dia, nombre_sala, COUNT(*)
FROM reserva
GROUP BY dia, nombre_sala;

###Participantes que nunca faltaron
#Filtra los que no aparecen en la lista de faltas.
SELECT *
FROM participante
WHERE ci NOT IN (
    SELECT ci_participante FROM reserva_participante WHERE asistencia = FALSE
);

###Edificios con mas demanda:
#Cuenta reservas agrupadas por edificio para ver el más usado.
SELECT edificio, COUNT(*)
FROM reserva
GROUP BY edificio
ORDER BY COUNT(*) DESC;
