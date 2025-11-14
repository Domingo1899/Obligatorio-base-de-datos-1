const API = "http://127.0.0.1:5000";

/* PARTICIPANTES */
function cargarParticipantes() {
    fetch(API + "/participantes")
        .then(r => r.json())
        .then(data => {
            document.getElementById("lista").innerHTML =
                data.map(p => `<li>${p.ci_participante} - ${p.nombre} ${p.apellido}</li>`).join("");
        });
}

function crearParticipante() {
    fetch(API + "/participantes", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            ci_participante: document.getElementById("ci").value,
            nombre: document.getElementById("nombre").value,
            apellido: document.getElementById("apellido").value,
            email: document.getElementById("email").value
        })
    }).then(r => r.json()).then(alert);
}

/* SALAS */
function cargarSalas() {
    fetch(API + "/salas")
        .then(r => r.json())
        .then(data => {
            document.getElementById("lista").innerHTML =
                data.map(s => `<li>${s.nombre_sala} (${s.edificio}) - Capacidad: ${s.capacidad}</li>`).join("");
        });
}

function crearSala() {
    fetch(API + "/salas", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            nombre_sala: document.getElementById("nombre_sala").value,
            edificio: document.getElementById("edificio").value,
            capacidad: document.getElementById("capacidad").value,
            tipo_sala: document.getElementById("tipo_sala").value
        })
    }).then(r => r.json()).then(alert);
}

/* RESERVAS */
function cargarReservas() {
    fetch(API + "/reservas")
        .then(r => r.json())
        .then(data => {
            document.getElementById("lista").innerHTML =
                data.map(r => `<li>ID ${r.id_reserva} - ${r.nombre_sala} - ${r.fecha}</li>`).join("");
        });
}

function crearReserva() {
    const participantes = document.getElementById("res_participantes").value
            .split(",")
            .map(x => x.trim())
            .filter(x => x !== "");

    fetch(API + "/reservas", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            nombre_sala: document.getElementById("res_sala").value,
            edificio: document.getElementById("res_edificio").value,
            fecha: document.getElementById("res_fecha").value,
            id_turno: document.getElementById("res_turno").value,
            ci_participante: document.getElementById("res_ci").value,
            participantes: participantes
        })
    }).then(r => r.json()).then(alert);
}

/* ASISTENCIA */
function registrarAsistencia() {
    fetch(`${API}/reservas/${document.getElementById("as_id_reserva").value}/asistencia`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            ci_participante: document.getElementById("as_ci").value,
            asistio: document.getElementById("as_asistio").value == "1"
        })
    }).then(r => r.json()).then(alert);
}

function finalizarReserva() {
    fetch(`${API}/reservas/${document.getElementById("fin_id_reserva").value}/finalizar`, {
        method: "POST"
    }).then(r => r.json()).then(alert);
}

/* DISPONIBILIDAD */
function verDisponibilidad() {
    const sala = document.getElementById("disp_sala").value;
    const edificio = document.getElementById("disp_edificio").value;
    const fecha = document.getElementById("disp_fecha").value;

    fetch(`${API}/disponibilidad?sala=${sala}&edificio=${edificio}&fecha=${fecha}`)
        .then(r => r.json())
        .then(data => {
            document.getElementById("resultado").innerText = JSON.stringify(data, null, 2);
        });
}