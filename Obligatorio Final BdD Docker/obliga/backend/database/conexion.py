import mysql.connector
import os
import time

def obtener_conexion():
    for _ in range(10):  # intenta 10 veces
        try:
            return mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASS", "rootpassword"),
                database=os.getenv("DB_NAME", "gestion_salas")
            )
        except mysql.connector.Error as err:
            print("Esperando conexión a MySQL...")
            time.sleep(2)  # espera 2 segundos antes de reintentar
    raise Exception("No se pudo conectar a la base de datos después de múltiples intentos.")
