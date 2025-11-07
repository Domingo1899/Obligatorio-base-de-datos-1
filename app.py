from flask import Flask, jsonify
# Importa Flask, que es el framework web para crear la aplicación,
# y jsonify, que convierte los datos en formato JSON para que el navegador los entienda.

from db.conexion import obtener_conexion
# Importa la función 'obtener_conexion' desde el archivo 'db/conexion.py',
# que permite conectarse a la base de datos MySQL.

app = Flask(__name__)
# Crea una instancia de la aplicación Flask. 
# __name__ indica que se está ejecutando este archivo principal.
@app.route("/salas")
# Define una ruta web "/salas". 
# Cuando alguien abra esta URL en el navegador, se ejecuta la función siguiente.

def listar_salas():
    conn = obtener_conexion()
    # Llama a la función para conectarse a la base de datos.
    cursor = conn.cursor(dictionary=True)
    # Crea un cursor para ejecutar consultas SQL.
    # 'dictionary=True' hace que cada fila devuelta sea un diccionario con nombres de columna.
    cursor.execute("SELECT * FROM sala;")
    # Ejecuta la consulta SQL que obtiene todas las filas de la tabla 'sala'.
    salas = cursor.fetchall()
    # Recupera todos los resultados de la consulta y los guarda en la variable 'salas'.
    cursor.close()
    # Cierra el cursor para liberar recursos.
    conn.close()
    # Cierra la conexión con la base de datos.
    return jsonify(salas)
    # Convierte la lista de salas en formato JSON y la devuelve al navegador.
if __name__ == "__main__":
    app.run(debug=True)
    # Inicia la aplicación Flask.
    # 'debug=True' permite que se vea cualquier error y recarga la app automáticamente cuando se hacen cambios.