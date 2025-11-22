from flask import Blueprint, jsonify, request
from database.conexion import obtener_conexion
from datetime import datetime, timedelta

reservas_bp = Blueprint("reservas", __name__)

# ============================================================
# ==================== LISTAR RESERVAS ========================
# ============================================================

@reservas_bp.route("/reservas", methods=["GET"])
def listar_reservas():
    conn = obtener_conexion()
    cur = conn.cursor(dictionary=True, buffered=True)
    cur.execute("SELECT * FROM reserva;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)


# ============================================================
# ==================== CREAR RESERVA ==========================
# ============================================================

@reservas_bp.route("/reservas", methods=["POST"])
def crear_reserva():
    """
    CREA una reserva aplicando TODAS las validaciones solicitadas:
    - La sala debe existir
    - El turno debe existir
    - La sala no puede estar ocupada en ese turno
    - No superar la capacidad
    - Máximo 2 reservas por día por participante
    - Máximo 3 reservas por semana por participante
    - Insertar participantes en reserva_participante
    - No reservar si hay sanción vigente
    """
    data = request.get_json()

    nombre_sala = data.get("nombre_sala")
    edificio = data.get("edificio")
    fecha_str = data.get("fecha")
    id_turno = data.get("id_turno")
    ci_solicitante = data.get("ci_participante")
    participantes = data.get("participantes") or []

    if ci_solicitante not in participantes:
        participantes.append(ci_solicitante)

    if not nombre_sala or not edificio or not fecha_str or not id_turno or not ci_solicitante:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    try:
        fecha_reserva = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    conn = obtener_conexion()
    cur = conn.cursor(dictionary=True, buffered=True)

    try:
        # VALIDACIÓN 1: Sanción activa
        cur.execute("""
            SELECT fecha_inicio, fecha_fin
            FROM sancion_participante
            WHERE ci_participante = %s
              AND CURDATE() BETWEEN fecha_inicio AND fecha_fin
        """, (ci_solicitante,))
        sancion = cur.fetchone()
        if sancion:
            return jsonify({"error": "El participante está sancionado", "sancion": sancion}), 400

        # VALIDACIÓN 2: Sala existe
        cur.execute("""
            SELECT capacidad, tipo_sala
            FROM sala
            WHERE nombre_sala = %s AND edificio = %s
        """, (nombre_sala, edificio))
        sala = cur.fetchone()
        cur.fetchall()
        if not sala:
            return jsonify({"error": "La sala no existe"}), 400

        capacidad_sala = sala["capacidad"]
        tipo_sala = sala["tipo_sala"]

        # VALIDACIÓN DE TIPO DE SALA
        cur.execute("""
            SELECT ppa.rol, pa.tipo
            FROM participante_programa_academico ppa
            JOIN programa_academico pa ON pa.nombre_programa = ppa.nombre_programa
            WHERE ppa.ci_participante = %s
            LIMIT 1
        """, (ci_solicitante,))
        usuario = cur.fetchone()
        cur.fetchall()

        if not usuario:
            return jsonify({"error": "El participante no tiene un programa académico asociado"}), 400

        rol = usuario["rol"]  # 'alumno' o 'docente'
        tipo_programa = usuario["tipo"]  # 'grado' o 'posgrado'
        tipo_sala = sala["tipo_sala"]  # 'libre', 'posgrado', 'docente'
        # DEFINIR SI EL USUARIO ESTÁ EXENTO DE LÍMITES
        es_exento = False

        # Docentes o posgrado tienen excepción SOLO en salas exclusivas
        if tipo_sala == "posgrado" and (rol == "docente" or tipo_programa == "posgrado"):
            es_exento = True

        if tipo_sala == "docente" and rol == "docente":
            es_exento = True

        # VALIDAR ACCESO A SALAS EXCLUSIVAS
        if tipo_sala == "posgrado" and not es_exento:
            return jsonify({"error": "La sala es exclusiva para docentes o estudiantes de posgrado"}), 403

        if tipo_sala == "docente" and rol != "docente":
            return jsonify({"error": "La sala es exclusiva para docentes"}), 403

        # VALIDACIÓN 3: Turno debe existir
        cur.execute("SELECT id_turno FROM turno WHERE id_turno = %s", (id_turno,))
        if not cur.fetchone():
            return jsonify({"error": "El turno no existe"}), 400
        cur.fetchall()

        # VALIDACIÓN 4: No superar capacidad
        if len(participantes) > capacidad_sala:
            return jsonify({"error": "Supera la capacidad de la sala"}), 400

        # VALIDACIÓN 5: Sala no ocupada
        cur.execute("""
            SELECT id_reserva
            FROM reserva
            WHERE nombre_sala=%s AND edificio=%s
              AND fecha=%s AND id_turno=%s
              AND estado='activa'
        """, (nombre_sala, edificio, fecha_reserva, id_turno))
        if cur.fetchone():
            return jsonify({"error": "La sala ya está reservada en ese turno"}), 400
        cur.fetchall()

        # VALIDACIÓN 6 y 7 — Máx 2 por día / máx 3 por semana
        semana_inicio = fecha_reserva - timedelta(days=fecha_reserva.weekday())
        semana_fin = semana_inicio + timedelta(days=6)

        for ci in participantes:
            # Día
            cur.execute("""
                SELECT COUNT(*) AS c
                FROM reserva r
                JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
                WHERE rp.ci_participante = %s
                  AND r.fecha = %s
                  AND r.estado='activa'
            """, (ci, fecha_reserva))
            if not es_exento and cur.fetchone()["c"] >= 2:
                return jsonify({"error": f"El participante {ci} ya tiene 2 reservas ese día"}), 400
            cur.fetchall()

            # Semana
            cur.execute("""
                SELECT COUNT(*) AS c
                FROM reserva r
                JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
                WHERE rp.ci_participante = %s
                  AND r.fecha BETWEEN %s AND %s
                  AND r.estado='activa'
            """, (ci, semana_inicio, semana_fin))
            if not es_exento and cur.fetchone()["c"] >= 3:
                return jsonify({"error": f"El participante {ci} ya tiene 3 reservas esa semana"}), 400

        # CREAR reserva
        cur.execute("""
            INSERT INTO reserva (nombre_sala, edificio, fecha, id_turno, estado)
            VALUES (%s, %s, %s, %s, 'activa')
        """, (nombre_sala, edificio, fecha_reserva, id_turno))
        id_reserva = cur.lastrowid

        # INSERTAR PARTICIPANTES
        for ci in participantes:
            cur.execute("""
                INSERT INTO reserva_participante
                (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia)
                VALUES (%s, %s, NOW(), 0)
            """, (ci, id_reserva))

        conn.commit()

        return jsonify({
            "mensaje": "Reserva creada con éxito",
            "id_reserva": id_reserva,
            "participantes": participantes
        })

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


# ============================================================
# ==================== BORRAR RESERVA =========================
# ============================================================

@reservas_bp.route("/reservas/<int:id_reserva>", methods=["DELETE"])
def eliminar_reserva(id_reserva):
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("DELETE FROM reserva_participante WHERE id_reserva=%s;", (id_reserva,))
    cur.execute("DELETE FROM reserva WHERE id_reserva=%s;", (id_reserva,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Reserva eliminada"})


# ============================================================
# ==================== REGISTRAR ASISTENCIA ==================
# ============================================================

@reservas_bp.route("/reservas/<int:id_reserva>/asistencia", methods=["POST"])
def registrar_asistencia(id_reserva):
    data = request.get_json()
    ci = data.get("ci_participante")
    asistio_raw = data.get("asistio")   # puede venir como string "0" o "1"

    if ci is None or asistio_raw is None:
        return jsonify({"error": "Faltan datos para registrar asistencia."}), 400

    # 🔥 Conversión segura:
    # solo "1" o 1 es True — todo lo demás es False
    asistio = True if asistio_raw == 1 or str(asistio_raw) == "1" else False

    conn = obtener_conexion()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE reserva_participante
            SET asistencia = %s
            WHERE id_reserva = %s AND ci_participante = %s
        """, (1 if asistio else 0, id_reserva, ci))
        conn.commit()

        return jsonify({"mensaje": "Asistencia registrada correctamente."})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()

# ============================================================
# ======================= FINALIZAR RESERVA ==================
# ============================================================

@reservas_bp.route("/reservas/<int:id_reserva>/finalizar", methods=["POST"])
def finalizar_reserva(id_reserva):
    conn = obtener_conexion()
    cur = conn.cursor(dictionary=True)

    try:
        # Obtener participantes
        cur.execute("""
            SELECT ci_participante, asistencia
            FROM reserva_participante
            WHERE id_reserva = %s
        """, (id_reserva,))
        participantes = cur.fetchall()

        if not participantes:
            return jsonify({"error": "La reserva no tiene participantes."}), 400

        # Ver si alguien asistió
        alguien_asistio = any(p["asistencia"] == 1 for p in participantes)

        # Cambiar estado
        cur.execute("""
            UPDATE reserva
            SET estado = 'finalizada'
            WHERE id_reserva = %s
        """, (id_reserva,))
        conn.commit()

        # Sancionar si nadie asistió
        if not alguien_asistio:
            fecha_inicio = datetime.today().date()
            fecha_fin = fecha_inicio + timedelta(days=60)

            cur2 = conn.cursor()
            for p in participantes:
                cur2.execute("""
                    INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin)
                    VALUES (%s, %s, %s)
                """, (p["ci_participante"], fecha_inicio, fecha_fin))
            conn.commit()

            return jsonify({
                "mensaje": "Reserva finalizada. Nadie asistió, sanciones aplicadas.",
                "sancionados": [p["ci_participante"] for p in participantes]
            })

        return jsonify({"mensaje": "Reserva finalizada correctamente. Hubo asistencia."})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


# ============================================================
# ===================== DETALLE DE RESERVA ====================
# ============================================================

@reservas_bp.route("/reservas/<int:id_reserva>", methods=["GET"])
def obtener_reserva_detalle(id_reserva):
    conn = obtener_conexion()
    cur = conn.cursor(dictionary=True)

    try:
        # Obtener reserva
        cur.execute("""
            SELECT *
            FROM reserva
            WHERE id_reserva = %s
        """, (id_reserva,))
        reserva = cur.fetchone()

        if not reserva:
            return jsonify({"error": "La reserva no existe"}), 404

        # Obtener participantes
        cur.execute("""
            SELECT rp.ci_participante, rp.asistencia,
                   p.nombre, p.apellido, p.email
            FROM reserva_participante rp
            JOIN participante p
            ON p.ci = rp.ci_participante
            WHERE rp.id_reserva = %s
        """, (id_reserva,))
        participantes = cur.fetchall()

        return jsonify({
            "reserva": reserva,
            "participantes": participantes
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()

#        ENDPOINT DE DISPONIBILIDAD

@reservas_bp.route("/disponibilidad", methods=["GET"])
def disponibilidad_sala():
    nombre_sala = request.args.get("sala")
    edificio = request.args.get("edificio")
    fecha_str = request.args.get("fecha")

    if not nombre_sala or not edificio or not fecha_str:
        return jsonify({"error": "Faltan parámetros: sala, edificio o fecha"}), 400

    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except:
        return jsonify({"error": "Formato de fecha inválido (usar YYYY-MM-DD)"}), 400

    conn = obtener_conexion()
    cur = conn.cursor(dictionary=True)

    try:
        # Obtener turnos
        cur.execute("SELECT id_turno, hora_inicio, hora_fin FROM turno;")
        turnos = cur.fetchall()

        # Obtener reservas ocupadas
        cur.execute("""
            SELECT id_turno, estado
            FROM reserva
            WHERE nombre_sala = %s
              AND edificio = %s
              AND fecha = %s
        """, (nombre_sala, edificio, fecha))
        reservas = cur.fetchall()

        ocupados = {r["id_turno"]: r["estado"] for r in reservas}

        resultado = []
        for t in turnos:
            estado = "libre"
            if t["id_turno"] in ocupados:
                if ocupados[t["id_turno"]] == "activa":
                    estado = "ocupado"
                else:
                    estado = ocupados[t["id_turno"]]
            resultado.append({
                "id_turno": t["id_turno"],
                "hora_inicio": str(t["hora_inicio"]),
                "hora_fin": str(t["hora_fin"]),
                "estado": estado
            })

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()
