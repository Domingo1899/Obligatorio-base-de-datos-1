from flask import Blueprint, jsonify, request
from database.conexion import obtener_conexion


salas_bp = Blueprint("salas", __name__)

@salas_bp.route("/salas", methods=["GET"])
def listar_salas():
    conn = obtener_conexion()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM sala;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@salas_bp.route("/salas", methods=["POST"])
def crear_sala():
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

@salas_bp.route("/salas/<string:nombre>/<string:edificio>", methods=["PUT"])
def modificar_sala(nombre, edificio):
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

@salas_bp.route("/salas/<string:nombre>/<string:edificio>", methods=["DELETE"])
def eliminar_sala(nombre, edificio):
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
