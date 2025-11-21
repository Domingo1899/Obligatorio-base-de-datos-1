# Obligatorio-base-de-datos-1
Sistema para Gestión de Reserva de Salas de Estudio

## Requisitos
- Python 
- MySQL  
- Instalar dependencias:
```bash
pip install flask mysql-connector-python
```

## Crear la base de datos
1. Ejecutar:
- `TablasObligatorio.sql`
- `IngresoDatos.sql`

2. Asegurarse de usar la base:
```sql
USE gestion_salas;
```

## Ejecutar el backend
Desde la carpeta **backend**:

```bash
python app.py
```

El servidor iniciará en:  
http://127.0.0.1:5000/

## Endpoints principales
- `GET /participantes`  
- `POST /participantes`  
- `GET /salas`  
- `POST /salas`  
- `POST /reservas` (incluye validaciones)  
- `POST /reservas/<id>/asistencia`  
- `POST /reservas/<id>/finalizar`  
- `GET /sanciones`

## Consultas SQL
Las consultas solicitadas están en **consultas.sql**.