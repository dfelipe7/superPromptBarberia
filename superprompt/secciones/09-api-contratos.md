# 09. Contratos de la API REST y Especificación OpenAPI

## 9.1 Convenciones Generales de la API
* **Base URL:** `/` (o prefijo de entorno de despliegue).
* **Documentación Interactiva:** Swagger UI expuesto en `/api/docs` y especificación cruda en `/api/docs-json`.
* **Formato de Comunicación:** JSON (`Content-Type: application/json; charset=utf-8`).
* **Autenticación:** Cabecera estándar HTTP `Authorization: Bearer <token_jwt>`.

---

## 9.2 Endpoints Principales por Módulo

### 1. Autenticación y Sesión (`/auth`)
* `POST /auth/google` ➔ Inicia sesión con Google OAuth 2.0. Recibe `{ idToken }` y retorna `{ accessToken, usuario }`.
* `POST /auth/refresh` ➔ Renueva el JWT con los roles vigentes en la base de datos (requiere Bearer token actual).

### 2. Administración y Personal (`/usuarios`)
* `GET /usuarios/me` ➔ Consulta el perfil del usuario autenticado.
* `POST /usuarios/administradores` ➔ Registra un nuevo administrador (exclusivo `@Roles('SUPERADMIN')`).
* `GET /usuarios/administradores` ➔ Lista todos los administradores (exclusivo `@Roles('SUPERADMIN')`).
* `PATCH /usuarios/administradores/:id/estado` ➔ Activa o suspende una cuenta de administrador.
* `GET /usuarios/barberos` ➔ Lista pública de barberos activos para el catálogo de reservas.
* `POST /usuarios/barberos` ➔ Da de alta un barbero en el sistema con su porcentaje de comisión inicial.
* `PATCH /usuarios/barberos/:id/comision` ➔ Actualiza la comisión pactada con el barbero.
* `POST /usuarios/barberos/foto` ➔ Sube la foto de perfil del barbero mediante `multipart/form-data`.

### 3. Catálogo de Servicios (`/servicios`)
* `GET /servicios` ➔ Lista pública de servicios activos con precio y duración.
* `POST /servicios` ➔ Crea un nuevo servicio estético (`@Roles('SUPERADMIN', 'ADMINISTRADOR')`).
* `PATCH /servicios/:id` ➔ Modifica precio, descripción o estado de un servicio.
* `GET /servicios/:servicioId/barberos` ➔ Retorna los barberos habilitados para ejecutar un servicio específico.

### 4. Horarios y Disponibilidad (`/usuarios/.../horarios`)
* `GET /usuarios/me/barbero/horario-semanal` ➔ Consulta el horario base del barbero en sesión.
* `PUT /usuarios/me/barbero/horario-semanal` ➔ Guarda la matriz de horas de atención por día de la semana.
* `POST /usuarios/me/barbero/bloqueos-horario` ➔ Registra un descanso o periodo no disponible.
* `GET /usuarios/barberos/:barberoId/disponibilidad?fecha=YYYY-MM-DD&servicioId=X` ➔ **Endpoint de consulta pública:** Retorna las franjas horarias libres de 60 minutos calculadas en tiempo real.

### 5. Reservas y Citas (`/reservas`)
* `POST /reservas` ➔ Crea una cita (cliente registrado o invitado). Retorna detalle de la cita y `tokenGestion`.
* `GET /reservas/barbero/me` ➔ Lista de citas asignadas al barbero en sesión filtradas por fecha.
* `PATCH /reservas/:reservaId/completar` ➔ Marca la cita como finalizada (`@Roles('BARBERO')`).
* `PATCH /reservas/:reservaId/no-show` ➔ Marca inasistencia del cliente tras la tolerancia.
* `PATCH /reservas/invitado/:reservaId/cancelar` ➔ Cancela una cita de invitado requiriendo el token en la cabecera `X-Reservation-Management-Token`.

---

## 9.3 Estructura Estándar de Respuestas de Error
Toda respuesta de error generada por el backend **DEBE** ajustarse estrictamente a este formato:

```json
{
  "statusCode": 403,
  "timestamp": "2026-10-20T04:50:38.474Z",
  "path": "/usuarios/administradores",
  "message": "No tienes permisos para realizar esta operación"
}
```
*(Se prohíbe exponer mensajes de error nativos de SQL o trazas internas de Node.js).*
