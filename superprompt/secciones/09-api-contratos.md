# 09. Contratos de la API REST y Especificación OpenAPI Multitenant

## 9.1 Convenciones Generales de la API
* **Base URL:** `/` (o prefijo de entorno de despliegue).
* **Cabecera de Enrutamiento de Tenant (OBLIGATORIA para rutas de sede):** `X-Negocio-Slug: <slug>`.
* **Documentación Interactiva:** Swagger UI expuesto en `/api/docs` y especificación OpenAPI en `/api/docs-json`.
* **Autenticación:** Cabecera estándar HTTP `Authorization: Bearer <token_jwt>`.

---

## 9.2 Endpoints Principales por Módulo

### 1. Directorio Global y Plataforma SaaS (`/plataforma`)
* `GET /plataforma/negocios` ➔ Lista todas las barberías registradas con sus métricas en tiempo real (barberos, servicios, citas, clientes) y estado.
* `POST /plataforma/negocios` ➔ Da de alta un nuevo tenant en la plataforma, inicializa su perfil y asocia atómicamente a su Superadmin fundador.
* `PATCH /plataforma/negocios/:id/estado` ➔ Activa o suspende una barbería en la plataforma (`ACTIVO` / `INACTIVO`).

### 2. Identidad y Perfil de Sede (`/negocios/perfil`)
* `GET /negocios/perfil/publico` ➔ Consulta pública de la identidad de la sede (nombre, lema, dirección, coordenadas, radar y tema visual `temaKey`).
* `GET /negocios/perfil/gestion` ➔ Consulta administrativa del perfil para configuración del negocio.
* `PUT /negocios/perfil` ➔ Actualiza lema, dirección, coordenadas GPS (`latitud`, `longitud`) y tema visual (`temaKey`).
* `POST /negocios/perfil/archivos/:tipo` ➔ Sube archivos de marca validados (favicon, banner, logo blanco, logo negro).

### 3. Autenticación de Personal y Clientes
* `POST /auth/google` ➔ Inicia sesión de personal administrativo/barberos.
* `POST /auth/refresh` ➔ Renueva el JWT del personal resolviendo membresías del tenant activo.
* `POST /auth/clientes/google` ➔ Inicia sesión de cliente final con Google OAuth. Retorna `accessToken` de cliente y ficha en ese tenant.
* `GET /auth/clientes/perfil` ➔ Consulta el perfil del cliente autenticado en la sede.
* `PATCH /auth/clientes/perfil` ➔ Actualiza nombre o teléfono del cliente.

### 4. Personal y Barberos (`/usuarios`)
* `GET /usuarios/me` ➔ Consulta perfil y membresía del usuario en la sede actual.
* `GET /usuarios/barberos` ➔ Catálogo de barberos activos del tenant.
* `POST /usuarios/barberos` ➔ Vincula un nuevo barbero a la sede con comisión pactada.
* `PATCH /usuarios/barberos/:id/comision` ➔ Actualiza la comisión del barbero para este tenant.
* `POST /usuarios/administradores` ➔ Asigna membresía de administrador a un usuario en la sede.

### 5. Catálogo de Servicios (`/servicios`)
* `GET /servicios` ➔ Lista pública de servicios activos de la barbería con precio y duración.
* `POST /servicios` ➔ Crea un nuevo servicio para el tenant (`@Roles('SUPERADMIN', 'ADMINISTRADOR')`).
* `PATCH /servicios/:id` ➔ Modifica precio, duración o estado del servicio.
* `GET /servicios/:servicioId/barberos` ➔ Barberos del tenant habilitados para el servicio.

### 6. Horarios y Disponibilidad (`/usuarios/.../horarios`)
* `GET /usuarios/me/barbero/horario-semanal` ➔ Horario base semanal del barbero en esta sede.
* `PUT /usuarios/me/barbero/horario-semanal` ➔ Actualiza matriz de horarios semanales.
* `POST /usuarios/me/barbero/bloqueos-horario` ➔ Registra descansos o ausencias temporales.
* `GET /usuarios/barberos/:barberoId/disponibilidad?fecha=YYYY-MM-DD&servicioId=X` ➔ Franjas horarias libres de 60 minutos calculadas en tiempo real.

### 7. Reservas y Citas (`/reservas`)
* `POST /reservas` ➔ Agendamiento online (cliente autenticado o invitado). Retorna cita y `tokenGestion`.
* `POST /reservas/admin` ➔ Creación de reserva administrativa para clientes presenciales o registrados.
* `GET /reservas/me` ➔ Historial de citas del cliente autenticado en esta sede.
* `GET /reservas/barbero/me` ➔ Agenda diaria del barbero autenticado en la sede.
* `PATCH /reservas/:id/completar` ➔ Marca cita como finalizada.
* `PATCH /reservas/:id/no-show` ➔ Marca inasistencia del cliente.
* `PATCH /reservas/invitado/:id/cancelar` ➔ Cancela cita con token de gestión seguro.

---

## 9.3 Formato Estándar de Errores (JSON)
```json
{
  "statusCode": 403,
  "timestamp": "2026-11-02T19:30:00.000Z",
  "path": "/servicios",
  "message": "No tienes permisos para operar en esta barbería"
}
```
*(Se prohíbe exponer mensajes de error nativos de SQL o trazas internas de Node.js).*
