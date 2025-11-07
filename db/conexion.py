import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",            # tu usuario MySQL
        password="rootpassword", # tu contraseña real
        database="reserva_salas"
    )