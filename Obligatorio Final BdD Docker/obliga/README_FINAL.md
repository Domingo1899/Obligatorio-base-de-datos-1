# Obligatorio – Sistema de Gestión de Reservas de Salas (Dockerizado)

Este proyecto implementa un sistema completo para la **gestión de reservas de salas**, incluyendo:

- Backend en **Flask (Python)**
- Frontend en **HTML + JavaScript (Nginx)**
- Base de datos **MySQL**
- Dockerización completa mediante `docker-compose`
- Importación automática de tablas y datos iniciales
- API REST para participantes, salas, reservas y sanciones

---

## 1. Estructura del Proyecto

```
obliga/
│
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── database/
│   │   ├── TablasObligatorio.sql
│   │   └── IngresoDatos.sql
│   └── Dockerfile
│
├── frontend/
│   ├── index.html
│   ├── salas.html
│   ├── participantes.html
│   ├── reservas.html
│   ├── sanciones.html
│   ├── app.js
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

---

## 2. Dockerización Completa

El sistema se ejecuta utilizando **tres contenedores Docker**:

### ✔ Backend – Flask  
Contiene la API del proyecto y corre en `http://localhost:5000`.

### ✔ Frontend – Nginx  
Sirve los archivos estáticos del frontend en `http://localhost`.

### ✔ MySQL – Base de Datos  
Incluye inicialización automática con:
- `TablasObligatorio.sql`
- `IngresoDatos.sql`

Y persiste datos mediante un volumen Docker.

---

## 3. Cómo Ejecutar el Proyecto con Docker

### 📌 Paso 1: Ejecutar el proyecto

Desde la carpeta `obliga/`:

```bash
docker-compose up --build
```

Esto:
- Construye las imágenes del backend y frontend
- Levanta la base de datos MySQL
- Crea tablas e inserta datos automáticamente (solo la primera vez)

### 📌 Paso 2: Acceder al sistema

- Frontend: http://localhost  
- API Backend: http://localhost:5000

---

## 4. Base de Datos: Importación Automática

Los SQL se copian a `/docker-entrypoint-initdb.d/` y se ejecutan automáticamente **la primera vez que se crea el contenedor MySQL**.

| Archivo SQL | Descripción |
|-------------|-------------|
| `TablasObligatorio.sql` | Crea todas las tablas necesarias |
| `IngresoDatos.sql` | Inserta datos iniciales solicitados |

### ❗ Reiniciar completamente la base de datos

```bash
docker-compose down -v
docker-compose up --build
```

---

## 5. Comandos Útiles

Reiniciar el sistema:

```bash
docker-compose down
docker-compose up
```

Borrar BD y reconstruir todo:

```bash
docker-compose down -v
docker-compose up --build
```

