from flask import Blueprint, jsonify, request
from database.conexion import obtener_conexion

participantes_bp = Blueprint("participantes", __name__)

@participantes_bp.route("/participantes", methods=["GET"])
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

@participantes_bp.route("/participantes", methods=["POST"])
def crear_participante():
    """
    CREA (Create): Inserta un nuevo participante.
    """
    data = request.get_json()
    ci = data.get("ci")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")

    if not ci or not nombre or not apellido or not email:
        return jsonify({"error": "Datos incompletos"}), 400

    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO participante (ci, nombre, apellido, email)
        VALUES (%s, %s, %s, %s)
    """, (ci, nombre, apellido, email))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Participante creado correctamente"}), 201

@participantes_bp.route("/participantes/<int:ci>", methods=["PUT"])
def modificar_participante(ci):
    data = request.get_json()
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")

    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("""
        UPDATE participante
        SET nombre=%s, apellido=%s, email=%s
        WHERE ci=%s
    """, (nombre, apellido, email, ci))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Participante actualizado"})

@participantes_bp.route("/participantes/<int:ci>", methods=["DELETE"])
def eliminar_participante(ci):
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("DELETE FROM participante WHERE ci=%s;", (ci,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Participante eliminado"})
