# Usar una imagen base de Python (por ejemplo, Python 3.10 slim)
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el cdigo del backend al contenedor
COPY . . 

# Instalar las dependencias de Python (Flask, Flask-CORS, MySQL connector)
RUN pip install flask flask-cors mysql-connector-python  #:contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}

# Exponer el puerto 5000 (puerto por defecto donde corre el Flask backend)
EXPOSE 5000

# Comando por defecto para ejecutar la aplicación 
CMD ["python", "app.py"]
