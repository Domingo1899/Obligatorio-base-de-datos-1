const API = "http://127.0.0.1:5000";

/* PARTICIPANTES */
async function cargarParticipantes() {
    const id = document.getElementById("reservaId").value;

    if (!id) {
        alert("Ingrese un ID de reserva");
        return;
    }

    const resp = await fetch(`${API}/reservas/${id}`);
    const data = await resp.json();

    if (!resp.ok) {
        alert("Error: " + (data.error || "No se pudo obtener participantes"));
        return;
    }

    const participantes = data.participantes;

    document.getElementById("lista").innerHTML =
        participantes
            .map(p => `<li>${p.ci_participante} - ${p.nombre} ${p.apellido}</li>`)
            .join("");
}

function crearParticipante() {
    fetch(`${API}/participantes`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            ci: document.getElementById("ci").value,
            nombre: document.getElementById("nombre").value,
            apellido: document.getElementById("apellido").value,
            email: document.getElementById("email").value
        })
    })
    .then(response => response.json())
    .then(respuesta => {
        alert(respuesta.mensaje || "Operación realizada");
    })
    .catch(error => {
        console.error(error);
        alert("Error al crear participante");
    });
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
    fetch(`${API}/salas`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nombre: document.getElementById("nombre_sala").value,
            edificio: document.getElementById("edificio").value,
            capacidad: document.getElementById("capacidad").value,
            tipo: document.getElementById("tipo").value
        })
    })
    .then(response => response.json())
    .then(respuesta => {
        alert(respuesta.mensaje || "Sala creada correctamente");
    })
    .catch(err => {
        console.log(err);
        alert("Error al crear sala");
    });
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
    fetch(`${API}/reservas`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nombre_sala: document.getElementById("res_sala").value,
            edificio: document.getElementById("res_edificio").value,
            fecha: document.getElementById("res_fecha").value,
            id_turno: document.getElementById("res_turno").value,
            ci_participante: document.getElementById("res_ci").value,
            participantes: document.getElementById("res_participantes").value.split(",")
        })
    })
    .then(async response => {
        const data = await response.json();
        if (!response.ok) {
            alert("Error: " + (data.error || "No se pudo crear la reserva"));
        } else {
            alert(data.mensaje || "Reserva creada correctamente");
        }
    })
    .catch(err => {
        console.error(err);
        alert("Error al crear reserva");
    });
}

/* ASISTENCIA */
function registrarAsistencia() {
    const id = document.getElementById("id_reserva").value;
    const ci = document.getElementById("ci_participante").value;
    const asistio = document.getElementById("asistio").value;

    fetch(`${API}/reservas/${id}/asistencia`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            ci_participante: ci,
            asistio: asistio
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.mensaje || "Asistencia registrada correctamente");
    })
    .catch(error => {
        console.error(error);
        alert("Error al registrar asistencia");
    });
}

function finalizarReserva() {
    const id = document.getElementById("id_reserva_finalizar").value;

    fetch(`${API}/reservas/${id}/finalizar`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.mensaje || "Reserva finalizada correctamente");
    })
    .catch(error => {
        console.error(error);
        alert("Error al finalizar la reserva");
    });
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