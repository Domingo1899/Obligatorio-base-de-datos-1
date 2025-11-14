from flask import Flask, jsonify, request
# Flask es el framework web. request permite leer datos enviados al servidor.
# jsonify convierte diccionarios/listas de Python a JSON para el navegador.

from db.conexion import obtener_conexion
# Importamos la función para conectarnos a la base MySQL.

app = Flask(__name__)
# Creamos la aplicación Flask.

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
    CREA una reserva sin validaciones complejas.
    """
    data = request.get_json()
    nombre_sala = data.get("nombre_sala")
    edificio = data.get("edificio")
    fecha = data.get("fecha")
    id_turno = data.get("id_turno")

    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reserva (nombre_sala, edificio, fecha, id_turno, estado)
        VALUES (%s, %s, %s, %s, 'activa')
    """, (nombre_sala, edificio, fecha, id_turno))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Reserva creada"})

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
# ===================== MAIN APP =============================
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)