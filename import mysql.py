import mysql.connector
# Importa la librería mysql.connector, que permite conectar Python con bases de datos MySQL.
def obtener_conexion():
        # Define una función llamada 'obtener_conexion' que devolverá un objeto de conexión
        # a la base de datos. Esto permite reutilizar la conexión cada vez que se necesite.
    return mysql.connector.connect(
        host="localhost",
        user="root",            # cambialo si usás otro usuario
        password="rootpassword", # poné tu contraseña real
        database="reserva_salas"
    )