from flask import Flask, jsonify, request
# Flask es el framework web. request lee datos enviados al servidor.
# jsonify convierte diccionarios/listas de Python a JSON para el navegador.

from db.conexion import obtener_conexion

app = Flask(__name__)


# ============================================================
# =============== RUTA INICIAL ===============================
# ============================================================

@app.route("/")
def inicio():
    """
    Página principal para verificar que el servidor está funcionando.
    """
    return jsonify({
        "mensaje": "API de Reserva de Salas funcionando correctamente",
        "endpoints": [
            "/participantes",
            "/salas",
            "/reservas",
            "/sanciones"
        ]
    })

# ============================================================
# =============== ABM PARTICIPANTE ===========================
# ============================================================

@app.route("/participantes", methods=["GET"])
def listar_participantes():
    """
    LEE (Read): Devuelve todos los participantes.
    """
    conn = obtener_conexion()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM participante;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route("/participantes", methods=["POST"])
def crear_participante():
    """
    CREA (Create): Inserta un nuevo participante.
    """
    data = request.get_json()
    ci = data.get("ci_participante")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")

    if not ci or not nombre or not apellido or not email:
        return jsonify({"error": "Datos incompletos"}), 400

    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO participante (ci_participante, nombre, apellido, email)
        VALUES (%s, %s, %s, %s)
    """, (ci, nombre, apellido, email))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Participante creado correctamente"}), 201

@app.route("/participantes/<int:ci>", methods=["PUT"])
def modificar_participante(ci):
    """
    MODIFICA (Update): Cambia datos de un participante.
    """
    data = request.get_json()
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")

    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("""
        UPDATE participante
        SET nombre=%s, apellido=%s, email=%s
        WHERE ci_participante=%s
    """, (nombre, apellido, email, ci))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Participante actualizado"})

@app.route("/participantes/<int:ci>", methods=["DELETE"])
def eliminar_participante(ci):
    """
    BORRA (Delete): Elimina un participante por CI.
    """
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("DELETE FROM participante WHERE ci_participante=%s;", (ci,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Participante eliminado"})

# ============================================================
# ===================== ABM SALA =============================
# ============================================================

@app.route("/salas", methods=["GET"])
def listar_salas():
    """
    LEE todas las salas.
    """
    conn = obtener_conexion()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM sala;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route("/salas", methods=["POST"])
def crear_sala():
    """
    CREA una sala nueva.
    """
    data = request.get_json()
    nombre = data.get("nombre_sala")
    edificio = data.get("edificio")
    capacidad = data.get("capacidad")
    tipo = data.get("tipo_sala")

    if not nombre or not edificio or not capacidad or not tipo:
        return jsonify({"error": "Datos incompletos"}), 400

    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO sala (nombre_sala, edificio, capacidad, tipo_sala)
        VALUES (%s, %s, %s, %s)
    """, (nombre, edificio, capacidad, tipo))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Sala creada correctamente"})

@app.route("/salas/<string:nombre>/<string:edificio>", methods=["PUT"])
def modificar_sala(nombre, edificio):
    """
    MODIFICA datos de una sala.
    """
    data = request.get_json()
    capacidad = data.get("capacidad")
    tipo = data.get("tipo_sala")

    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("""
        UPDATE sala
        SET capacidad=%s, tipo_sala=%s
        WHERE nombre_sala=%s AND edificio=%s
    """, (capacidad, tipo, nombre, edificio))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Sala modificada"})

@app.route("/salas/<string:nombre>/<string:edificio>", methods=["DELETE"])
def eliminar_sala(nombre, edificio):
    """
    ELIMINA una sala.
    """
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM sala
        WHERE nombre_sala=%s AND edificio=%s
    """, (nombre, edificio))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Sala eliminada"})

# ============================================================
# ==================== ABM RESERVAS ==========================
# ============================================================

@app.route("/reservas", methods=["GET"])
def listar_reservas():
    """
    LEE todas las reservas.
    """
    conn = obtener_conexion()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM reserva;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route("/reservas", methods=["POST"])
def crear_reserva():
    """
    CREA una reserva aplicando TODAS las validaciones solicitadas:
    - La sala debe existir
    - El turno debe existir
    - La sala no puede estar ocupada en ese día/turno
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
    cur = conn.cursor(dictionary=True)

    try:
        # VALIDACIÓN 1:No permitir reservar si el participante está sancionado
        cur.execute("""
            SELECT fecha_inicio, fecha_fin
            FROM sancion_participante
            WHERE ci_participante = %s
              AND CURDATE() BETWEEN fecha_inicio AND fecha_fin
        """, (ci_solicitante,))
        sancion = cur.fetchone()
        if sancion:
            return jsonify({
                "error": "El participante está sancionado",
                "sancion": sancion
            }), 400

        # VALIDACIÓN 2:Sala debe existir
        cur.execute("""
            SELECT capacidad
            FROM sala
            WHERE nombre_sala = %s AND edificio = %s
        """, (nombre_sala, edificio))
        sala = cur.fetchone()
        if not sala:
            return jsonify({"error": "La sala no existe"}), 400
        capacidad_sala = sala["capacidad"]

        # VALIDACIÓN 3:Turno debe existir
        cur.execute("SELECT id_turno FROM turno WHERE id_turno = %s", (id_turno,))
        if not cur.fetchone():
            return jsonify({"error": "El turno no existe"}), 400

        # VALIDACIÓN 4:No superar capacidad
        if len(participantes) > capacidad_sala:
            return jsonify({"error": "Supera la capacidad de la sala"}), 400

        # VALIDACIÓN 5:Sala no ocupada
        cur.execute("""
            SELECT id_reserva
            FROM reserva
            WHERE nombre_sala=%s AND edificio=%s
              AND fecha=%s AND id_turno=%s
              AND estado='activa'
        """, (nombre_sala, edificio, fecha_reserva, id_turno))
        if cur.fetchone():
            return jsonify({"error": "La sala ya está reservada en ese turno"}), 400

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
            if cur.fetchone()["c"] >= 2:
                return jsonify({"error": f"El participante {ci} ya tiene 2 reservas ese día"}), 400

            # Semana
            cur.execute("""
                SELECT COUNT(*) AS c
                FROM reserva r
                JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
                WHERE rp.ci_participante = %s
                  AND r.fecha BETWEEN %s AND %s
                  AND r.estado='activa'
            """, (ci, semana_inicio, semana_fin))
            if cur.fetchone()["c"] >= 3:
                return jsonify({"error": f"El participante {ci} ya tiene 3 reservas esa semana"}), 400

        # CREAR RESERVA
        cur2 = conn.cursor()
        cur2.execute("""
            INSERT INTO reserva (nombre_sala, edificio, fecha, id_turno, estado)
            VALUES (%s, %s, %s, %s, 'activa')
        """, (nombre_sala, edificio, fecha_reserva, id_turno))
        conn.commit()
        id_reserva = cur2.lastrowid

        # INSERTAR PARTICIPANTES
        for ci in participantes:
            cur2.execute("""
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

@app.route("/reservas/<int:id_reserva>", methods=["DELETE"])
def eliminar_reserva(id_reserva):
    """
    ELIMINA una reserva y sus participantes asociados.
    """
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("DELETE FROM reserva_participante WHERE id_reserva=%s;", (id_reserva,))
    cur.execute("DELETE FROM reserva WHERE id_reserva=%s;", (id_reserva,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Reserva eliminada"})

# ============================================================
# ==================== ABM SANCIONES =========================
# ============================================================

@app.route("/sanciones", methods=["GET"])
def listar_sanciones():
    conn = obtener_conexion()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM sancion_participante;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route("/sanciones", methods=["POST"])
def crear_sancion():
    data = request.get_json()
    ci = data.get("ci_participante")
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")

    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin)
        VALUES (%s, %s, %s)
    """, (ci, fecha_inicio, fecha_fin))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Sanción creada"})

@app.route("/sanciones/<int:ci>", methods=["DELETE"])
def eliminar_sancion(ci):
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("DELETE FROM sancion_participante WHERE ci_participante=%s;", (ci,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Sanción eliminada"})

# ============================================================
# =============== ASISTENCIAS Y SANCIONES ====================
# ============================================================

from datetime import datetime, timedelta

@app.route("/reservas/<int:id_reserva>/asistencia", methods=["POST"])
def registrar_asistencia(id_reserva):
    """
    Marca asistencia de un participante en una reserva.
    Espera:
    {
        "ci_participante": 12345678,
        "asistio": true/false
    }
    """
    data = request.get_json()
    ci = data.get("ci_participante")
    asistio = data.get("asistio")

    if ci is None or asistio is None:
        return jsonify({"error": "Faltan datos para registrar asistencia."}), 400

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


@app.route("/reservas/<int:id_reserva>/finalizar", methods=["POST"])
def finalizar_reserva(id_reserva):
    """
    Finaliza una reserva.
    - Cambia estado a 'finalizada'
    - Si todos los participantes faltaron -> se crean sanciones de 60 días
    """
    conn = obtener_conexion()
    cur = conn.cursor(dictionary=True)

    try:
        #Verificar asistencia
        cur.execute("""
            SELECT ci_participante, asistencia
            FROM reserva_participante
            WHERE id_reserva = %s
        """, (id_reserva,))
        participantes = cur.fetchall()

        if not participantes:
            return jsonify({"error": "La reserva no tiene participantes."}), 400

        #Verificar si alguien asistió
        alguien_asistio = any(p["asistencia"] == 1 for p in participantes)

        #Termianrar la reserva
        cur.execute("""
            UPDATE reserva
            SET estado = 'finalizada'
            WHERE id_reserva = %s
        """, (id_reserva,))
        conn.commit()

        #Sanción 60 días si alguien no asistió
        if not alguien_asistio:
            fecha_inicio = datetime.today().date()
            fecha_fin = fecha_inicio + timedelta(days=60)

            cur = conn.cursor()
            for p in participantes:
                cur.execute("""
                    INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin)
                    VALUES (%s, %s, %s)
                """, (p["ci_participante"], fecha_inicio, fecha_fin))
            conn.commit()

            return jsonify({
                "mensaje": "Reserva finalizada. Nadie asistió, sanciones aplicadas.",
                "sancionados": [p["ci_participante"] for p in participantes]
            })

        return jsonify({
            "mensaje": "Reserva finalizada correctamente. Hubo asistencia."
        })

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()

# ============================================================
# ======== VER DETALLE DE UNA RESERVA CON PARTICIPANTES ======
# ============================================================

@app.route("/reservas/<int:id_reserva>", methods=["GET"])
def obtener_reserva_detalle(id_reserva):
    """
    Devuelve una reserva con la lista de sus participantes y asistencias.
    """
    conn = obtener_conexion()
    cur = conn.cursor(dictionary=True)

    try:
        # Obtener la reserva
        cur.execute("""
            SELECT *
            FROM reserva
            WHERE id_reserva = %s
        """, (id_reserva,))
        reserva = cur.fetchone()

        if not reserva:
            cur.close()
            conn.close()
            return jsonify({"error": "La reserva no existe"}), 404

        # Obtener participantes
        cur.execute("""
            SELECT rp.ci_participante, rp.asistencia,
                   p.nombre, p.apellido, p.email
            FROM reserva_participante rp
            JOIN participante p
            ON p.ci_participante = rp.ci_participante
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

# ============================================================
# ===================== MAIN APP =============================
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)