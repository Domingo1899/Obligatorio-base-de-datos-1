from flask import Flask
from routes.participantes import participantes_bp
from routes.salas import salas_bp
from routes.reservas import reservas_bp
from routes.sanciones import sanciones_bp
from flask_cors import CORS 

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(participantes_bp)
app.register_blueprint(salas_bp)
app.register_blueprint(reservas_bp)
app.register_blueprint(sanciones_bp)

@app.route("/")
def inicio():
    return {
        "mensaje": "API de Reserva de Salas funcionando correctamente",
        "endpoints": [
            "/participantes",
            "/salas",
            "/reservas",
            "/sanciones"
        ]
    }

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

