from flask import Blueprint, jsonify, request
from database.conexion import obtener_conexion

sanciones_bp = Blueprint("sanciones", __name__)

@sanciones_bp.route("/sanciones", methods=["GET"])
def listar_sanciones():
    conn = obtener_conexion()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM sancion_participante;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@sanciones_bp.route("/sanciones", methods=["POST"])
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

@sanciones_bp.route("/sanciones/<int:ci>", methods=["DELETE"])
def eliminar_sancion(ci):
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("DELETE FROM sancion_participante WHERE ci_participante=%s;", (ci,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Sanción eliminada"})
